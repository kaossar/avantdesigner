"""
Unit tests for smart chunker
"""

import pytest
from preprocessing.chunker import SmartChunker

class TestSmartChunker:
    """Test suite for smart chunking"""
    
    @pytest.fixture
    def chunker(self):
        """Fixture for SmartChunker instance"""
        return SmartChunker(contract_type="Bail d'habitation", max_chunk_size=1000)
    
    def test_chunk_by_articles(self, chunker):
        """Test chunking by article markers"""
        text = """
Article 1
This is the first article content.

Article 2
This is the second article content.

Article 3
This is the third article content.
"""
        chunks = chunker.chunk(text)
        
        assert len(chunks) >= 3
        assert chunks[0]["clause_number"] == 1
        assert "Article 1" in chunks[0]["text"]
        assert chunks[0]["context"] == "[Contrat: Bail d'habitation, Clause 1, Type: general]"
    
    def test_chunk_by_paragraphs_fallback(self, chunker):
        """Test fallback to paragraph chunking"""
        text = """
This is the first paragraph with enough content to be considered.

This is the second paragraph also with sufficient content.

This is the third paragraph.
"""
        chunks = chunker.chunk(text)
        
        assert len(chunks) >= 2
        assert all("clause_number" in chunk for chunk in chunks)
    
    def test_detect_financial_clause(self, chunker):
        """Test financial clause detection"""
        text = "Article 1\nLe loyer mensuel est de 800 euros."
        chunks = chunker.chunk(text)
        
        assert chunks[0]["type"] == "financial"
    
    def test_detect_termination_clause(self, chunker):
        """Test termination clause detection"""
        text = "Article 5\nLa résiliation du contrat peut intervenir avec préavis."
        chunks = chunker.chunk(text)
        
        assert chunks[0]["type"] == "termination"
    
    def test_detect_duration_clause(self, chunker):
        """Test duration clause detection"""
        text = "Article 2\nLa durée du bail est de 12 mois."
        chunks = chunker.chunk(text)
        
        assert chunks[0]["type"] == "duration"
    
    def test_detect_guarantee_clause(self, chunker):
        """Test guarantee clause detection"""
        text = "Article 3\nUn dépôt de garantie de 800 euros est demandé."
        chunks = chunker.chunk(text)
        
        assert chunks[0]["type"] == "guarantee"
    
    def test_chunk_size_limit(self, chunker):
        """Test chunk size limiting"""
        long_text = "Article 1\n" + "A" * 2000  # Text longer than max_chunk_size
        chunks = chunker.chunk(long_text)
        
        assert len(chunks[0]["text"]) <= 1000 + 3  # +3 for "..."
        assert chunks[0]["text"].endswith("...")
    
    def test_chunk_metadata(self, chunker):
        """Test chunk metadata completeness"""
        text = "Article 1\nSome content here."
        chunks = chunker.chunk(text)
        
        chunk = chunks[0]
        assert "text" in chunk
        assert "context" in chunk
        assert "clause_number" in chunk
        assert "type" in chunk
        assert "char_count" in chunk
        assert chunk["char_count"] > 0
    
    def test_empty_text(self, chunker):
        """Test empty text handling"""
        chunks = chunker.chunk("")
        
        # Should return empty list or handle gracefully
        assert isinstance(chunks, list)
    
    def test_clause_patterns(self, chunker):
        """Test different clause patterns"""
        patterns = [
            "Article 1.1\nContent",
            "ARTICLE I\nContent",
            "Clause 5\nContent"
        ]
        
        for pattern in patterns:
            chunks = chunker.chunk(pattern)
            assert len(chunks) >= 1, f"Failed for pattern: {pattern}"
