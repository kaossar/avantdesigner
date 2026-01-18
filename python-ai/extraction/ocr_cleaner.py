"""
OCR Text Post-Processing with AI
Cleans and improves OCR output before displaying to user
"""
import re
from typing import Dict, List

class OCRTextCleaner:
    """
    Post-processes OCR text to improve quality and readability
    """
    
    def __init__(self):
        # Common OCR errors mapping (French legal documents)
        self.common_errors = {
            # Numbers confused with letters
            r'\b0(?=[A-Z])': 'O',  # 0 -> O at start of words
            r'(?<=[A-Z])0\b': 'O',  # 0 -> O at end of words
            r'\bl(?=\d)': '1',      # l -> 1 before numbers
            r'(?<=\d)l\b': '1',     # l -> 1 after numbers
            
            # Common French legal terms corrections
            r'sÉCU57': 'SÉCURITÉ',
            r'assistancr': 'assistance',
            r'avenuc': 'avenue',
            r'Gcorges': 'Georges',
            r'SaINT': 'SAINT',
            r'RUEUE': 'RUELLE',
            r'PARTENARIAI': 'PARTENARIAT',
            r'ENTRE-LES': 'ENTRE LES',
            r'Clémenceau': 'Clemenceau',
            
            # Spacing issues
            r'(\d),;(\d)': r'\1.\2',  # Fix decimal separators
            r'24/20': '24.20',         # Phone number format
            
            # Common punctuation errors
            r"'(?=[A-Z])": "'",        # Fix apostrophes
            r';(?=[A-Z])': ':',        # Semicolon -> colon before capitals
        }
        
        # Legal document structure patterns
        self.structure_patterns = {
            'article': r'Article\s+(\d+)',
            'clause': r'Clause\s+(\d+)',
            'section': r'Section\s+(\d+)',
        }
    
    def clean_text(self, raw_text: str) -> Dict[str, str]:
        """
        Clean and improve OCR text
        
        Returns:
            {
                'original': raw_text,
                'cleaned': improved_text,
                'corrections': list of corrections made
            }
        """
        corrections = []
        cleaned = raw_text
        
        # Apply common error corrections
        for pattern, replacement in self.common_errors.items():
            matches = re.findall(pattern, cleaned)
            if matches:
                corrections.append(f"Fixed: {pattern} -> {replacement} ({len(matches)} occurrences)")
                cleaned = re.sub(pattern, replacement, cleaned)
        
        # Fix spacing around punctuation
        cleaned = self._fix_spacing(cleaned)
        
        # Normalize line breaks
        cleaned = self._normalize_line_breaks(cleaned)
        
        # Fix capitalization in titles
        cleaned = self._fix_capitalization(cleaned)
        
        return {
            'original': raw_text,
            'cleaned': cleaned,
            'corrections': corrections,
            'improvement_score': self._calculate_improvement_score(raw_text, cleaned)
        }
    
    def _fix_spacing(self, text: str) -> str:
        """Fix spacing issues around punctuation"""
        # Remove spaces before punctuation
        text = re.sub(r'\s+([,;:!?.])', r'\1', text)
        # Add space after punctuation if missing
        text = re.sub(r'([,;:!?.])(?=[A-Za-z])', r'\1 ', text)
        # Fix multiple spaces
        text = re.sub(r'\s{2,}', ' ', text)
        return text
    
    def _normalize_line_breaks(self, text: str) -> str:
        """Normalize line breaks and paragraph spacing"""
        # Remove trailing spaces
        lines = [line.rstrip() for line in text.split('\n')]
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
    
    def _fix_capitalization(self, text: str) -> str:
        """Fix obvious capitalization errors in titles"""
        # Fix all-caps words that should be title case (except acronyms)
        def fix_word(match):
            word = match.group(0)
            # Keep acronyms (2-4 letters all caps)
            if len(word) <= 4:
                return word
            # Title case for longer words
            return word.title()
        
        # Fix lines that are entirely uppercase (likely titles)
        lines = text.split('\n')
        fixed_lines = []
        for line in lines:
            # If line is all uppercase and longer than 10 chars, it's likely a title
            if line.isupper() and len(line.strip()) > 10:
                # Keep first word capitalized, rest title case
                words = line.split()
                if words:
                    fixed_line = ' '.join([words[0]] + [w.title() if len(w) > 4 else w for w in words[1:]])
                    fixed_lines.append(fixed_line)
                else:
                    fixed_lines.append(line)
            else:
                fixed_lines.append(line)
        
        return '\n'.join(fixed_lines)
    
    def _calculate_improvement_score(self, original: str, cleaned: str) -> float:
        """Calculate how much the text was improved (0-100)"""
        if original == cleaned:
            return 0.0
        
        # Count corrections made
        corrections = len(original) - len(cleaned) if len(original) > len(cleaned) else len(cleaned) - len(original)
        improvement = min(100, (corrections / len(original)) * 100)
        
        return round(improvement, 2)
    
    def format_for_display(self, cleaned_text: str) -> str:
        """
        Format cleaned text for optimal display
        Adds visual structure markers
        """
        lines = cleaned_text.split('\n')
        formatted_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                formatted_lines.append('')
                continue
            
            # Detect and format section headers
            if re.match(r'^(ARTICLE|CLAUSE|SECTION|TITRE)\s+\d+', line, re.IGNORECASE):
                formatted_lines.append(f"\n{'='*60}")
                formatted_lines.append(f"  {line}")
                formatted_lines.append(f"{'='*60}\n")
            # Detect and format party names (all caps lines)
            elif line.isupper() and len(line) > 15:
                formatted_lines.append(f"\n--- {line} ---\n")
            else:
                formatted_lines.append(line)
        
        return '\n'.join(formatted_lines)


# Singleton instance
ocr_cleaner = OCRTextCleaner()
