import requests
import json

# Risky contract with abusive clauses
contract_text = """CONTRAT DE BAIL D'HABITATION

ENTRE LES SOUSSIGNÉS :
Le Bailleur : Monsieur Jean DUPONT
Le Preneur : Madame Marie MARTIN

ARTICLE 1 : LOYER
Le loyer mensuel est fixé à 2500 euros, avec une pénalité de 500 euros en cas de retard de paiement.

ARTICLE 2 : DÉPÔT DE GARANTIE
Un dépôt de garantie de 7500 euros (3 mois de loyer) est versé. Ce montant est non conforme à la loi.

ARTICLE 3 : ACCÈS AUX LOCAUX
Le bailleur se réserve le droit d'entrer dans les locaux à tout moment sans préavis. Cette clause est abusive.

ARTICLE 4 : RÉSILIATION UNILATÉRALE
Le bailleur peut résilier le contrat de manière unilatérale sans préavis en cas de simple retard de paiement.

ARTICLE 5 : TRAVAUX
Tous les travaux, même structurels, sont à la charge exclusive du locataire. Cette clause est illégale.

ARTICLE 6 : INTERDICTION
Il est strictement interdit au locataire de recevoir des visiteurs après 20h."""

# Call API
url = "http://localhost:8000/analyze"
payload = {
    "text": contract_text,
    "contract_type": "auto"
}

print("📤 Calling API with RISKY contract...")
response = requests.post(url, json=payload)

print(f"\n📊 Status Code: {response.status_code}")

# Save to file
with open('api_response_risky.json', 'w', encoding='utf-8') as f:
    json.dump(response.json(), f, indent=2, ensure_ascii=False)

print("\n✅ Response saved to api_response_risky.json")
print(f"\n📄 Response Summary:")
data = response.json()
print(f"  - contract_type: {data.get('contract_type')}")
print(f"  - total_clauses: {data.get('metadata', {}).get('total_clauses')}")
print(f"  - high_risk_count: {data.get('metadata', {}).get('high_risk_count')}")
print(f"  - medium_risk_count: {data.get('metadata', {}).get('medium_risk_count')}")
print(f"  - clauses count: {len(data.get('clauses', []))}")
print(f"  - risks count: {len(data.get('risks', []))}")
print(f"  - global_score: {data.get('score', {}).get('global')}")

print(f"\n⚠️ Detected Risks:")
for i, risk in enumerate(data.get('risks', []), 1):
    print(f"  {i}. Clause {risk['clause_number']} - {risk['severity'].upper()}: {risk['issue'][:80]}...")
