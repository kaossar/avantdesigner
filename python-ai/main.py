from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables (support for Next.js .env.local)
from dotenv import load_dotenv
import os
from pathlib import Path

# Try connecting to parent directory .env.local if not running in root
env_path = Path(__file__).parent.parent / '.env.local'
if env_path.exists():
    logger.info(f"📂 Loading environment from {env_path}")
    load_dotenv(dotenv_path=env_path)
else:
    # Fallback to standard .env
    load_dotenv()

app = FastAPI(
    title="Contract Analysis AI Service",
    description="AI-powered contract analysis using Hugging Face models",
    version="1.0.0"
)

# CORS for Next.js
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response models
class AnalysisRequest(BaseModel):
    text: str
    contract_type: str = "auto"

class AnalysisResponse(BaseModel):
    contract_type: str
    summary: str
    entities: dict
    clauses: list
    risks: list
    score: dict
    recommendations: list
    metadata: dict

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "service": "ai-contract-analysis",
        "version": "1.0.0"
    }

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_contract(request: AnalysisRequest):
    """
    Analyze a contract using AI pipeline
    
    Pipeline:
    1. Text cleaning (spaCy)
    2. Chunking (LangChain)
    3. Classification (CamemBERT)
    4. NER (entity extraction)
    5. Clause analysis (Mistral 7B)
    6. Risk detection
    7. Score calculation
    8. Recommendations
    """
    try:
        logger.info(f"📥 Received analysis request ({len(request.text)} chars)")
        
        # Import pipeline (lazy loading to avoid startup delay)
        from pipeline import ContractAIPipeline
        
        # Initialize pipeline (singleton pattern will be used)
        pipeline = ContractAIPipeline()
        
        # Process contract
        result = await pipeline.process(request.text)
        
        logger.info(f"✅ Analysis complete: {result['metadata']['total_clauses']} clauses, {result['metadata']['high_risk_count']} high risks")
        
        return result
        
    except Exception as e:
        logger.error(f"❌ Analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

from fastapi import UploadFile, File, Form
from extraction.ocr_service import ocr_service
import fitz # PyMuPDF

@app.post("/analyze-file")
async def analyze_file(
    file: UploadFile = File(...),
    contract_type: str = Form("auto")
):
    """
    Handle file upload with Server-Side OCR (Legal Grade)
    Supports: PDF (Native & Scanned), Images
    """
    try:
        logger.info(f"📂 Receiving file: {file.filename} ({file.content_type})")
        contents = await file.read()
        
        text = ""
        
        # 1. Try Native Extraction (PDF)
        if file.content_type == "application/pdf":
            try:
                with fitz.open(stream=contents, filetype="pdf") as doc:
                    for page in doc:
                        text += page.get_text() + "\n"
            except Exception as e:
                logger.warning(f"Native PDF extraction failed: {e}")
        
        # 2. OCR Fallback (if text empty or Image)
        if len(text.strip()) < 50 or file.content_type.startswith("image/"):
            logger.info("🕵️ Triggering Legal-Grade OCR (EasyOCR)...")
            ocr_result = ocr_service.process_scanned_pdf(contents) if file.content_type == "application/pdf" else {"text": ocr_service.extract_text_from_image(contents)}
            
            if ocr_result.get("error"):
                 raise HTTPException(status_code=400, detail=f"OCR Failed: {ocr_result['error']}")
            
            text = ocr_result["text"]
            logger.info(f"✅ OCR complete. Extracted {len(text)} chars.")

        if not text.strip():
            raise HTTPException(status_code=400, detail="Could not extract text from file.")

        # 3. Run Pipeline
        from pipeline import ContractAIPipeline
        pipeline = ContractAIPipeline()
        result = await pipeline.process(text)
        
        # Add raw text to response so frontend knows extraction worked
        result["text"] = text
        
        import json
        # Ensure result is JSON serializable (sometimes float32 from numpy/torch causes issues)
        # Fast fix: rely on FastAPI's jsonable_encoder or just return dict.
        # But we need to be carefully with numpy types.
        
        return result

    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"❌ File analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"File analysis failed: {str(e)}")

@app.post("/export-pdf")
async def export_pdf(analysis_data: dict):
    """Export analysis results as professional PDF report"""
    try:
        logger.info("📄 Generating PDF report...")
        
        from export import generate_pdf_report
        from fastapi.responses import Response
        
        # Generate PDF
        pdf_bytes = generate_pdf_report(analysis_data)
        
        logger.info("✅ PDF generated successfully")
        
        # Return PDF as downloadable file
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=rapport_analyse_{analysis_data.get('contract_type', 'contrat')}.pdf"
            }
        )
        
    except Exception as e:
        logger.error(f"❌ PDF generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {str(e)}")

if __name__ == "__main__":
    logger.info("🚀 Starting AI Contract Analysis Service...")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
