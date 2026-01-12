from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

if __name__ == "__main__":
    logger.info("🚀 Starting AI Contract Analysis Service...")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
