"""
Contract Type Detection and Legal References Mapping
Comprehensive database for ALL contract types handled by AvantdeSigner
Including ALL possible subcontracting scenarios (B2B)
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
    Comprehensive coverage of all contract types for B2B/B2C legal analysis
    """
    
    def __init__(self):
        # Contract type patterns with keywords and legal codes
        self.contract_patterns = {
            # ========== SOUS-TRAITANCE (TOUS TYPES) ==========
            'soustraitance_securite': {
                'keywords': [
                    'sous-traitance', 'sous-traitant', 'donneur d\'ordre',
                    'gardiennage', 'sécurité privée', 'agent de sécurité', 'surveillance',
                    'cnaps', 'autorisation préfectorale', 'prévention', 'protection',
                    'intervention', 'alarme', 'ronde', 'vigile', 'agent cynophile',
                    'télésurveillance', 'vidéosurveillance', 'contrôle d\'accès'
                ],
                'legal_codes': ['loi_securite_privee', 'code_secu_interieure', 'code_travail_soustraitance'],
                'name': 'Contrat de Sous-traitance - Sécurité Privée',
                'category': 'Sous-traitance'
            },
            
            'soustraitance_informatique': {
                'keywords': [
                    'sous-traitance', 'sous-traitant', 'donneur d\'ordre',
                    'développement', 'informatique', 'it', 'logiciel', 'application',
                    'infogérance', 'tma', 'tierce maintenance', 'support technique',
                    'infrastructure', 'réseau', 'serveur', 'cloud', 'devops'
                ],
                'legal_codes': ['code_civil_contrats', 'code_commerce', 'code_travail_soustraitance'],
                'name': 'Contrat de Sous-traitance - Informatique/IT',
                'category': 'Sous-traitance'
            },
            
            'soustraitance_construction': {
                'keywords': [
                    'sous-traitance', 'sous-traitant', 'donneur d\'ordre', 'entreprise générale',
                    'construction', 'btp', 'travaux', 'chantier', 'gros œuvre', 'second œuvre',
                    'maçonnerie', 'plomberie', 'électricité', 'menuiserie', 'peinture',
                    'lot', 'corps d\'état', 'maître d\'œuvre'
                ],
                'legal_codes': ['code_civil_construction', 'code_construction', 'code_travail_soustraitance'],
                'name': 'Contrat de Sous-traitance - Construction/BTP',
                'category': 'Sous-traitance'
            },
            
            'soustraitance_nettoyage': {
                'keywords': [
                    'sous-traitance', 'sous-traitant', 'donneur d\'ordre',
                    'nettoyage', 'propreté', 'entretien', 'ménage', 'hygiène',
                    'agent d\'entretien', 'nettoyage industriel', 'nettoyage bureaux',
                    'désinfection', 'vitrerie'
                ],
                'legal_codes': ['code_civil_contrats', 'code_commerce', 'code_travail_soustraitance'],
                'name': 'Contrat de Sous-traitance - Nettoyage/Propreté',
                'category': 'Sous-traitance'
            },
            
            'soustraitance_logistique': {
                'keywords': [
                    'sous-traitance', 'sous-traitant', 'donneur d\'ordre',
                    'logistique', 'entreposage', 'stockage', 'préparation commandes',
                    'picking', 'packing', 'expédition', 'gestion stock',
                    'plateforme logistique', '3pl', '4pl'
                ],
                'legal_codes': ['code_commerce_transport', 'code_civil_contrats', 'code_travail_soustraitance'],
                'name': 'Contrat de Sous-traitance - Logistique/Entreposage',
                'category': 'Sous-traitance'
            },
            
            'soustraitance_restauration': {
                'keywords': [
                    'sous-traitance', 'sous-traitant', 'donneur d\'ordre',
                    'restauration', 'traiteur', 'cuisine', 'repas', 'cantine',
                    'restauration collective', 'service traiteur', 'événementiel',
                    'haccp', 'hygiène alimentaire'
                ],
                'legal_codes': ['code_civil_contrats', 'code_commerce', 'code_travail_soustraitance'],
                'name': 'Contrat de Sous-traitance - Restauration/Traiteur',
                'category': 'Sous-traitance'
            },
            
            'soustraitance_rh': {
                'keywords': [
                    'sous-traitance', 'sous-traitant', 'donneur d\'ordre',
                    'ressources humaines', 'rh', 'recrutement', 'paie', 'formation',
                    'gestion administrative', 'externalisation rh', 'bpo',
                    'gestion personnel', 'administration personnel'
                ],
                'legal_codes': ['code_civil_contrats', 'code_commerce', 'code_travail_soustraitance'],
                'name': 'Contrat de Sous-traitance - Ressources Humaines',
                'category': 'Sous-traitance'
            },
            
            'soustraitance_comptabilite': {
                'keywords': [
                    'sous-traitance', 'sous-traitant', 'donneur d\'ordre',
                    'comptabilité', 'expertise comptable', 'tenue comptable',
                    'bilan', 'déclarations fiscales', 'liasse fiscale',
                    'externalisation comptable', 'cabinet comptable'
                ],
                'legal_codes': ['code_civil_contrats', 'code_commerce', 'code_travail_soustraitance'],
                'name': 'Contrat de Sous-traitance - Comptabilité/Expertise',
                'category': 'Sous-traitance'
            },
            
            'soustraitance_marketing': {
                'keywords': [
                    'sous-traitance', 'sous-traitant', 'donneur d\'ordre',
                    'marketing', 'communication', 'publicité', 'digital marketing',
                    'seo', 'sea', 'réseaux sociaux', 'content marketing',
                    'agence communication', 'campagne publicitaire'
                ],
                'legal_codes': ['code_civil_contrats', 'code_commerce', 'code_travail_soustraitance'],
                'name': 'Contrat de Sous-traitance - Marketing/Communication',
                'category': 'Sous-traitance'
            },
            
            'soustraitance_juridique': {
                'keywords': [
                    'sous-traitance', 'sous-traitant', 'donneur d\'ordre',
                    'juridique', 'legal', 'conseil juridique', 'contentieux',
                    'rédaction contrats', 'veille juridique', 'compliance',
                    'externalisation juridique', 'legal process outsourcing'
                ],
                'legal_codes': ['code_civil_contrats', 'code_commerce', 'code_travail_soustraitance'],
                'name': 'Contrat de Sous-traitance - Services Juridiques',
                'category': 'Sous-traitance'
            },
            
            'soustraitance_industrielle': {
                'keywords': [
                    'sous-traitance', 'sous-traitant', 'donneur d\'ordre',
                    'fabrication', 'production', 'usinage', 'assemblage',
                    'sous-traitance industrielle', 'manufacture', 'oem',
                    'pièces détachées', 'composants'
                ],
                'legal_codes': ['code_civil_contrats', 'code_commerce', 'code_travail_soustraitance'],
                'name': 'Contrat de Sous-traitance - Industrielle/Fabrication',
                'category': 'Sous-traitance'
            },
            
            'soustraitance_maintenance': {
                'keywords': [
                    'sous-traitance', 'sous-traitant', 'donneur d\'ordre',
                    'maintenance', 'entretien', 'dépannage', 'réparation',
                    'maintenance préventive', 'maintenance curative',
                    'facility management', 'gestion technique'
                ],
                'legal_codes': ['code_civil_contrats', 'code_commerce', 'code_travail_soustraitance'],
                'name': 'Contrat de Sous-traitance - Maintenance Technique',
                'category': 'Sous-traitance'
            },
            
            # ========== IMMOBILIER ==========
            'bail_habitation': {
                'keywords': [
                    'loyer', 'locataire', 'bailleur', 'logement', 'habitation',
                    'dépôt de garantie', 'charges locatives', 'état des lieux',
                    'préavis', 'congé', 'tacite reconduction', 'surface habitable'
                ],
                'legal_codes': ['loi_89_462', 'code_civil_bail'],
                'name': 'Bail d\'Habitation',
                'category': 'Immobilier'
            },
            
            'bail_commercial': {
                'keywords': [
                    'bail commercial', 'fonds de commerce', 'pas-de-porte', 'droit au bail',
                    'activité commerciale', 'renouvellement bail', 'indemnité d\'éviction',
                    'clause résolutoire', 'destination des lieux', 'loyer commercial'
                ],
                'legal_codes': ['code_commerce_bail', 'code_civil_bail'],
                'name': 'Bail Commercial',
                'category': 'Immobilier'
            },
            
            'bail_professionnel': {
                'keywords': [
                    'bail professionnel', 'activité libérale', 'profession libérale',
                    'cabinet', 'bureau professionnel', 'exercice profession'
                ],
                'legal_codes': ['loi_86_1290', 'code_civil_bail'],
                'name': 'Bail Professionnel',
                'category': 'Immobilier'
            },
            
            'promesse_vente': {
                'keywords': [
                    'promesse de vente', 'compromis de vente', 'vente immobilière',
                    'acquéreur', 'vendeur', 'prix de vente', 'conditions suspensives',
                    'prêt immobilier', 'notaire', 'acte authentique'
                ],
                'legal_codes': ['code_civil_vente', 'code_construction'],
                'name': 'Promesse de Vente Immobilière',
                'category': 'Immobilier'
            },
            
            # ========== TRAVAIL & EMPLOI ==========
            'cdi': {
                'keywords': [
                    'contrat à durée indéterminée', 'cdi', 'salarié', 'employeur',
                    'rémunération', 'salaire', 'horaires', 'congés payés',
                    'période d\'essai', 'clause de non-concurrence', 'préavis'
                ],
                'legal_codes': ['code_travail_cdi'],
                'name': 'Contrat de Travail CDI',
                'category': 'Travail'
            },
            
            'cdd': {
                'keywords': [
                    'contrat à durée déterminée', 'cdd', 'remplacement', 'accroissement temporaire',
                    'terme précis', 'renouvellement', 'prime de précarité',
                    'motif de recours', 'durée maximale'
                ],
                'legal_codes': ['code_travail_cdd'],
                'name': 'Contrat de Travail CDD',
                'category': 'Travail'
            },
            
            'interim': {
                'keywords': [
                    'travail temporaire', 'intérim', 'mission', 'entreprise de travail temporaire',
                    'ett', 'entreprise utilisatrice', 'indemnité de fin de mission'
                ],
                'legal_codes': ['code_travail_interim'],
                'name': 'Contrat de Travail Temporaire (Intérim)',
                'category': 'Travail'
            },
            
            'apprentissage': {
                'keywords': [
                    'contrat d\'apprentissage', 'apprenti', 'maître d\'apprentissage',
                    'formation en alternance', 'cfa', 'diplôme', 'qualification professionnelle'
                ],
                'legal_codes': ['code_travail_apprentissage'],
                'name': 'Contrat d\'Apprentissage',
                'category': 'Travail'
            },
            
            'professionnalisation': {
                'keywords': [
                    'contrat de professionnalisation', 'alternance', 'qualification',
                    'action de professionnalisation', 'tuteur'
                ],
                'legal_codes': ['code_travail_professionnalisation'],
                'name': 'Contrat de Professionnalisation',
                'category': 'Travail'
            },
            
            # ========== PRESTATION DE SERVICES ==========
            'prestation_services': {
                'keywords': [
                    'prestataire', 'client', 'mission', 'livrable', 'délai',
                    'cahier des charges', 'réception', 'garantie', 'obligation de moyens',
                    'obligation de résultat', 'pénalités de retard'
                ],
                'legal_codes': ['code_civil_contrats', 'code_commerce'],
                'name': 'Contrat de Prestation de Services',
                'category': 'Services'
            },
            
            'maintenance': {
                'keywords': [
                    'maintenance', 'entretien', 'dépannage', 'assistance technique',
                    'niveau de service', 'sla', 'temps d\'intervention', 'astreinte'
                ],
                'legal_codes': ['code_civil_contrats', 'code_commerce'],
                'name': 'Contrat de Maintenance',
                'category': 'Services'
            },
            
            'conseil': {
                'keywords': [
                    'conseil', 'consultant', 'expertise', 'audit', 'recommandations',
                    'mission de conseil', 'honoraires', 'confidentialité'
                ],
                'legal_codes': ['code_civil_contrats', 'code_commerce'],
                'name': 'Contrat de Conseil',
                'category': 'Services'
            },
            
            # ========== INFORMATIQUE & DIGITAL ==========
            'developpement_logiciel': {
                'keywords': [
                    'développement', 'logiciel', 'application', 'code source',
                    'propriété intellectuelle', 'licence', 'bug', 'recette',
                    'spécifications fonctionnelles', 'api', 'hébergement'
                ],
                'legal_codes': ['code_propriete_intellectuelle', 'code_civil_contrats'],
                'name': 'Contrat de Développement Logiciel',
                'category': 'Informatique'
            },
            
            'licence_logiciel': {
                'keywords': [
                    'licence logiciel', 'droit d\'utilisation', 'utilisateur final',
                    'eula', 'saas', 'abonnement', 'mise à jour', 'support technique'
                ],
                'legal_codes': ['code_propriete_intellectuelle', 'code_commerce'],
                'name': 'Contrat de Licence Logiciel',
                'category': 'Informatique'
            },
            
            'hebergement_web': {
                'keywords': [
                    'hébergement', 'serveur', 'nom de domaine', 'bande passante',
                    'disponibilité', 'sauvegarde', 'infogérance', 'cloud'
                ],
                'legal_codes': ['code_commerce', 'rgpd'],
                'name': 'Contrat d\'Hébergement Web',
                'category': 'Informatique'
            },
            
            # ========== COMMERCIAL & DISTRIBUTION ==========
            'vente': {
                'keywords': [
                    'vente', 'acheteur', 'vendeur', 'marchandise', 'prix',
                    'livraison', 'garantie', 'vice caché', 'conformité',
                    'réserve de propriété', 'paiement'
                ],
                'legal_codes': ['code_civil_vente', 'code_commerce'],
                'name': 'Contrat de Vente',
                'category': 'Commercial'
            },
            
            'distribution': {
                'keywords': [
                    'distribution', 'distributeur', 'fournisseur', 'réseau de distribution',
                    'exclusivité', 'territoire', 'quota', 'objectif de vente',
                    'commission', 'approvisionnement'
                ],
                'legal_codes': ['code_commerce', 'code_civil_contrats'],
                'name': 'Contrat de Distribution',
                'category': 'Commercial'
            },
            
            'franchise': {
                'keywords': [
                    'franchise', 'franchiseur', 'franchisé', 'enseigne', 'savoir-faire',
                    'droit d\'entrée', 'redevance', 'royalties', 'document d\'information précontractuel',
                    'dip', 'réseau de franchise'
                ],
                'legal_codes': ['loi_doubin', 'code_commerce'],
                'name': 'Contrat de Franchise',
                'category': 'Commercial'
            },
            
            'agent_commercial': {
                'keywords': [
                    'agent commercial', 'mandat', 'commission', 'représentation',
                    'prospection', 'clientèle', 'indemnité de clientèle', 'indépendance'
                ],
                'legal_codes': ['code_commerce_agent', 'code_civil_mandat'],
                'name': 'Contrat d\'Agent Commercial',
                'category': 'Commercial'
            },
            
            # ========== PARTENARIAT & COLLABORATION ==========
            'partenariat': {
                'keywords': [
                    'partenaire', 'collaboration', 'coopération', 'accord de partenariat',
                    'objectifs communs', 'répartition', 'contribution', 'joint-venture'
                ],
                'legal_codes': ['code_civil_contrats', 'code_commerce'],
                'name': 'Accord de Partenariat',
                'category': 'Partenariat'
            },
            
            'consortium': {
                'keywords': [
                    'consortium', 'groupement', 'entreprises', 'projet commun',
                    'chef de file', 'cotraitance', 'solidarité'
                ],
                'legal_codes': ['code_civil_contrats', 'code_commerce'],
                'name': 'Accord de Consortium',
                'category': 'Partenariat'
            },
            
            # ========== ASSURANCE & FINANCE ==========
            'assurance': {
                'keywords': [
                    'assurance', 'assuré', 'assureur', 'prime', 'sinistre',
                    'indemnisation', 'garantie', 'exclusion', 'franchise',
                    'responsabilité civile', 'dommages'
                ],
                'legal_codes': ['code_assurances'],
                'name': 'Contrat d\'Assurance',
                'category': 'Assurance'
            },
            
            'pret': {
                'keywords': [
                    'prêt', 'emprunteur', 'prêteur', 'crédit', 'taux d\'intérêt',
                    'remboursement', 'échéance', 'garantie', 'hypothèque',
                    'caution', 'teg', 'taeg'
                ],
                'legal_codes': ['code_consommation_credit', 'code_monetaire'],
                'name': 'Contrat de Prêt',
                'category': 'Finance'
            },
            
            # ========== TRANSPORT & LOGISTIQUE ==========
            'transport': {
                'keywords': [
                    'transport', 'transporteur', 'expéditeur', 'destinataire',
                    'marchandise', 'livraison', 'lettre de voiture', 'responsabilité',
                    'retard', 'avarie', 'perte'
                ],
                'legal_codes': ['code_commerce_transport', 'code_civil_contrats'],
                'name': 'Contrat de Transport',
                'category': 'Transport'
            },
            
            # ========== CONSTRUCTION & BTP ==========
            'entreprise_construction': {
                'keywords': [
                    'construction', 'maître d\'ouvrage', 'entrepreneur', 'travaux',
                    'chantier', 'réception', 'garantie décennale', 'garantie biennale',
                    'garantie de parfait achèvement', 'dommages-ouvrage'
                ],
                'legal_codes': ['code_civil_construction', 'code_construction'],
                'name': 'Contrat d\'Entreprise (Construction)',
                'category': 'Construction'
            },
            
            # ========== PROPRIÉTÉ INTELLECTUELLE ==========
            'cession_droits_auteur': {
                'keywords': [
                    'cession', 'droits d\'auteur', 'œuvre', 'propriété intellectuelle',
                    'exploitation', 'reproduction', 'représentation', 'redevance',
                    'droit moral', 'droit patrimonial'
                ],
                'legal_codes': ['code_propriete_intellectuelle'],
                'name': 'Contrat de Cession de Droits d\'Auteur',
                'category': 'Propriété Intellectuelle'
            },
            
            'licence_marque': {
                'keywords': [
                    'licence de marque', 'marque', 'titulaire', 'licencié',
                    'exploitation', 'territoire', 'redevance', 'inpi'
                ],
                'legal_codes': ['code_propriete_intellectuelle'],
                'name': 'Contrat de Licence de Marque',
                'category': 'Propriété Intellectuelle'
            },
            
            # ========== AUTRES ==========
            'confidentialite': {
                'keywords': [
                    'confidentialité', 'nda', 'secret', 'information confidentielle',
                    'divulgation', 'protection', 'données sensibles'
                ],
                'legal_codes': ['code_civil_contrats', 'rgpd'],
                'name': 'Accord de Confidentialité (NDA)',
                'category': 'Autres'
            },
            
            'mandat': {
                'keywords': [
                    'mandat', 'mandant', 'mandataire', 'représentation', 'pouvoir',
                    'procuration', 'agir au nom de', 'intérêt'
                ],
                'legal_codes': ['code_civil_mandat'],
                'name': 'Contrat de Mandat',
                'category': 'Autres'
            }
        }
        
        # Legal references database by code
        self.legal_references = self._build_legal_database()
    
    def _build_legal_database(self) -> Dict[str, List[LegalReference]]:
        """Build comprehensive legal references database"""
        return {
            # SÉCURITÉ PRIVÉE
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
                )
            ],
            
            'code_secu_interieure': [
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
            
            # BAIL HABITATION
            'loi_89_462': [
                LegalReference(
                    code='Loi 89-462',
                    article='Article 1',
                    title='Champ d\'application',
                    summary='S\'applique aux locations de locaux à usage d\'habitation ou mixte professionnel et d\'habitation.'
                ),
                LegalReference(
                    code='Loi 89-462',
                    article='Article 3',
                    title='Durée du bail',
                    summary='Durée minimale de 3 ans (personne physique) ou 6 ans (personne morale). Renouvellement tacite sauf congé.'
                ),
                LegalReference(
                    code='Loi 89-462',
                    article='Article 5',
                    title='Préavis du locataire',
                    summary='Préavis de 3 mois (réduit à 1 mois pour mutation, perte d\'emploi, RSA, AAH, santé, +60 ans).'
                ),
                LegalReference(
                    code='Loi 89-462',
                    article='Article 24',
                    title='Clause résolutoire',
                    summary='Joue uniquement pour : non-paiement loyer/charges, non-paiement dépôt, défaut d\'assurance.'
                )
            ],
            
            # CODE DU TRAVAIL
            'code_travail_cdi': [
                LegalReference(
                    code='Code du Travail',
                    article='L1221-1',
                    title='Contrat de travail',
                    summary='Le contrat de travail est soumis aux règles du droit commun. Peut être établi selon les formes que les parties contractantes décident d\'adopter.'
                ),
                LegalReference(
                    code='Code du Travail',
                    article='L1234-1',
                    title='Rupture du contrat',
                    summary='Le contrat de travail à durée indéterminée peut être rompu à l\'initiative de l\'employeur ou du salarié, ou d\'un commun accord.'
                )
            ],
            
            'code_travail_cdd': [
                LegalReference(
                    code='Code du Travail',
                    article='L1242-1',
                    title='Cas de recours au CDD',
                    summary='Le CDD ne peut être conclu que pour l\'exécution d\'une tâche précise et temporaire, dans les cas limitativement énumérés.'
                ),
                LegalReference(
                    code='Code du Travail',
                    article='L1243-8',
                    title='Indemnité de précarité',
                    summary='À l\'issue du CDD, le salarié a droit à une indemnité de fin de contrat égale à 10% de la rémunération totale brute.'
                )
            ],
            
            'code_travail_soustraitance': [
                LegalReference(
                    code='Code du Travail',
                    article='L8221-1',
                    title='Travail dissimulé',
                    summary='Interdit le travail dissimulé. Obligation de déclaration préalable à l\'embauche, remise bulletin de paie.'
                ),
                LegalReference(
                    code='Code du Travail',
                    article='L8241-1',
                    title='Sous-traitance et cotraitance',
                    summary='Obligation de vigilance du donneur d\'ordre sur les conditions de travail des salariés des sous-traitants.'
                ),
                LegalReference(
                    code='Code du Travail',
                    article='L8222-1',
                    title='Marchandage',
                    summary='Interdit le marchandage (prêt illicite de main-d\'œuvre). Sanctions pénales pour le donneur d\'ordre et le sous-traitant.'
                )
            ],
            
            # CODE CIVIL - CONTRATS GÉNÉRAUX
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
            ],
            
            # CODE COMMERCE
            'code_commerce': [
                LegalReference(
                    code='Code de Commerce',
                    article='L110-1',
                    title='Actes de commerce',
                    summary='Définit les actes de commerce par nature et par accessoire.'
                ),
                LegalReference(
                    code='Code de Commerce',
                    article='L442-1',
                    title='Pratiques restrictives',
                    summary='Interdit les pratiques restrictives de concurrence et les déséquilibres significatifs.'
                )
            ],
            
            # PROPRIÉTÉ INTELLECTUELLE
            'code_propriete_intellectuelle': [
                LegalReference(
                    code='Code Propriété Intellectuelle',
                    article='L111-1',
                    title='Droit d\'auteur',
                    summary='L\'auteur d\'une œuvre de l\'esprit jouit sur cette œuvre, du seul fait de sa création, d\'un droit de propriété incorporelle.'
                ),
                LegalReference(
                    code='Code Propriété Intellectuelle',
                    article='L131-3',
                    title='Cession des droits',
                    summary='La transmission des droits de l\'auteur est subordonnée à la condition que chacun des droits cédés fasse l\'objet d\'une mention distincte dans l\'acte de cession.'
                )
            ],
            
            # RGPD
            'rgpd': [
                LegalReference(
                    code='RGPD',
                    article='Article 5',
                    title='Principes relatifs au traitement des données',
                    summary='Les données doivent être traitées de manière licite, loyale et transparente. Collecte limitée aux finalités déterminées.'
                ),
                LegalReference(
                    code='RGPD',
                    article='Article 6',
                    title='Licéité du traitement',
                    summary='Le traitement n\'est licite que si la personne concernée a consenti ou si le traitement est nécessaire à l\'exécution d\'un contrat.'
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
                'name': config['name'],
                'category': config['category']
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
        if 'code_civil_contrats' in self.legal_references and contract_type != 'bail_habitation':
            references.extend(self.legal_references['code_civil_contrats'][:2])  # Force obligatoire + Bonne foi
        
        return references[:6]  # Limit to most relevant
    
    def get_all_contract_types(self) -> List[Dict]:
        """Get list of all supported contract types"""
        return [
            {
                'key': key,
                'name': config['name'],
                'category': config['category'],
                'keywords_count': len(config['keywords'])
            }
            for key, config in self.contract_patterns.items()
        ]

# Singleton
contract_detector = ContractTypeDetector()
