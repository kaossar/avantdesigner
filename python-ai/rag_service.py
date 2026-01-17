"""
RAG Service - Retrieval-Augmented Generation for Legal References

This module provides semantic search over legal knowledge base
to enrich contract analysis with relevant legal references.
"""

import os
import json
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class LegalRAGService:
    """
    Legal RAG Service for semantic search over legal documents
    
    Features:
    - Load legal knowledge base (markdown files)
    - Parse articles and create searchable chunks
    - Semantic search for relevant legal references
    - Enrich analysis with legal context
    """
    
    def __init__(self, knowledge_base_path: str = "knowledge_base"):
        """Initialize RAG service with knowledge base path"""
        self.kb_path = knowledge_base_path
        self.articles = []
        self.load_knowledge_base()
    
    def load_knowledge_base(self):
        """Load all legal documents from knowledge base"""
        logger.info(f"📚 Loading legal knowledge base from {self.kb_path}...")
        
        # For MVP: Simple keyword-based search
        # Future: Use sentence-transformers + FAISS for semantic search
        
        self.articles = [
            # Loi 89-462 - Baux d'habitation
            {
                "source": "Loi 89-462",
                "article": "Article 22",
                "title": "Dépôt de garantie",
                "content": "Le dépôt de garantie ne peut excéder un mois de loyer en principal (hors charges) pour les locations vides. Pour les locations meublées, il ne peut excéder deux mois de loyer.",
                "keywords": ["dépôt", "garantie", "caution", "mois", "loyer"],
                "category": "financial"
            },
            {
                "source": "Loi 89-462",
                "article": "Article 3",
                "title": "Durée du bail",
                "content": "Le contrat de location est conclu pour une durée minimale de trois ans lorsque le bailleur est une personne physique et de six ans lorsqu'il est une personne morale.",
                "keywords": ["durée", "bail", "trois ans", "six ans", "contrat"],
                "category": "duration"
            },
            {
                "source": "Loi 89-462",
                "article": "Article 5",
                "title": "Préavis du locataire",
                "content": "Le locataire peut résilier le contrat à tout moment, sous réserve de respecter un préavis de trois mois. Ce délai est réduit à un mois dans certains cas (mutation, perte d'emploi, etc.).",
                "keywords": ["préavis", "résiliation", "trois mois", "un mois", "locataire"],
                "category": "termination"
            },
            {
                "source": "Loi 89-462",
                "article": "Article 6",
                "title": "Clauses abusives interdites",
                "content": "Sont réputées non écrites les clauses interdisant au locataire de recevoir des visiteurs, imposant une assurance désignée, ou permettant au bailleur d'entrer sans préavis.",
                "keywords": ["clause", "abusive", "interdite", "non écrite", "visiteur", "assurance"],
                "category": "general"
            },
            {
                "source": "Loi 89-462",
                "article": "Article 25",
                "title": "Travaux",
                "content": "Les grosses réparations (gros murs, toiture, structure) sont à la charge exclusive du bailleur. Les réparations locatives (entretien courant) sont à la charge du locataire.",
                "keywords": ["travaux", "réparation", "charge", "bailleur", "locataire", "entretien"],
                "category": "general"
            },
            # Code Civil
            {
                "source": "Code Civil",
                "article": "Article 606",
                "title": "Grosses réparations",
                "content": "Les grosses réparations sont celles des gros murs et des voûtes, le rétablissement des poutres et des couvertures entières. Toutes les autres réparations sont d'entretien.",
                "keywords": ["grosse", "réparation", "mur", "toiture", "entretien"],
                "category": "general"
            },
            {
                "source": "Code Civil",
                "article": "Article 1171",
                "title": "Clauses abusives",
                "content": "Dans un contrat d'adhésion, toute clause qui crée un déséquilibre significatif entre les droits et obligations des parties au contrat est réputée non écrite.",
                "keywords": ["clause", "abusive", "déséquilibre", "non écrite"],
                "category": "general"
            },
            {
                "source": "Code Civil",
                "article": "Article 1719",
                "title": "Obligations du bailleur",
                "content": "Le bailleur est obligé de délivrer au preneur la chose louée, de l'entretenir en état de servir à l'usage pour lequel elle a été louée, et d'en faire jouir paisiblement le preneur.",
                "keywords": ["obligation", "bailleur", "délivrance", "entretien", "jouissance"],
                "category": "general"
            }
        ]
        
        logger.info(f"✅ Loaded {len(self.articles)} legal articles")
    
    def search_relevant_articles(self, query: str, clause_type: str = None, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Search for relevant legal articles based on query
        
        Args:
            query: Search query (clause text)
            clause_type: Type of clause (financial, termination, etc.)
            top_k: Number of results to return
        
        Returns:
            List of relevant articles with scores
        """
        query_lower = query.lower()
        results = []
        
        for article in self.articles:
            # Simple keyword-based scoring (MVP)
            # Future: Use semantic embeddings
            score = 0
            
            # Match keywords
            for keyword in article["keywords"]:
                if keyword in query_lower:
                    score += 2
            
            # Match category
            if clause_type and article["category"] == clause_type:
                score += 3
            
            # Match article content
            if any(word in article["content"].lower() for word in query_lower.split()):
                score += 1
            
            if score > 0:
                results.append({
                    **article,
                    "relevance_score": score
                })
        
        # Sort by relevance and return top_k
        results.sort(key=lambda x: x["relevance_score"], reverse=True)
        return results[:top_k]
    
    def enrich_clause_analysis(self, clause_text: str, clause_type: str) -> Dict[str, Any]:
        """
        Enrich clause analysis with relevant legal references
        
        Args:
            clause_text: Text of the clause
            clause_type: Type of clause
        
        Returns:
            Dictionary with legal references and context
        """
        relevant_articles = self.search_relevant_articles(clause_text, clause_type, top_k=2)
        
        if not relevant_articles:
            return {
                "has_references": False,
                "references": [],
                "legal_context": "Aucune référence légale spécifique trouvée."
            }
        
        references = []
        for article in relevant_articles:
            references.append({
                "source": article["source"],
                "article": article["article"],
                "title": article["title"],
                "summary": article["content"][:150] + "..."
            })
        
        # Generate legal context
        main_ref = relevant_articles[0]
        legal_context = f"Selon {main_ref['source']} {main_ref['article']} ({main_ref['title']}): {main_ref['content'][:200]}..."
        
        return {
            "has_references": True,
            "references": references,
            "legal_context": legal_context
        }

# Singleton instance
_rag_service = None

def get_rag_service() -> LegalRAGService:
    """Get or create RAG service singleton"""
    global _rag_service
    if _rag_service is None:
        _rag_service = LegalRAGService()
    return _rag_service
