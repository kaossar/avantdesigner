
import easyocr
import logging
import sys

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    try:
        logger.info("⬇️ Attempting to download/load EasyOCR models...")
        # Force download
        reader = easyocr.Reader(['fr', 'en'], gpu=False, download_enabled=True, verbose=True)
        logger.info("✅ Model loaded successfully!")
    except Exception as e:
        logger.error(f"❌ Failed to load model: {e}")
        # Print full traceback
        import traceback
        traceback.print_exc()
        sys.exit(1)
