"""
Unit tests for text cleaner
"""

import pytest
from preprocessing.cleaner import TextCleaner

class TestTextCleaner:
    """Test suite for text cleaning"""
    
    @pytest.fixture
    def cleaner(self):
        """Fixture for TextCleaner instance"""
        return TextCleaner()
    
    def test_remove_page_numbers(self, cleaner):
        """Test page number removal"""
        text = "Contract text here\nPage 1\nMore text\nPage 2/10\nEnd"
        result = cleaner.clean(text)
        
        assert "Page 1" not in result["text"]
        assert "Page 2/10" not in result["text"]
        assert "Contract text here" in result["text"]
    
    def test_normalize_whitespace(self, cleaner):
        """Test whitespace normalization"""
        text = "Text  with    multiple   spaces\n\n\n\nAnd many newlines"
        result = cleaner.clean(text)
        
        # Multiple spaces should become single
        assert "  " not in result["text"]
        # Multiple newlines should become double
        assert "\n\n\n" not in result["text"]
    
    def test_remove_signatures(self, cleaner):
        """Test signature removal"""
        text = "Contract content\nSignature: John Doe\nMore content"
        result = cleaner.clean(text)
        
        assert "Signature:" not in result["text"]
        assert "Contract content" in result["text"]
    
    def test_normalize_quotes(self, cleaner):
        """Test quote normalization"""
        text = "Text with smart quotes and apostrophes"
        result = cleaner.clean(text)
        
        assert "smart quotes" in result["text"]
    
    def test_remove_headers_footers(self, cleaner):
        """Test repeated header/footer removal"""
        # Test with 5 occurrences
        text_repeated = "\n".join(["Header Line"] * 5 + ["Content"])
        result = cleaner.clean(text_repeated)
        
        # Header should be removed (threshold > 3)
        assert result["text"].count("Header Line") < 5
    
    def test_metadata_calculation(self, cleaner):
        """Test metadata calculation"""
        text = "A" * 1000
        result = cleaner.clean(text)
        
        assert "metadata" in result
        assert result["metadata"]["original_length"] == 1000
        assert result["metadata"]["cleaned_length"] > 0
        assert "reduction_percent" in result["metadata"]
    
    def test_empty_text(self, cleaner):
        """Test empty text handling"""
        result = cleaner.clean("")
        
        assert result["text"] == ""
        assert result["metadata"]["original_length"] == 0
        assert result["metadata"]["cleaned_length"] == 0
    
    def test_strip_whitespace(self, cleaner):
        """Test leading/trailing whitespace removal"""
        text = "   \n\n  Contract text  \n\n  "
        result = cleaner.clean(text)
        
        assert result["text"] == "Contract text"
