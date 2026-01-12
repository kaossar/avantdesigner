"""
Unit tests for file validator
"""

import pytest
from utils.validator import validate_file, FILE_LIMITS

class TestFileValidator:
    """Test suite for file validation"""
    
    def test_valid_txt_file(self):
        """Test valid TXT file"""
        result = validate_file(
            file_path="contract.txt",
            file_size=1024,  # 1 KB
            mime_type="text/plain"
        )
        assert result["valid"] is True
        assert result["error"] is None
    
    def test_valid_pdf_file(self):
        """Test valid PDF file"""
        result = validate_file(
            file_path="contract.pdf",
            file_size=5 * 1024 * 1024,  # 5 MB
            mime_type="application/pdf"
        )
        assert result["valid"] is True
        assert result["error"] is None
    
    def test_file_too_large(self):
        """Test file exceeding size limit"""
        result = validate_file(
            file_path="huge.pdf",
            file_size=60 * 1024 * 1024,  # 60 MB (over 50 MB limit)
            mime_type="application/pdf"
        )
        assert result["valid"] is False
        assert "trop volumineux" in result["error"]
    
    def test_invalid_mime_type(self):
        """Test unsupported MIME type"""
        result = validate_file(
            file_path="document.docx",
            file_size=1024,
            mime_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
        assert result["valid"] is False
        assert "non supporté" in result["error"]
    
    def test_invalid_extension(self):
        """Test unsupported file extension"""
        result = validate_file(
            file_path="file.exe",
            file_size=1024,
            mime_type="application/octet-stream"
        )
        assert result["valid"] is False
        assert "Extension non supportée" in result["error"]
    
    def test_edge_case_max_size(self):
        """Test file at exact size limit"""
        result = validate_file(
            file_path="contract.pdf",
            file_size=FILE_LIMITS["max_size"],  # Exactly 50 MB
            mime_type="application/pdf"
        )
        assert result["valid"] is True
    
    def test_image_files(self):
        """Test valid image files"""
        for ext, mime in [("jpg", "image/jpeg"), ("png", "image/png"), ("tiff", "image/tiff")]:
            result = validate_file(
                file_path=f"scan.{ext}",
                file_size=1024,
                mime_type=mime
            )
            assert result["valid"] is True, f"Failed for {ext}"
