import requests
import json

# Test contract
contract_text = """CONTRAT DE BAIL D'HABITATION

ENTRE LES SOUSSIGNÉS :
Le Bailleur : Monsieur Jean DUPONT
Le Preneur : Madame Marie MARTIN

ARTICLE 1 : LOYER
Le loyer mensuel est fixé à 850 euros.

ARTICLE 2 : DÉPÔT DE GARANTIE
Un dépôt de garantie de 1700 euros est versé.

ARTICLE 3 : DURÉE
Le bail est conclu pour 3 ans à compter du 1er février 2024.

ARTICLE 4 : RÉSILIATION
Le locataire peut résilier avec un préavis de 3 mois."""

# Call API
url = "http://localhost:8000/analyze"
payload = {
    "text": contract_text,
    "contract_type": "auto"
}

print("📤 Calling API...")
response = requests.post(url, json=payload)

print(f"\n📊 Status Code: {response.status_code}")

# Save to file
with open('api_response_full.json', 'w', encoding='utf-8') as f:
    json.dump(response.json(), f, indent=2, ensure_ascii=False)

print("\n✅ Response saved to api_response_full.json")
print(f"\n📄 Response Preview:")
data = response.json()
print(f"  - contract_type: {data.get('contract_type')}")
print(f"  - total_clauses: {data.get('metadata', {}).get('total_clauses')}")
print(f"  - high_risk_count: {data.get('metadata', {}).get('high_risk_count')}")
print(f"  - clauses count: {len(data.get('clauses', []))}")
print(f"  - risks count: {len(data.get('risks', []))}")
