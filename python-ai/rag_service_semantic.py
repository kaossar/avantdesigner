"""
Semantic RAG Service - Production-Ready with Hugging Face

Uses sentence-transformers + FAISS for semantic search over legal knowledge base.
Model: paraphrase-multilingual-mpnet-base-v2 (optimized for French)
"""

import os
import json
import pickle
import numpy as np
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class SemanticRAGService:
    """
    Semantic RAG Service using Hugging Face sentence-transformers + FAISS
    
    Features:
    - Semantic embeddings (768 dimensions)
    - FAISS vector index for fast search
    - Multilingual model optimized for French
    - Caching for performance
    """
    
    def __init__(self, knowledge_base_path: str = "knowledge_base", cache_dir: str = "rag_cache"):
        """Initialize semantic RAG service"""
        self.kb_path = knowledge_base_path
        self.cache_dir = cache_dir
        self.model = None
        self.index = None
        self.articles = []
        
        # Create cache directory
        os.makedirs(self.cache_dir, exist_ok=True)
        
        # Load or create embeddings
        self._initialize()
    
    def _initialize(self):
        """Initialize model, articles, and FAISS index"""
        logger.info("🚀 Initializing Semantic RAG Service...")
        
        try:
            # Import here to avoid errors if not installed
            from sentence_transformers import SentenceTransformer
            import faiss
            
            # Load model
            logger.info("📥 Loading sentence-transformers model...")
            self.model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')
            logger.info("✅ Model loaded successfully")
            
            # Load articles
            self.articles = self._get_complete_knowledge_base()
            logger.info(f"📚 Loaded {len(self.articles)} legal articles")
            
            # Load or create embeddings
            embeddings_path = os.path.join(self.cache_dir, "embeddings.pkl")
            index_path = os.path.join(self.cache_dir, "faiss.index")
            
            if os.path.exists(embeddings_path) and os.path.exists(index_path):
                logger.info("📂 Loading cached embeddings and index...")
                with open(embeddings_path, 'rb') as f:
                    embeddings = pickle.load(f)
                self.index = faiss.read_index(index_path)
                logger.info("✅ Loaded from cache")
            else:
                logger.info("🔨 Creating embeddings (first time, may take 30s)...")
                embeddings = self._create_embeddings()
                
                logger.info("🔨 Building FAISS index...")
                self.index = self._build_faiss_index(embeddings)
                
                # Save to cache
                logger.info("💾 Saving to cache...")
                with open(embeddings_path, 'wb') as f:
                    pickle.dump(embeddings, f)
                faiss.write_index(self.index, index_path)
                logger.info("✅ Cache saved")
            
            logger.info("🎉 Semantic RAG Service ready!")
            
        except ImportError as e:
            logger.error(f"❌ Hugging Face libraries not installed: {e}")
            logger.error("   Run: pip install sentence-transformers faiss-cpu")
            raise
    
    def _get_complete_knowledge_base(self) -> List[Dict[str, Any]]:
        """Complete knowledge base - 35 articles"""
        # Import from existing rag_service to avoid duplication
        from rag_service import LegalRAGService
        temp_service = LegalRAGService()
        return temp_service.articles
    
    def _create_embeddings(self) -> np.ndarray:
        """Create embeddings for all articles"""
        # Combine article content for embedding
        texts = []
        for article in self.articles:
            # Combine title + content for better semantic understanding
            text = f"{article['title']}: {article['content']}"
            texts.append(text)
        
        # Encode with sentence-transformers
        embeddings = self.model.encode(
            texts,
            show_progress_bar=True,
            convert_to_numpy=True,
            normalize_embeddings=True  # For cosine similarity
        )
        
        return embeddings
    
    def _build_faiss_index(self, embeddings: np.ndarray):
        """Build FAISS index for fast similarity search"""
        import faiss
        
        # Get embedding dimension
        dimension = embeddings.shape[1]
        
        # Create index (L2 distance, equivalent to cosine with normalized vectors)
        index = faiss.IndexFlatL2(dimension)
        
        # Add embeddings
        index.add(embeddings.astype('float32'))
        
        return index
    
    def search_relevant_articles(self, query: str, clause_type: str = None, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Semantic search for relevant legal articles
        
        Args:
            query: Search query (clause text)
            clause_type: Type of clause (optional, for boosting)
            top_k: Number of results to return
        
        Returns:
            List of relevant articles with semantic scores
        """
        # Encode query
        query_embedding = self.model.encode(
            [query],
            convert_to_numpy=True,
            normalize_embeddings=True
        )
        
        # Search FAISS index
        distances, indices = self.index.search(query_embedding.astype('float32'), top_k * 2)
        
        # Build results
        results = []
        for i, (distance, idx) in enumerate(zip(distances[0], indices[0])):
            article = self.articles[idx].copy()
            
            # Convert L2 distance to similarity score (0-100)
            # Lower distance = higher similarity
            similarity = max(0, 100 - (distance * 50))
            
            # Boost score if category matches
            if clause_type and article.get('category') == clause_type:
                similarity += 10
            
            article['relevance_score'] = similarity
            article['semantic_distance'] = float(distance)
            results.append(article)
        
        # Sort by relevance and return top_k
        results.sort(key=lambda x: x['relevance_score'], reverse=True)
        return results[:top_k]
    
    def enrich_clause_analysis(self, clause_text: str, clause_type: str) -> Dict[str, Any]:
        """
        Enrich clause analysis with semantic legal references
        
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
                "summary": article["content"][:150] + "...",
                "relevance": f"{article['relevance_score']:.1f}%"
            })
        
        # Generate legal context
        main_ref = relevant_articles[0]
        legal_context = f"Selon {main_ref['source']} {main_ref['article']} ({main_ref['title']}): {main_ref['content'][:200]}..."
        
        return {
            "has_references": True,
            "references": references,
            "legal_context": legal_context,
            "search_method": "semantic"  # Indicate semantic search was used
        }

# Singleton instance
_semantic_rag_service = None

def get_semantic_rag_service() -> SemanticRAGService:
    """Get or create semantic RAG service singleton"""
    global _semantic_rag_service
    if _semantic_rag_service is None:
        _semantic_rag_service = SemanticRAGService()
    return _semantic_rag_service
