"""
OCR Text Post-Processing - Generic & Intelligent
Cleans and improves OCR output using algorithmic patterns, not hardcoded words
Works on ANY text, ANY language, ANY document type
"""
import re
from typing import Dict, List, Tuple
import unicodedata

class OCRTextCleaner:
    """
    Generic OCR text cleaner using algorithmic pattern detection
    NO hardcoded word lists - works on any document
    """
    
    def __init__(self):
        # Character confusion patterns (algorithmic, not hardcoded)
        self.char_patterns = [
            # Common OCR character confusions (context-aware)
            (r'(?<=[a-z])0(?=[a-z])', 'o'),  # 0 -> o in lowercase words
            (r'(?<=[A-Z])0(?=[A-Z])', 'O'),  # 0 -> O in uppercase words
            (r'(?<=\d)l(?=\d)', '1'),        # l -> 1 in numbers
            (r'(?<=\d)I(?=\d)', '1'),        # I -> 1 in numbers
            (r'(?<=\d)O(?=\d)', '0'),        # O -> 0 in numbers
            (r'(?<=\d)o(?=\d)', '0'),        # o -> 0 in numbers
            (r'(?<=\d)S(?=\d)', '5'),        # S -> 5 in numbers
            (r'(?<=\d)B(?=\d)', '8'),        # B -> 8 in numbers
            (r'(?<=\d)Z(?=\d)', '2'),        # Z -> 2 in numbers
            
            # Ligature fixes
            (r'ﬁ', 'fi'),
            (r'ﬂ', 'fl'),
            (r'ﬀ', 'ff'),
            (r'ﬃ', 'ffi'),
            (r'ﬄ', 'ffl'),
            (r'ﬆ', 'st'),
            
            # Common OCR artifacts
            (r'rn', 'm'),   # rn often confused with m
            (r'vv', 'w'),   # vv -> w
            (r'VV', 'W'),   # VV -> W
        ]
        
        # Punctuation and spacing patterns
        self.spacing_patterns = [
            # Remove space before punctuation
            (r'\s+([,;:!?.\)])', r'\1'),
            
            # Add space after punctuation (if missing)
            (r'([,;:!?.\)])(?=[A-Za-zÀ-ÿ0-9])', r'\1 '),
            
            # Fix multiple spaces
            (r' {2,}', ' '),
            
            # Fix space after opening parenthesis
            (r'\(\s+', '('),
            
            # Fix space before closing parenthesis
            (r'\s+\)', ')'),
            
            # Normalize quotes
            (r'[''`]', "'"),
            (r'[""«»]', '"'),
            
            # Remove trailing spaces on lines
            (r' +$', '', re.MULTILINE),
        ]
        
        # Phone number patterns (French format)
        self.phone_patterns = [
            # Fix broken phone numbers: 02.38,;3.17.62 -> 02.38.53.17.62
            (r'(\d{2})[.,;:\s]+(\d{2})[.,;:\s]+(\d{2})[.,;:\s]+(\d{2})[.,;:\s]+(\d{2})', r'\1.\2.\3.\4.\5'),
            (r'(\d{2})[.,;:\s]+(\d{2})[.,;:\s]+(\d{2})[.,;:\s]+(\d{2})', r'\1.\2.\3.\4'),
        ]
    
    def clean_text(self, text: str) -> Dict[str, any]:
        """
        Clean OCR text using generic algorithmic patterns
        
        Returns:
            {
                'original': raw text,
                'cleaned': improved text,
                'corrections': list of corrections made,
                'improvement_score': percentage improvement
            }
        """
        if not text or not text.strip():
            return {
                'original': text,
                'cleaned': text,
                'corrections': [],
                'improvement_score': 0.0
            }
        
        original = text
        cleaned = text
        corrections = []
        
        # 1. Normalize unicode (remove weird characters)
        cleaned = self._normalize_unicode(cleaned)
        if cleaned != text:
            corrections.append("Unicode normalization")
        
        # 2. Apply character pattern fixes
        for pattern, replacement in self.char_patterns:
            before = cleaned
            cleaned = re.sub(pattern, replacement, cleaned)
            if before != cleaned:
                corrections.append(f"Char pattern: {pattern[:20]}...")
        
        # 3. Fix phone numbers
        for pattern, replacement in self.phone_patterns:
            before = cleaned
            cleaned = re.sub(pattern, replacement, cleaned)
            if before != cleaned:
                corrections.append("Phone number normalization")
        
        # 4. Apply spacing and punctuation fixes
        for item in self.spacing_patterns:
            if len(item) == 2:
                pattern, replacement = item
                flags = 0
            else:
                pattern, replacement, flags = item
            
            before = cleaned
            cleaned = re.sub(pattern, replacement, cleaned, flags=flags)
            if before != cleaned:
                corrections.append(f"Spacing: {pattern[:20]}...")
        
        # 5. Fix broken words at line breaks
        cleaned = self._fix_broken_words(cleaned)
        
        # 6. Remove excessive blank lines
        cleaned = self._normalize_line_breaks(cleaned)
        
        # 7. Final cleanup
        cleaned = cleaned.strip()
        
        return {
            'original': original,
            'cleaned': cleaned,
            'corrections': corrections,
            'improvement_score': self._calculate_improvement_score(original, cleaned)
        }
    
    def _normalize_unicode(self, text: str) -> str:
        """
        Normalize unicode characters to their closest ASCII equivalent
        Removes weird OCR artifacts while preserving accented characters
        """
        # Normalize to NFKC (compatibility decomposition + canonical composition)
        normalized = unicodedata.normalize('NFKC', text)
        
        # Remove control characters except newlines and tabs
        cleaned = ''.join(
            char for char in normalized
            if unicodedata.category(char)[0] != 'C' or char in '\n\t'
        )
        
        return cleaned
    
    def _fix_broken_words(self, text: str) -> str:
        """
        Fix words broken across line breaks (heuristic approach)
        Example: "ges-\ntionnaire" -> "gestionnaire"
        """
        # Pattern: lowercase letter + hyphen + newline + lowercase letter
        # This is a common OCR artifact for broken words
        fixed = re.sub(r'([a-zà-ÿ])-\s*\n\s*([a-zà-ÿ])', r'\1\2', text)
        
        # Pattern: lowercase letter + newline + lowercase letter (no hyphen)
        # Only if the line is very short (likely broken word)
        lines = fixed.split('\n')
        result = []
        i = 0
        while i < len(lines):
            current_line = lines[i].rstrip()
            
            # Check if this line might be a broken word
            if (i < len(lines) - 1 and 
                len(current_line) > 0 and 
                len(current_line) < 50 and  # Short line
                current_line[-1].islower() and  # Ends with lowercase
                len(lines[i + 1]) > 0 and
                lines[i + 1][0].islower()):  # Next line starts with lowercase
                
                # Likely a broken word - merge
                result.append(current_line + lines[i + 1].lstrip())
                i += 2
            else:
                result.append(current_line)
                i += 1
        
        return '\n'.join(result)
    
    def _normalize_line_breaks(self, text: str) -> str:
        """
        Normalize line breaks and remove excessive blank lines
        """
        # Split into lines
        lines = text.split('\n')
        
        # Remove excessive blank lines (max 2 consecutive)
        cleaned_lines = []
        blank_count = 0
        
        for line in lines:
            if line.strip():
                cleaned_lines.append(line)
                blank_count = 0
            else:
                blank_count += 1
                if blank_count <= 2:
                    cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines)
    
    def _calculate_improvement_score(self, original: str, cleaned: str) -> float:
        """
        Calculate improvement score based on character differences
        Returns percentage (0-100)
        """
        if original == cleaned:
            return 0.0
        
        # Count character differences
        min_len = min(len(original), len(cleaned))
        char_diff = sum(1 for i in range(min_len) if original[i] != cleaned[i])
        char_diff += abs(len(original) - len(cleaned))
        
        # Calculate percentage
        if len(original) == 0:
            return 0.0
        
        improvement = (char_diff / len(original)) * 100
        
        return round(min(100, improvement), 2)


# Singleton instance
ocr_cleaner = OCRTextCleaner()
