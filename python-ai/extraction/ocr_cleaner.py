"""
Professional OCR Post-Processing with Spell Checking
Uses mature Python libraries for production-grade text correction
"""
import re
from typing import Dict, List
import unicodedata
import logging

logger = logging.getLogger(__name__)

class ProfessionalOCRCleaner:
    """
    Production-grade OCR text cleaner with spell checking
    Uses SymSpell for ultra-fast corrections
    """
    
    def __init__(self):
        self.spell_checker = None
        self._init_spell_checker()
        
        # Common OCR patterns (algorithmic)
        self.patterns = self._build_patterns()
    
    def _init_spell_checker(self):
        """Initialize spell checker (SymSpell if available, fallback otherwise)"""
        try:
            from symspellpy import SymSpell, Verbosity
            import pkg_resources
            
            self.spell_checker = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
            
            # Load French dictionary
            dictionary_path = pkg_resources.resource_filename(
                "symspellpy", "frequency_dictionary_fr_62_000.txt"
            )
            
            self.spell_checker.load_dictionary(dictionary_path, term_index=0, count_index=1)
            logger.info("✅ SymSpell spell checker initialized (French)")
            
        except Exception as e:
            logger.warning(f"⚠️ SymSpell not available: {e}. Using basic cleaning only.")
            self.spell_checker = None
    
    def _build_patterns(self) -> List[tuple]:
        """Build OCR correction patterns"""
        return [
            # Fix ligatures
            (r'ﬁ', 'fi'),
            (r'ﬂ', 'fl'),
            (r'ﬀ', 'ff'),
            (r'ﬃ', 'ffi'),
            (r'ﬄ', 'ffl'),
            
            # Context-aware character fixes
            (r'(?<=[a-z])0(?=[a-z])', 'o'),  # 0 -> o in words
            (r'(?<=[A-Z])0(?=[A-Z])', 'O'),  # 0 -> O in uppercase
            (r'(?<=\d)l(?=\d)', '1'),        # l -> 1 in numbers
            (r'(?<=\d)I(?=\d)', '1'),        # I -> 1 in numbers
            (r'(?<=\d)O(?=\d)', '0'),        # O -> 0 in numbers
            (r'(?<=\d)S(?=\d)', '5'),        # S -> 5 in numbers
            
            # Common OCR artifacts
            (r'rn', 'm'),   # rn -> m (very common)
            (r'vv', 'w'),   # vv -> w
            (r'VV', 'W'),   # VV -> W
            (r'cl', 'd'),   # cl -> d
            
            # Phone numbers (French format)
            (r'(\d{2})[.,;:\s]+(\d{2})[.,;:\s]+(\d{2})[.,;:\s]+(\d{2})[.,;:\s]+(\d{2})', r'\1.\2.\3.\4.\5'),
            
            # Spacing fixes
            (r'\s+([,;:!?.\)])', r'\1'),  # Remove space before punctuation
            (r'([,;:!?.\)])(?=[A-Za-zÀ-ÿ0-9])', r'\1 '),  # Add space after
            (r' {2,}', ' '),  # Multiple spaces
            
            # Quotes normalization
            (r'[''`]', "'"),
            (r'[""«»]', '"'),
        ]
    
    def clean_text(self, text: str) -> Dict:
        """
        Clean OCR text with spell checking
        
        Returns:
            {
                'original': raw text,
                'cleaned': improved text,
                'corrections': list of corrections,
                'improvement_score': percentage
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
        
        # 1. Unicode normalization
        cleaned = unicodedata.normalize('NFKC', cleaned)
        
        # 2. Apply regex patterns
        for pattern, replacement in self.patterns:
            before = cleaned
            cleaned = re.sub(pattern, replacement, cleaned)
            if before != cleaned:
                corrections.append(f"Pattern: {pattern[:20]}")
        
        # 3. Spell checking (if available)
        if self.spell_checker:
            cleaned, spell_corrections = self._apply_spell_checking(cleaned)
            corrections.extend(spell_corrections)
        
        # 4. Final cleanup
        cleaned = self._final_cleanup(cleaned)
        
        return {
            'original': original,
            'cleaned': cleaned,
            'corrections': corrections,
            'improvement_score': self._calculate_score(original, cleaned)
        }
    
    def _apply_spell_checking(self, text: str) -> tuple:
        """Apply spell checking to text"""
        from symspellpy import Verbosity
        
        corrections = []
        words = text.split()
        corrected_words = []
        
        for word in words:
            # Skip if word is too short, all caps, or contains numbers
            if len(word) < 3 or word.isupper() or any(c.isdigit() for c in word):
                corrected_words.append(word)
                continue
            
            # Clean word (remove punctuation)
            clean_word = re.sub(r'[^\w\-àâäéèêëïîôùûüÿæœç]', '', word, flags=re.IGNORECASE)
            
            if not clean_word:
                corrected_words.append(word)
                continue
            
            # Get suggestions
            suggestions = self.spell_checker.lookup(
                clean_word.lower(),
                Verbosity.CLOSEST,
                max_edit_distance=2
            )
            
            if suggestions and suggestions[0].term != clean_word.lower():
                # Found a better match
                corrected = suggestions[0].term
                
                # Preserve original capitalization
                if clean_word[0].isupper():
                    corrected = corrected.capitalize()
                
                # Replace in original word (preserve punctuation)
                corrected_word = word.replace(clean_word, corrected)
                corrected_words.append(corrected_word)
                corrections.append(f"Spell: {clean_word} → {corrected}")
            else:
                corrected_words.append(word)
        
        return ' '.join(corrected_words), corrections
    
    def _final_cleanup(self, text: str) -> str:
        """Final cleanup pass"""
        # Remove control characters except newlines/tabs
        text = ''.join(
            char for char in text
            if unicodedata.category(char)[0] != 'C' or char in '\n\t'
        )
        
        # Normalize line breaks
        lines = text.split('\n')
        cleaned_lines = []
        blank_count = 0
        
        for line in lines:
            line = line.rstrip()
            if line.strip():
                cleaned_lines.append(line)
                blank_count = 0
            else:
                blank_count += 1
                if blank_count <= 2:
                    cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines).strip()
    
    def _calculate_score(self, original: str, cleaned: str) -> float:
        """Calculate improvement score"""
        if original == cleaned:
            return 0.0
        
        char_diff = sum(1 for i in range(min(len(original), len(cleaned))) 
                       if original[i] != cleaned[i])
        char_diff += abs(len(original) - len(cleaned))
        
        if len(original) == 0:
            return 0.0
        
        return round(min(100, (char_diff / len(original)) * 100), 2)


# Singleton
ocr_cleaner = ProfessionalOCRCleaner()
