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

from fastapi.responses import StreamingResponse
import json

async def analysis_stream_generator(file_obj, contents, contract_type):
    """
    Orchestrates the streaming process:
    1. OCR/Text Extraction (Yields progress)
    2. AI Analysis (Yields output)
    """
    text = ""
    ocr_mode = False
    
    # CRITICAL: Yield immediately to start streaming
    yield json.dumps({"type": "info", "message": "Connexion établie. Lecture du fichier..."}) + "\n"
    
    # Read file content inside generator (non-blocking for HTTP headers)
    if contents is None:
        contents = await file_obj.read()
    
    yield json.dumps({"type": "info", "message": "Fichier chargé. Analyse en cours..."}) + "\n"
    
    # 1. Determine Extraction Method
    if file_obj.content_type == "application/pdf":
        # Check if native
        try:
            is_native = False
            with fitz.open(stream=contents, filetype="pdf") as doc:
                # heuristic: check first page text
                if len(doc) > 0 and len(doc[0].get_text().strip()) > 50:
                    is_native = True
                
            if is_native:
                yield json.dumps({"type": "info", "message": "PDF natif détecté (Extraction rapide)..."}) + "\n"
                with fitz.open(stream=contents, filetype="pdf") as doc:
                    for page in doc:
                        text += page.get_text() + "\n"
                yield json.dumps({"type": "ocr_complete", "full_text": text, "message": "Extraction terminée."}) + "\n"
            else:
                ocr_mode = True
        except:
             ocr_mode = True
    else:
        ocr_mode = True
        
    # 2. Run OCR if needed
    if ocr_mode:
        yield json.dumps({"type": "info", "message": "Scan détecté. Démarrage OCR..."}) + "\n"
        if file_obj.content_type == "application/pdf":
            # Stream from OCR Service
            async for event in ocr_service.process_scanned_pdf_stream(contents):
                if event["type"] == "ocr_complete":
                    text = event["full_text"]
                yield json.dumps(event) + "\n"
        else:
            # Image OCR (Simple for now, can be streamed if needed)
            yield json.dumps({"type": "page_start", "page": 1, "message": "Traitement image..."}) + "\n"
            text = ocr_service.extract_text_from_image(contents)
            yield json.dumps({"type": "ocr_complete", "full_text": text, "message": "Image analysée."}) + "\n"

    if not text.strip():
        yield json.dumps({"type": "error", "error": "Aucun texte extrait du fichier."}) + "\n"
        return

    # 3. AI Analysis Pipeline
    yield json.dumps({"type": "stage", "stage": "analysis", "message": "Analyse juridique et détection des risques..."}) + "\n"
    
    try:
        from pipeline import ContractAIPipeline
        pipeline = ContractAIPipeline()
        result = await pipeline.process(text)
        
        # Add raw text for frontend
        result["text"] = text
        
        yield json.dumps({"type": "complete", "data": result}) + "\n"
        
    except Exception as e:
        logger.error(f"Analysis Pipeline Failed: {e}")
        yield json.dumps({"type": "error", "error": f"Erreur analyse IA: {str(e)}"}) + "\n"


@app.post("/analyze-file")
async def analyze_file(
    file: UploadFile = File(...),
    contract_type: str = Form("auto")
):
    """
    Handle file upload with Server-Side Streaming (NDJSON)
    """
    try:
        logger.info(f"📂 Streaming Request: {file.filename}")
        
        # Return StreamingResponse immediately (don't await file.read() here!)
        return StreamingResponse(
            analysis_stream_generator(file, None, contract_type),
            media_type="application/x-ndjson"
        )
            
    except Exception as e:
        logger.error(f"❌ Initialization failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Init failed: {str(e)}")

@app.post("/extract-text")
async def extract_text(
    file: UploadFile = File(...),
):
    """
    Extract text from file using OCR (streaming, no AI analysis)
    Returns NDJSON stream with OCR progress
    """
    try:
        logger.info(f"📂 OCR-only Request: {file.filename}")
        
        async def ocr_only_generator(file_obj):
            """Generator for OCR-only processing"""
            yield json.dumps({"type": "info", "message": "Connexion établie. Lecture du fichier..."}) + "\n"
            
            contents = await file_obj.read()
            yield json.dumps({"type": "info", "message": "Fichier chargé. Démarrage OCR..."}) + "\n"
            
            # Determine if PDF or image
            if file_obj.content_type == "application/pdf":
                # Check if native PDF
                try:
                    is_native = False
                    with fitz.open(stream=contents, filetype="pdf") as doc:
                        if len(doc) > 0 and len(doc[0].get_text().strip()) > 50:
                            is_native = True
                    
                    if is_native:
                        yield json.dumps({"type": "info", "message": "PDF natif détecté (Extraction rapide)..."}) + "\n"
                        text = ""
                        with fitz.open(stream=contents, filetype="pdf") as doc:
                            for page in doc:
                                text += page.get_text() + "\n"
                        yield json.dumps({"type": "ocr_complete", "full_text": text, "message": "Extraction terminée."}) + "\n"
                    else:
                        # Scanned PDF - use OCR service
                        async for event in ocr_service.process_scanned_pdf_stream(contents):
                            yield json.dumps(event) + "\n"
                except:
                    # Fallback to OCR
                    async for event in ocr_service.process_scanned_pdf_stream(contents):
                        yield json.dumps(event) + "\n"
            else:
                # Image OCR
                yield json.dumps({"type": "page_start", "page": 1, "message": "Traitement image..."}) + "\n"
                text = ocr_service.extract_text_from_image(contents)
                yield json.dumps({"type": "ocr_complete", "full_text": text, "message": "Image analysée."}) + "\n"
            
            yield json.dumps({"type": "complete", "message": "Extraction terminée."}) + "\n"
        
        return StreamingResponse(
            ocr_only_generator(file),
            media_type="application/x-ndjson"
        )
            
    except Exception as e:
        logger.error(f"❌ OCR extraction failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"OCR failed: {str(e)}")

from pydantic import BaseModel

class TextAnalysisRequest(BaseModel):
    text: str
    contract_type: str = "auto"

@app.post("/analyze-text")
async def analyze_text(request: TextAnalysisRequest):
    """
    Analyze pre-extracted text using AI pipeline
    Returns complete analysis results
    """
    try:
        logger.info(f"🧠 Analyzing text ({len(request.text)} chars)")
        
        if not request.text.strip():
            raise HTTPException(status_code=400, detail="Text cannot be empty")
        
        # Initialize AI pipeline
        pipeline = ContractAIPipeline()
        
        # Process contract
        result = await pipeline.process(request.text)
        
        # Add original text to result
        result["text"] = request.text
        
        logger.info(f"✅ Analysis complete: {result['metadata']['total_clauses']} clauses, {result['metadata']['high_risk_count']} high risks")
        
        return result
        
    except Exception as e:
        logger.error(f"❌ Text analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

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
