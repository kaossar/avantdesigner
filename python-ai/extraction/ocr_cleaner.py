"""
Pure Algorithmic OCR Text Cleaner
NO hardcoded words - only pattern-based fixes
"""
import re
import unicodedata
from typing import Dict, List

class AlgorithmicOCRCleaner:
    """
    Pure algorithmic OCR cleaner - no word lists
    Uses only context-aware patterns
    """
    
    def __init__(self):
        # Pure algorithmic patterns (no hardcoded words)
        self.patterns = [
            # Ligatures
            (r'ﬁ', 'fi'), (r'ﬂ', 'fl'), (r'ﬀ', 'ff'), (r'ﬃ', 'ffi'), (r'ﬄ', 'ffl'),
            
            # Context-aware character fixes (numbers vs letters)
            (r'(?<=[a-zà-ÿ])0(?=[a-zà-ÿ])', 'o'),  # 0 in lowercase words
            (r'(?<=[A-ZÀ-Ÿ])0(?=[A-ZÀ-Ÿ])', 'O'),  # 0 in uppercase words
            (r'(?<=\d)l(?=\d)', '1'),  # l in numbers
            (r'(?<=\d)I(?=\d)', '1'),  # I in numbers
            (r'(?<=\d)O(?=\d)', '0'),  # O in numbers
            (r'(?<=\d)o(?=\d)', '0'),  # o in numbers
            (r'(?<=\d)S(?=\d)', '5'),  # S in numbers
            (r'(?<=\d)B(?=\d)', '8'),  # B in numbers
            (r'(?<=\d)Z(?=\d)', '2'),  # Z in numbers
            
            # Common OCR confusions (algorithmic)
            (r'\brn\b', 'm'),  # rn -> m at word boundaries
            (r'vv', 'w'), (r'VV', 'W'),
            
            # Phone numbers (French format detection)
            (r'(\d{2})[.,;:\s/]+(\d{2})[.,;:\s/]+(\d{2})[.,;:\s/]+(\d{2})[.,;:\s/]+(\d{2})', r'\1.\2.\3.\4.\5'),
            
            # Spacing fixes
            (r'\s+([,;:!?.\)\]])', r'\1'),
            (r'([,;:!?.\)])(?=[A-Za-zÀ-ÿ0-9])', r'\1 '),
            (r' {2,}', ' '),
            
            # Quotes normalization
            (r'[''`]', "'"), (r'[""«»]', '"'),
        ]
    
    def clean_text(self, text: str) -> Dict:
        """
        Clean OCR text using pure algorithmic patterns
        Returns: {original, cleaned, corrections, improvement_score}
        """
        if not text or not text.strip():
            return {'original': text, 'cleaned': text, 'corrections': [], 'improvement_score': 0.0}
        
        original = text
        cleaned = text
        corrections = []
        
        # 1. Unicode normalization
        cleaned = unicodedata.normalize('NFKC', cleaned)
        
        # 2. Apply algorithmic patterns
        for pattern, replacement in self.patterns:
            before = cleaned
            cleaned = re.sub(pattern, replacement, cleaned)
            if before != cleaned:
                corrections.append("Pattern fix")
        
        # 3. Final cleanup
        cleaned = self._final_cleanup(cleaned)
        
        return {
            'original': original,
            'cleaned': cleaned,
            'corrections': corrections,
            'improvement_score': self._calc_score(original, cleaned)
        }
    
    def _final_cleanup(self, text: str) -> str:
        """Final cleanup pass"""
        # Remove control characters
        text = ''.join(c for c in text if unicodedata.category(c)[0] != 'C' or c in '\n\t')
        
        # Normalize line breaks
        lines = [line.rstrip() for line in text.split('\n')]
        result = []
        blanks = 0
        for line in lines:
            if line.strip():
                result.append(line)
                blanks = 0
            elif blanks < 2:
                result.append(line)
                blanks += 1
        
        return '\n'.join(result).strip()
    
    def _calc_score(self, original: str, cleaned: str) -> float:
        """Calculate improvement percentage"""
        if original == cleaned or not original:
            return 0.0
        diff = sum(1 for i in range(min(len(original), len(cleaned))) if original[i] != cleaned[i])
        diff += abs(len(original) - len(cleaned))
        return round(min(100, (diff / len(original)) * 100), 2)


# Singleton
ocr_cleaner = AlgorithmicOCRCleaner()
