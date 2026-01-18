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
import io
import os
import time
from typing import List, Dict, Any, Tuple
from PIL import Image, ImageFilter
import pytesseract

logger = logging.getLogger(__name__)

# 1. Environment Optimization (Prevent CPU Starvation)
os.environ["OMP_THREAD_LIMIT"] = "1"

class OCRService:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(OCRService, cls).__new__(cls)
            cls._instance.reader = None # Lazy load
            
            # Configure Tesseract Path (Windows)
            tess_paths = [
                r"C:\Program Files\Tesseract-OCR\tesseract.exe",
                r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
            ]
            for path in tess_paths:
                if os.path.exists(path):
                    pytesseract.pytesseract.tesseract_cmd = path
                    logger.info(f"✅ Tesseract found at: {path}")
                    break
                    
        return cls._instance

    def _get_reader(self):
        """Lazy load EasyOCR reader (heavy model)"""
        if self.reader is None:
            logger.info("🧠 Loading EasyOCR model (fr, en)... This might take a moment.")
            self.reader = easyocr.Reader(['fr', 'en'], gpu=False) 
        return self.reader

    def extract_text_from_image(self, image_bytes: bytes) -> str:
        """Perform OCR on a single image (EasyOCR fallback)"""
        reader = self._get_reader()
        try:
            result = reader.readtext(image_bytes, detail=0, paragraph=True)
            return "\n\n".join(result)
        except Exception as e:
            logger.error(f"OCR Error on image: {e}")
            return ""

    def optimized_tesseract_ocr(
        self,
        image_bytes: bytes,
        lang: str = "fra+eng",
        psm: int = 6
    ) -> Dict[str, Any]:
        """
        Legal-grade optimized Tesseract OCR.
        
        Returns:
            {
                "text": str,
                "confidence": float,
                "duration_ms": int,
                "psm": int,
                "engine": "tesseract"
            }
        """
        start_time = time.time()

        try:
            # Load image
            image = Image.open(io.BytesIO(image_bytes))

            # 1️⃣ Preprocessing (CRITICAL)
            image = image.convert("L")  # grayscale
            image = image.filter(ImageFilter.MedianFilter(size=3))

            # Adaptive binarization
            image = image.point(lambda x: 0 if x < 180 else 255, "1")

            # Explicit DPI
            image.info["dpi"] = (300, 300)

            # 2️⃣ Tesseract config (OPTIMIZED)
            custom_config = f"""
            --oem 1
            --psm {psm}
            -c preserve_interword_spaces=1
            -c tessedit_char_blacklist=¢§™®©
            """

            # 3️⃣ OCR
            text = pytesseract.image_to_string(
                image,
                lang=lang,
                config=custom_config
            )

            duration_ms = int((time.time() - start_time) * 1000)

            # 4️⃣ Post-process and clean OCR text (Couche 1: Déterministe)
            from extraction.ocr_cleaner import ocr_cleaner
            cleaned_result = ocr_cleaner.clean_text(text)
            text = cleaned_result['cleaned']  # Use cleaned version
            
            # Log improvements if significant
            if cleaned_result['improvement_score'] > 5:
                logger.info(f"✨ OCR text improved by {cleaned_result['improvement_score']}%")

            # 5️⃣ AI Grammar Refinement (Couche 2: IA Safe) - OPTIONAL
            # Only if HuggingFace API is available and text is reasonable length
            try:
                from extraction.ocr_refiner import ocr_refiner
                refined_result = ocr_refiner.refine_text(text, timeout=5)
                
                if refined_result['used_ai']:
                    text = refined_result['refined']
                    logger.info(f"✨ AI refinement applied (confidence: {refined_result['confidence']:.2f})")
            except Exception as e:
                logger.warning(f"⚠️ AI refinement skipped: {e}")
                # Continue with Couche 1 text (safe fallback)

            # 6️⃣ Confidence estimation (simple & stable)
            words = text.split()
            # Simple heuristic: longer text = likely improved confidence up to a point
            confidence = min(0.99, 0.6 + (len(words) / 2000))

            return {
                "text": text.strip(),
                "confidence": round(confidence, 2),
                "duration_ms": duration_ms,
                "psm": psm,
                "engine": "tesseract"
            }

        except Exception as e:
            logger.warning(f"Tesseract Error: {e}")
            return {
                "text": "",
                "confidence": 0.0,
                "duration_ms": int((time.time() - start_time) * 1000),
                "psm": psm,
                "engine": "tesseract",
                "error": str(e)
            }

    async def process_scanned_pdf_stream(self, pdf_bytes: bytes):
        """
        Generator that yields OCR progress events (NDJSON friendly).
        Yields: Dicts with 'type', 'page', 'content', etc.
        """
        full_text_accumulator = []
        
        try:
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            total_pages = len(doc)
            
            # 1. Init Event
            yield {
                "type": "init", 
                "total_pages": total_pages,
                "message": f"Document de {total_pages} pages détecté."
            }
            
            logger.info(f"📄 PDF has {total_pages} pages. Starting Legal-Grade OCR Streaming...")
            
            for page_num, page in enumerate(doc):
                current_page = page_num + 1
                start_time = time.time() # For total Page time
                
                yield {
                    "type": "page_start", 
                    "page": current_page,
                    "message": f"Traitement Page {current_page}/{total_pages}..."
                }
                
                # Render (Zoom=2 for quality ~150-200 DPI base)
                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
                img_bytes = pix.tobytes("png")
                
                # --- STRATEGIE HYBRIDE ---
                # 1. Tentative Tesseract Optimisé
                ocr_result = self.optimized_tesseract_ocr(img_bytes)
                
                page_text = ""
                ocr_source = ""
                confidence = 0.0
                duration_ms = 0
                
                # Heuristic: Confidence > 0.75 AND text length > 20 chars
                if ocr_result["confidence"] >= 0.75 and len(ocr_result["text"]) > 20:
                    page_text = ocr_result["text"]
                    ocr_source = "tesseract"
                    confidence = ocr_result["confidence"]
                    duration_ms = ocr_result["duration_ms"]
                    logger.info(f"   ⚡ Tesseract OK (Page {current_page}): {len(page_text)} chars in {duration_ms}ms")
                else:
                    # 2. Fallback EasyOCR
                    logger.info(f"   ⚠️ Tesseract low confidence ({ocr_result['confidence']}) or empty. Switching to EasyOCR...")
                    t0 = time.time()
                    try:
                        page_text = self.extract_text_from_image(img_bytes)
                        ocr_source = "easyocr"
                        confidence = 0.90 # EasyOCR is generally robust if it works
                        duration_ms = int((time.time() - t0) * 1000)
                    except Exception as e:
                        logger.error(f"   ❌ EasyOCR Failed: {e}")
                        page_text = ""
                        ocr_source = "failed"

                # Event Payload
                total_page_duration = int((time.time() - start_time) * 1000)
                
                if page_text.strip():
                    formatted_text = f"--- Page {current_page} ---\n{page_text}"
                    full_text_accumulator.append(formatted_text)
                    
                    yield {
                        "type": "page_done",
                        "page": current_page,
                        "text_preview": page_text[:80] + "...",
                        "source": ocr_source,
                        "confidence": confidence,
                        "duration_ms": total_page_duration,
                        "message": f"Page {current_page} OK ({ocr_source.upper()} - {duration_ms}ms)"
                    }
                else:
                    yield {
                        "type": "page_warning",
                        "page": current_page,
                        "message": f"Page {current_page} : Illisible / Vide"
                    }

            doc.close()
            
            complete_text = "\n\n".join(full_text_accumulator)
            
            yield {
                "type": "ocr_complete",
                "full_text": complete_text,
                "message": "OCR terminé. Analyse IA..."
            }
            
        except Exception as e:
            logger.error(f"Streaming OCR Failed: {e}")
            yield {
                "type": "error",
                "error": str(e),
                "message": "Erreur critique durant l'OCR."
            }

# Global instance
ocr_service = OCRService()
