
import sys
try:
    print("1. Importing EasyOCR...")
    import easyocr
    print("   Success.")
except Exception as e:
    print(f"   Failed to import easyocr: {e}")
    sys.exit(1)

try:
    print("2. Importing PyMuPDF (fitz)...")
    import fitz
    print("   Success.")
except Exception as e:
    print(f"   Failed to import fitz: {e}")
    sys.exit(1)

try:
    print("3. Initializing Reader (Model Download/Load)...")
    reader = easyocr.Reader(['en'], gpu=False, verbose=True)
    print("   Success.")
except Exception as e:
    print(f"   Failed to initialize Reader: {e}")
    sys.exit(1)

print("✅ Environment is READY for OCR.")
