"""
Smart chunking for contract analysis
Chunks by clause/article with context
"""

import re
from typing import List, Dict

class SmartChunker:
    """Professional chunking for contract analysis"""
    
    def __init__(self, contract_type: str = "auto", max_chunk_size: int = 1000):
        self.contract_type = contract_type
        self.max_chunk_size = max_chunk_size
    
    def chunk(self, text: str) -> List[Dict]:
        """
        Smart chunking by clause with context
        
        Args:
            text: Cleaned contract text
        
        Returns:
            List of {
                "text": chunk text,
                "context": context string,
                "clause_number": int,
                "type": clause type,
                "char_count": int
            }
        """
        # Try to detect articles/clauses
        chunks = self._chunk_by_articles(text)
        
        if not chunks or len(chunks) < 2:
            # Fallback to paragraph chunking
            chunks = self._chunk_by_paragraphs(text)
        
        # Add context and metadata to each chunk
        enriched_chunks = []
        for i, chunk_text in enumerate(chunks):
            # Limit chunk size
            if len(chunk_text) > self.max_chunk_size:
                chunk_text = chunk_text[:self.max_chunk_size] + "..."
            
            clause_type = self._detect_clause_type(chunk_text)
            
            enriched_chunks.append({
                "text": chunk_text,
                "context": f"[Contrat: {self.contract_type}, Clause {i+1}, Type: {clause_type}]",
                "clause_number": i + 1,
                "type": clause_type,
                "char_count": len(chunk_text)
            })
        
        return enriched_chunks
    
    def _chunk_by_articles(self, text: str) -> List[str]:
        """
        Chunk by Article/Clause markers
        Patterns: "Article 1", "ARTICLE I", "Clause 1"
        """
        patterns = [
            r'(Article\s+\d+(?:\.\d+)?)',
            r'(ARTICLE\s+[IVX]+)',
            r'(Clause\s+\d+)'
        ]
        
        # Try each pattern
        for pattern in patterns:
            if re.search(pattern, text):
                chunks = re.split(pattern, text)
                result = []
                
                # Recombine title + content
                for i in range(1, len(chunks), 2):
                    if i+1 < len(chunks):
                        result.append(chunks[i] + ' ' + chunks[i+1])
                
                if result:
                    return result
        
        return []
    
    def _chunk_by_paragraphs(self, text: str) -> List[str]:
        """
        Fallback: chunk by paragraphs
        Filter out very short paragraphs
        """
        paragraphs = text.split('\n\n')
        return [p.strip() for p in paragraphs if len(p.strip()) > 50]
    
    def _detect_clause_type(self, chunk: str) -> str:
        """
        Detect clause type from content keywords
        """
        chunk_lower = chunk.lower()
        
        # Financial clauses
        if any(kw in chunk_lower for kw in ['loyer', 'montant', 'prix', 'paiement', 'euros', '€']):
            return 'financial'
        
        # Termination clauses
        elif any(kw in chunk_lower for kw in ['résiliation', 'rupture', 'fin', 'terme']):
            return 'termination'
        
        # Duration clauses
        elif any(kw in chunk_lower for kw in ['durée', 'période', 'mois', 'ans']):
            return 'duration'
        
        # Guarantee/deposit clauses
        elif any(kw in chunk_lower for kw in ['caution', 'garantie', 'dépôt']):
            return 'guarantee'
        
        # Obligations
        elif any(kw in chunk_lower for kw in ['obligation', 'engagement', 'doit', 'devra']):
            return 'obligation'
        
        # General
        else:
            return 'general'
