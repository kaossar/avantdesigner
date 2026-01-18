"""
Contract Type Detection and Legal References Mapping
Detects contract type and provides appropriate legal references
"""
import re
from typing import Dict, List, Tuple
from dataclasses import dataclass

@dataclass
class LegalReference:
    code: str
    article: str
    title: str
    summary: str
    relevance_score: float = 1.0

class ContractTypeDetector:
    """
    Intelligent contract type detection based on keywords and structure
    """
    
    def __init__(self):
        # Contract type patterns with keywords
        self.contract_patterns = {
            'sous_traitance_securite': {
                'keywords': [
                    'gardiennage', 'sécurité privée', 'agent de sécurité', 'surveillance',
                    'cnaps', 'autorisation préfectorale', 'prévention', 'protection',
                    'intervention', 'alarme', 'ronde', 'vigile', 'agent cynophile'
                ],
                'legal_codes': ['code_travail', 'loi_securite_privee', 'code_secu_interieure'],
                'name': 'Contrat de Sous-traitance en Sécurité Privée'
            },
            'bail_habitation': {
                'keywords': [
                    'loyer', 'locataire', 'bailleur', 'logement', 'habitation',
                    'dépôt de garantie', 'charges locatives', 'état des lieux'
                ],
                'legal_codes': ['loi_89_462', 'code_civil_bail'],
                'name': 'Bail d\'Habitation'
            },
            'prestation_services': {
                'keywords': [
                    'prestataire', 'client', 'mission', 'livrable', 'délai',
                    'cahier des charges', 'réception', 'garantie'
                ],
                'legal_codes': ['code_civil_contrats', 'code_commerce'],
                'name': 'Contrat de Prestation de Services'
            },
            'travail_cdd': {
                'keywords': [
                    'salarié', 'employeur', 'contrat à durée déterminée', 'cdd',
                    'période d\'essai', 'rémunération', 'horaires', 'congés payés'
                ],
                'legal_codes': ['code_travail'],
                'name': 'Contrat de Travail CDD'
            },
            'partenariat': {
                'keywords': [
                    'partenaire', 'collaboration', 'coopération', 'accord de partenariat',
                    'objectifs communs', 'répartition', 'contribution'
                ],
                'legal_codes': ['code_civil_contrats', 'code_commerce'],
                'name': 'Accord de Partenariat'
            }
        }
        
        # Legal references database by code
        self.legal_references = {
            'loi_securite_privee': [
                LegalReference(
                    code='Loi 83-629',
                    article='Article 1',
                    title='Activités privées de sécurité',
                    summary='Réglemente les activités de surveillance, gardiennage, transport de fonds, protection physique. Nécessite autorisation CNAPS.'
                ),
                LegalReference(
                    code='Loi 83-629',
                    article='Article 6',
                    title='Autorisation d\'exercer',
                    summary='Obligation d\'obtenir une autorisation préfectorale pour exercer. Conditions : moralité, formation, aptitude professionnelle.'
                ),
                LegalReference(
                    code='Code Sécurité Intérieure',
                    article='L611-1',
                    title='Définition activités privées',
                    summary='Définit les activités de surveillance et gardiennage, transport de fonds, protection physique, sûreté aéroportuaire.'
                ),
                LegalReference(
                    code='Code Sécurité Intérieure',
                    article='L612-1',
                    title='Agrément et autorisation',
                    summary='Conditions d\'agrément des entreprises et d\'autorisation des agents. Contrôle CNAPS obligatoire.'
                )
            ],
            'code_travail': [
                LegalReference(
                    code='Code du Travail',
                    article='L1221-1',
                    title='Contrat de travail',
                    summary='Le contrat de travail est soumis aux règles du droit commun. Peut être établi selon les formes que les parties contractantes décident d\'adopter.'
                ),
                LegalReference(
                    code='Code du Travail',
                    article='L8221-1',
                    title='Travail dissimulé',
                    summary='Interdit le travail dissimulé. Obligation de déclaration préalable à l\'embauche, remise bulletin de paie, déclaration charges sociales.'
                ),
                LegalReference(
                    code='Code du Travail',
                    article='L8241-1',
                    title='Sous-traitance et cotraitance',
                    summary='Obligation de vigilance du donneur d\'ordre sur les conditions de travail des salariés des sous-traitants.'
                )
            ],
            'loi_89_462': [
                # Bail d'habitation (existant)
                LegalReference(
                    code='Loi 89-462',
                    article='Article 1',
                    title='Champ d\'application',
                    summary='S\'applique aux locations de locaux à usage d\'habitation ou mixte.'
                )
            ],
            'code_civil_contrats': [
                LegalReference(
                    code='Code Civil',
                    article='1103',
                    title='Force obligatoire',
                    summary='Les contrats légalement formés tiennent lieu de loi à ceux qui les ont faits.'
                ),
                LegalReference(
                    code='Code Civil',
                    article='1104',
                    title='Bonne foi',
                    summary='Les contrats doivent être négociés, formés et exécutés de bonne foi.'
                ),
                LegalReference(
                    code='Code Civil',
                    article='1231-1',
                    title='Dommages et intérêts',
                    summary='Le débiteur est condamné à des dommages-intérêts en cas d\'inexécution du contrat.'
                )
            ]
        }
    
    def detect_contract_type(self, text: str) -> Tuple[str, float, str]:
        """
        Detect contract type from text
        
        Returns:
            (contract_type_key, confidence_score, contract_name)
        """
        text_lower = text.lower()
        scores = {}
        
        for contract_type, config in self.contract_patterns.items():
            score = 0
            matches = []
            
            for keyword in config['keywords']:
                if keyword.lower() in text_lower:
                    score += 1
                    matches.append(keyword)
            
            # Normalize score
            confidence = min(1.0, score / len(config['keywords']))
            scores[contract_type] = {
                'score': confidence,
                'matches': matches,
                'name': config['name']
            }
        
        # Get best match
        if not scores:
            return ('prestation_services', 0.5, 'Contrat de Prestation de Services')
        
        best_type = max(scores.items(), key=lambda x: x[1]['score'])
        contract_key = best_type[0]
        confidence = best_type[1]['score']
        name = best_type[1]['name']
        
        return (contract_key, confidence, name)
    
    def get_legal_references(self, contract_type: str, clause_type: str = None) -> List[LegalReference]:
        """
        Get relevant legal references for a contract type
        
        Args:
            contract_type: Detected contract type key
            clause_type: Optional specific clause type for filtering
        
        Returns:
            List of relevant legal references
        """
        if contract_type not in self.contract_patterns:
            contract_type = 'prestation_services'
        
        legal_codes = self.contract_patterns[contract_type]['legal_codes']
        references = []
        
        for code in legal_codes:
            if code in self.legal_references:
                references.extend(self.legal_references[code])
        
        # Add general contract law references
        if 'code_civil_contrats' in self.legal_references:
            references.extend(self.legal_references['code_civil_contrats'][:2])  # Force obligatoire + Bonne foi
        
        return references[:4]  # Limit to most relevant

# Singleton
contract_detector = ContractTypeDetector()
