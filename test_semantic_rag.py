"""
Test script for Semantic RAG Service
"""

import sys
sys.path.append('python-ai')

from rag_service_semantic import get_semantic_rag_service

print("🧪 Testing Semantic RAG Service...")
print("=" * 60)

# Initialize service (will create embeddings first time)
print("\n1️⃣ Initializing service...")
rag = get_semantic_rag_service()

# Test queries
test_queries = [
    ("dépôt de garantie", "financial"),
    ("caution", "financial"),  # Synonym test
    ("travaux structure", "general"),
    ("réparations importantes", "general"),  # Synonym test
    ("préavis locataire", "termination"),
]

print("\n2️⃣ Testing semantic search...")
print("=" * 60)

for query, clause_type in test_queries:
    print(f"\n📝 Query: '{query}' (type: {clause_type})")
    print("-" * 60)
    
    results = rag.search_relevant_articles(query, clause_type, top_k=2)
    
    for i, article in enumerate(results, 1):
        print(f"\n  {i}. {article['source']} {article['article']}: {article['title']}")
        print(f"     Relevance: {article['relevance_score']:.1f}%")
        print(f"     Distance: {article['semantic_distance']:.4f}")
        print(f"     Content: {article['content'][:100]}...")

print("\n" + "=" * 60)
print("✅ Semantic RAG Service test complete!")
