"""
Test End-to-End Complet - AvantDeSigner Pipeline
Tests l'ensemble du système : API, RAG, PDF Export
"""

import requests
import json
import time
from pathlib import Path

# Configuration
API_URL = "http://localhost:8000"
TEST_DATA_DIR = Path("test_data")
TEST_OUTPUT_DIR = Path("test_output")

# Créer directories si nécessaire
TEST_OUTPUT_DIR.mkdir(exist_ok=True)

# Exemple de contrat de bail
BAIL_EXEMPLE = """
CONTRAT DE LOCATION

Entre les soussignés :

Monsieur Jean DUPONT, propriétaire
Et Madame Marie MARTIN, locataire

Article 1 - Objet
Le bailleur loue au locataire un appartement de 50m² situé au 10 rue de la Paix, 75001 Paris.

Article 2 - Durée
Le bail est conclu pour une durée de 3 ans à compter du 1er janvier 2024.

Article 3 - Loyer
Le loyer mensuel est fixé à 1200 euros, charges comprises.
Le loyer sera payable le 1er de chaque mois.

Article 4 - Dépôt de garantie
Un dépôt de garantie d'un montant de 1200 euros est versé à la signature du bail.

Article 5 - Préavis
Le locataire peut résilier le bail à tout moment avec un préavis de 3 mois.

Article 6 - Travaux
Le locataire s'engage à entretenir le logement en bon état.
Les grosses réparations restent à la charge du propriétaire.

Article 7 - Clause résolutoire
En cas de non-paiement du loyer, le bail sera résilié de plein droit.
"""

def print_section(title):
    """Print section header"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def test_health_check():
    """Test 1: Health Check API"""
    print_section("1️⃣ TEST HEALTH CHECK")
    
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        
        print(f"✅ API Status: {data.get('status')}")
        print(f"   Service: {data.get('service')}")
        print(f"   Version: {data.get('version')}")
        return True
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_contract_analysis():
    """Test 2: Contract Analysis with RAG"""
    print_section("2️⃣ TEST ANALYSE CONTRAT + RAG")
    
    try:
        start_time = time.time()
        
        response = requests.post(
            f"{API_URL}/analyze",
            json={
                "text": BAIL_EXEMPLE,
                "contract_type": "auto"
            },
            timeout=60
        )
        
        duration = time.time() - start_time
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        result = response.json()
        
        # Validation basique
        assert "contract_type" in result, "Missing contract_type"
        assert "clauses" in result, "Missing clauses"
        assert "risks" in result, "Missing risks"
        assert "score" in result, "Missing score"
        
        # Stats
        clauses = result.get("clauses", [])
        risks = result.get("risks", [])
        
        print(f"✅ Analyse terminée en {duration:.2f}s")
        print(f"   Type détecté: {result.get('contract_type')}")
        print(f"   Clauses analysées: {len(clauses)}")
        print(f"   Risques détectés: {len(risks)}")
        
        # Vérifier références légales RAG
        clauses_with_refs = [c for c in clauses if c.get('legal_references')]
        total_refs = sum(len(c.get('legal_references', [])) for c in clauses)
        avg_refs = total_refs / len(clauses) if clauses else 0
        
        print(f"\n📚 Références Légales (RAG):")
        print(f"   Clauses avec références: {len(clauses_with_refs)}/{len(clauses)}")
        print(f"   Total références: {total_refs}")
        print(f"   Moyenne: {avg_refs:.1f} refs/clause")
        
        # Vérifier méthode de recherche
        semantic_count = sum(1 for c in clauses if c.get('search_method') == 'semantic')
        print(f"   Recherche sémantique: {semantic_count}/{len(clauses)} clauses")
        
        # Afficher quelques références
        if clauses_with_refs:
            print(f"\n   Exemple de références:")
            for ref in clauses_with_refs[0].get('legal_references', [])[:2]:
                print(f"   - {ref.get('source')} {ref.get('article')}: {ref.get('title')}")
        
        # Sauvegarder résultat pour test PDF
        with open(TEST_OUTPUT_DIR / "analysis_result.json", "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        return True, result
        
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        return False, None

def test_pdf_export(analysis_result):
    """Test 3: PDF Export"""
    print_section("3️⃣ TEST EXPORT PDF")
    
    if not analysis_result:
        print("⚠️ Skipping PDF test (no analysis result)")
        return False
    
    try:
        start_time = time.time()
        
        response = requests.post(
            f"{API_URL}/export-pdf",
            json=analysis_result,
            timeout=30
        )
        
        duration = time.time() - start_time
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        assert response.headers.get('Content-Type') == 'application/pdf', "Not a PDF"
        
        pdf_content = response.content
        pdf_path = TEST_OUTPUT_DIR / "rapport_test.pdf"
        
        with open(pdf_path, "wb") as f:
            f.write(pdf_content)
        
        print(f"✅ PDF généré en {duration:.2f}s")
        print(f"   Taille: {len(pdf_content):,} bytes ({len(pdf_content)/1024:.1f} KB)")
        print(f"   Sauvegardé: {pdf_path}")
        
        return True
        
    except Exception as e:
        print(f"❌ PDF export failed: {e}")
        return False

def test_performance():
    """Test 4: Performance Metrics"""
    print_section("4️⃣ TEST PERFORMANCE")
    
    tests = [
        ("Contrat court", BAIL_EXEMPLE[:500], 15),
        ("Contrat moyen", BAIL_EXEMPLE, 25),
        ("Contrat long", BAIL_EXEMPLE * 2, 40),
    ]
    
    results = []
    
    for name, text, max_time in tests:
        try:
            start = time.time()
            response = requests.post(
                f"{API_URL}/analyze",
                json={"text": text, "contract_type": "auto"},
                timeout=60
            )
            duration = time.time() - start
            
            status = "✅" if duration < max_time else "⚠️"
            results.append((name, duration, max_time, status))
            
        except Exception as e:
            results.append((name, None, max_time, "❌"))
    
    print("Temps de réponse:")
    for name, duration, max_time, status in results:
        if duration:
            print(f"   {status} {name}: {duration:.2f}s (max: {max_time}s)")
        else:
            print(f"   {status} {name}: FAILED")
    
    return all(status == "✅" for _, _, _, status in results)

def run_all_tests():
    """Execute all tests"""
    print("\n" + "="*60)
    print("  🧪 TESTS END-TO-END - AVANTDESIGNER")
    print("="*60)
    
    results = {}
    
    # Test 1: Health Check
    results['health'] = test_health_check()
    
    if not results['health']:
        print("\n❌ API non disponible. Arrêt des tests.")
        return
    
    # Test 2: Analysis + RAG
    results['analysis'], analysis_result = test_contract_analysis()
    
    # Test 3: PDF Export
    results['pdf'] = test_pdf_export(analysis_result)
    
    # Test 4: Performance
    results['performance'] = test_performance()
    
    # Summary
    print_section("📊 RÉSUMÉ DES TESTS")
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    
    for test_name, passed_test in results.items():
        status = "✅ PASS" if passed_test else "❌ FAIL"
        print(f"   {status} - {test_name.upper()}")
    
    print(f"\n   Total: {passed}/{total} tests réussis")
    
    if passed == total:
        print("\n🎉 TOUS LES TESTS SONT PASSÉS !")
    else:
        print(f"\n⚠️ {total - passed} test(s) échoué(s)")

if __name__ == "__main__":
    run_all_tests()
