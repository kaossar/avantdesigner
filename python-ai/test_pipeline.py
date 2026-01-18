
import asyncio
import logging
from pipeline import ContractAIPipeline

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_pipeline():
    logger.info("🧪 Testing AI Pipeline Integrity...")
    
    try:
        pipeline = ContractAIPipeline()
        
        # Mock text (simulating OCR output)
        dummy_text = """
        CONTRAT DE LOCATION
        
        Article 1 : Durée
        Le présent contrat est conclu pour une durée de 3 ans.
        
        Article 2 : Loyer
        Le loyer est fixé à 800 euros par mois.
        
        Article 3 : Dépôt de garantie
        Le dépôt de garantie est fixé à 3 mois de loyer hors charges.
        """
        
        logger.info("▶️ Running process()...")
        result = await pipeline.process(dummy_text)
        
        logger.info("✅ Pipeline Success!")
        print("Summary:", result['summary'])
        print("Risks:", len(result['risks']))
        
    except Exception as e:
        logger.error(f"❌ Pipeline Failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_pipeline())
