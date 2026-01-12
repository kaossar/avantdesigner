"""
Professional text cleaning and normalization
Removes headers, footers, page numbers, normalizes whitespace
"""

import re
from typing import Dict, Any

class TextCleaner:
    """Professional text cleaning for contract analysis"""
    
    def clean(self, text: str) -> Dict[str, Any]:
        """
        Clean and normalize text
        
        Args:
            text: Raw extracted text
        
        Returns:
            {
                "text": cleaned text,
                "metadata": {
                    "original_length": int,
                    "cleaned_length": int,
                    "reduction_percent": float
                }
            }
        """
        original_length = len(text)
        
        # 1. Remove headers/footers (repeated patterns)
        text = self._remove_headers_footers(text)
        
        # 2. Remove page numbers
        text = re.sub(r'Page\s+\d+(/\d+)?', '', text, flags=re.IGNORECASE)
        text = re.sub(r'\d+\s*/\s*\d+', '', text)
        
        # 3. Normalize whitespace
        text = re.sub(r'[ \t]+', ' ', text)  # Multiple spaces to single
        text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)  # Multiple newlines to double
        
        # 4. Remove signatures/stamps patterns
        text = re.sub(r'Signature\s*:.*', '', text, flags=re.IGNORECASE)
        text = re.sub(r'Cachet\s*:.*', '', text, flags=re.IGNORECASE)
        
        # 5. Normalize quotes and apostrophes
        text = text.replace('"', '"').replace('"', '"')
        text = text.replace(''', "'").replace(''', "'")
        
        # 6. Remove excessive blank lines at start/end
        cleaned_text = text.strip()
        
        # Calculate reduction
        cleaned_length = len(cleaned_text)
        reduction = 0 if original_length == 0 else round((1 - cleaned_length/original_length) * 100, 2)
        
        return {
            "text": cleaned_text,
            "metadata": {
                "original_length": original_length,
                "cleaned_length": cleaned_length,
                "reduction_percent": reduction
            }
        }
    
    def _remove_headers_footers(self, text: str) -> str:
        """
        Remove repeated headers/footers
        Lines that appear more than 3 times are likely headers/footers
        """
        lines = text.split('\n')
        
        # Count line occurrences
        line_counts = {}
        for line in lines:
            stripped = line.strip()
            if len(stripped) > 10:  # Ignore very short lines
                line_counts[stripped] = line_counts.get(stripped, 0) + 1
        
        # Find repeated lines (appear more than 3 times)
        repeated = {line for line, count in line_counts.items() if count > 3}
        
        # Remove repeated lines
        cleaned_lines = [line for line in lines if line.strip() not in repeated]
        
        return '\n'.join(cleaned_lines)
