import requests
import json

# Test contract with specific legal references
contract_text = """CONTRAT DE BAIL D'HABITATION

ENTRE LES SOUSSIGNÉS :
Le Bailleur : Monsieur Jean DUPONT
Le Preneur : Madame Marie MARTIN

ARTICLE 1 : LOYER
Le loyer mensuel est fixé à 850 euros, payable le 1er de chaque mois.

ARTICLE 2 : DÉPÔT DE GARANTIE
Un dépôt de garantie de 850 euros (1 mois de loyer) est versé à la signature.

ARTICLE 3 : DURÉE
Le bail est conclu pour une durée de 3 ans à compter du 1er février 2024.

ARTICLE 4 : RÉSILIATION
Le locataire peut résilier avec un préavis de 3 mois."""

# Call API
url = "http://localhost:8000/analyze"
payload = {
    "text": contract_text,
    "contract_type": "auto"
}

print("📤 Calling API with RAG-enabled contract...")
response = requests.post(url, json=payload)

print(f"\n📊 Status Code: {response.status_code}")

# Save to file
with open('api_response_rag.json', 'w', encoding='utf-8') as f:
    json.dump(response.json(), f, indent=2, ensure_ascii=False)

print("\n✅ Response saved to api_response_rag.json")
print(f"\n📄 RAG Enrichment Check:")
data = response.json()

# Check if legal references are present
clauses_with_refs = 0
total_refs = 0

for clause in data.get('clauses', []):
    refs = clause.get('legal_references', [])
    if refs:
        clauses_with_refs += 1
        total_refs += len(refs)
        print(f"\n  Clause {clause['clause_number']} ({clause['clause_type']}):")
        print(f"    Legal context: {clause.get('legal_context', 'N/A')[:100]}...")
        for ref in refs:
            print(f"    → {ref['source']} {ref['article']}: {ref['title']}")

print(f"\n📊 RAG Statistics:")
print(f"  - Total clauses: {len(data.get('clauses', []))}")
print(f"  - Clauses with legal refs: {clauses_with_refs}")
print(f"  - Total legal references: {total_refs}")
print(f"  - Average refs per clause: {total_refs / len(data.get('clauses', [])) if data.get('clauses') else 0:.1f}")
