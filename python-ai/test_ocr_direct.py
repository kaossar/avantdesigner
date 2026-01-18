import asyncio
import os
import sys
# Add current dir to path so we can import extraction
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from extraction.ocr_service import ocr_service

async def test_stream():
    print("Testing OCR Stream...")
    # Create a minimal valid PDF (empty) or just random bytes?
    # PyMuPDF needs a valid PDF header.
    # I'll enable a dummy check or just try to open a non-existent file to see if it even calls logic?
    # No, let's create a minimal PDF using fitz
    import fitz
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((50, 50), "Hello World Tesseract Test")
    pdf_bytes = doc.tobytes()
    
    print(f"Generated PDF bytes: {len(pdf_bytes)}")
    
    iterator = ocr_service.process_scanned_pdf_stream(pdf_bytes)
    
    async for event in iterator:
        print(f"Event Received: {event['type']}")
        if event['type'] == 'error':
            print(f"ERROR: {event['error']}")
        if event['type'] == 'ocr_complete':
            print("Completed!")
            print(event['full_text'][:100])

if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(test_stream())
