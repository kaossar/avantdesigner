"""
Legal-Grade OCR Service
Implements a robust OCR pipeline using PyMuPDF (rendering) and EasyOCR (recognition).
Designed to handle scanned PDFs and Images without requiring external system binaries (Poppler/Tesseract).
"""

# ... (imports)
# ... (imports)
# ... (imports)
# ... (imports)
import logging
import fitz  # PyMuPDF
import easyocr
import numpy as np
import io
from typing import List, Dict, Any, Tuple
from PIL import Image

logger = logging.getLogger(__name__)

class OCRService:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(OCRService, cls).__new__(cls)
            cls._instance.reader = None # Lazy load
        return cls._instance

    def _get_reader(self):
        """Lazy load EasyOCR reader (heavy model)"""
        if self.reader is None:
            logger.info("🧠 Loading EasyOCR model (fr, en)... This might take a moment.")
            # gpu=False to be safe on standard user machines, or check cuda availability
            self.reader = easyocr.Reader(['fr', 'en'], gpu=False) 
        return self.reader

    def extract_text_from_image(self, image_bytes: bytes) -> str:
        """Perform OCR on a single image"""
        reader = self._get_reader()
        try:
            result = reader.readtext(image_bytes, detail=0, paragraph=True)
            return "\n\n".join(result)
        except Exception as e:
            logger.error(f"OCR Error on image: {e}")
            return ""

    def process_scanned_pdf(self, pdf_bytes: bytes) -> Dict[str, Any]:
        """
        Render PDF pages to images and perform OCR.
        Returns combined text and metadata.
        """
        full_text = []
        metadata = {"pages": 0, "ocr_confidence": "N/A (EasyOCR)"}
        
        try:
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            metadata["pages"] = len(doc)
            
            logger.info(f"📄 PDF has {len(doc)} pages. Starting OCR...")
            
            for page_num, page in enumerate(doc):
                logger.info(f"   👁️ OCR Processing Page {page_num + 1}/{len(doc)}")
                
                # Render page to image (zoom=2 for better quality)
                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
                img_bytes = pix.tobytes("png")
                
                # Perform OCR on the page image
                page_text = self.extract_text_from_image(img_bytes)
                if page_text.strip():
                   full_text.append(f"--- Page {page_num + 1} ---\n{page_text}")
            
            doc.close()
            
            combined_text = "\n\n".join(full_text)
            if not combined_text:
                return {"text": "", "error": "OCR produced no text"}
                
            return {"text": combined_text, "metadata": metadata}
            
        except Exception as e:
            logger.error(f"PDF OCR Failed: {e}")
            return {"text": "", "error": str(e)}

# Global instance
ocr_service = OCRService()
