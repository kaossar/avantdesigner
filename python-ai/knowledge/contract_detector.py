"""
Comprehensive Contract Type Detection System
Covers 100+ contract types across 9 strategic categories
Production-ready for B2C, Freelance, and B2B markets
"""
import re
from typing import Dict, List, Tuple, Set
from dataclasses import dataclass
from enum import Enum

class ContractCategory(Enum):
    """Strategic contract categories"""
    DAILY_HOUSING = "Logement"
    DAILY_CONSUMPTION = "Consommation"
    DAILY_INSURANCE = "Assurances"
    EMPLOYMENT = "Travail Salarié"
    FREELANCE = "Freelance/Indépendants"
    COMMERCIAL = "Commercial & Business"
    DIGITAL_IP = "Numérique & Propriété Intellectuelle"
    REAL_ESTATE_CONSTRUCTION = "Immobilier & Construction"
    TRANSPORT_LEISURE = "Transport & Loisirs"
    HIGH_RISK = "Contrats à Risque Élevé"
    INTERNATIONAL = "Contrats Internationaux"
    SUBCONTRACTING = "Sous-traitance"

@dataclass
class LegalReference:
    code: str
    article: str
    title: str
    summary: str
    relevance_score: float = 1.0

@dataclass
class ContractTypeDefinition:
    """Definition of a contract type"""
    key: str
    name: str
    category: ContractCategory
    keywords: List[str]
    legal_codes: List[str]
    priority: int = 1  # Higher = more specific

class ComprehensiveContractDetector:
    """
    Intelligent contract type detection system
    Covers 100+ contract types with smart keyword matching
    """
    
    def __init__(self):
        self.contract_types = self._build_contract_database()
        self.legal_references = self._build_legal_database()
    
    def _build_contract_database(self) -> List[ContractTypeDefinition]:
        """Build comprehensive contract type database"""
        return [
            # ========== 1. DAILY CONTRACTS - HOUSING ==========
            ContractTypeDefinition(
                key='bail_habitation_vide',
                name='Bail d\'Habitation Vide',
                category=ContractCategory.DAILY_HOUSING,
                keywords=['bail', 'habitation', 'vide', 'loyer', 'locataire', 'bailleur', 'logement'],
                legal_codes=['loi_89_462', 'code_civil_bail'],
                priority=2
            ),
            ContractTypeDefinition(
                key='bail_meuble',
                name='Bail Meublé',
                category=ContractCategory.DAILY_HOUSING,
                keywords=['bail', 'meublé', 'location meublée', 'loyer', 'locataire'],
                legal_codes=['loi_89_462', 'code_civil_bail'],
                priority=2
            ),
            ContractTypeDefinition(
                key='bail_etudiant',
                name='Bail Étudiant',
                category=ContractCategory.DAILY_HOUSING,
                keywords=['bail', 'étudiant', 'location étudiante', 'résidence universitaire', '9 mois'],
                legal_codes=['loi_89_462'],
                priority=3
            ),
            ContractTypeDefinition(
                key='bail_mobilite',
                name='Bail Mobilité',
                category=ContractCategory.DAILY_HOUSING,
                keywords=['bail mobilité', 'mutation professionnelle', 'formation', '1 à 10 mois'],
                legal_codes=['loi_elan'],
                priority=3
            ),
            ContractTypeDefinition(
                key='etat_lieux',
                name='État des Lieux',
                category=ContractCategory.DAILY_HOUSING,
                keywords=['état des lieux', 'entrée', 'sortie', 'constat', 'huissier'],
                legal_codes=['loi_89_462'],
                priority=2
            ),
            ContractTypeDefinition(
                key='cautionnement',
                name='Acte de Cautionnement',
                category=ContractCategory.DAILY_HOUSING,
                keywords=['caution', 'cautionnement', 'garant', 'solidaire'],
                legal_codes=['code_civil_cautionnement'],
                priority=2
            ),
            ContractTypeDefinition(
                key='colocation',
                name='Contrat de Colocation',
                category=ContractCategory.DAILY_HOUSING,
                keywords=['colocation', 'colocataire', 'bail collectif', 'clause de solidarité'],
                legal_codes=['loi_89_462'],
                priority=2
            ),
            ContractTypeDefinition(
                key='mandat_gestion_locative',
                name='Mandat de Gestion Locative',
                category=ContractCategory.DAILY_HOUSING,
                keywords=['mandat', 'gestion locative', 'administrateur de biens', 'syndic'],
                legal_codes=['loi_hoguet'],
                priority=2
            ),
            ContractTypeDefinition(
                key='compromis_vente_immo',
                name='Compromis de Vente Immobilière',
                category=ContractCategory.DAILY_HOUSING,
                keywords=['compromis', 'vente immobilière', 'acquéreur', 'vendeur', 'notaire'],
                legal_codes=['code_civil_vente'],
                priority=2
            ),
            ContractTypeDefinition(
                key='promesse_vente',
                name='Promesse Unilatérale de Vente',
                category=ContractCategory.DAILY_HOUSING,
                keywords=['promesse unilatérale', 'option', 'bénéficiaire', 'promettant'],
                legal_codes=['code_civil_vente'],
                priority=3
            ),
            
            # ========== 2. DAILY CONTRACTS - CONSUMPTION ==========
            ContractTypeDefinition(
                key='credit_consommation',
                name='Contrat de Crédit à la Consommation',
                category=ContractCategory.DAILY_CONSUMPTION,
                keywords=['crédit', 'consommation', 'prêt', 'emprunteur', 'taeg', 'mensualité', 'bordereau de rétractation'],
                legal_codes=['code_consommation_credit'],
                priority=2
            ),
            ContractTypeDefinition(
                 key='carte_bancaire',
                 name='Contrat Carte Bancaire',
                 category=ContractCategory.DAILY_CONSUMPTION,
                 keywords=['carte bancaire', 'convention de compte', 'débit immédiat', 'débit différé', 'plafond de paiement', 'code confidentiel'],
                 legal_codes=['code_monetaire', 'code_consommation'],
                 priority=2
            ),
            ContractTypeDefinition(
                key='credit_renouvelable',
                name='Crédit Renouvelable',
                category=ContractCategory.DAILY_CONSUMPTION,
                keywords=['crédit renouvelable', 'réserve d\'argent', 'revolving'],
                legal_codes=['code_consommation_credit'],
                priority=3
            ),
            ContractTypeDefinition(
                key='pret_personnel',
                name='Prêt Personnel',
                category=ContractCategory.DAILY_CONSUMPTION,
                keywords=['prêt personnel', 'crédit personnel', 'emprunt'],
                legal_codes=['code_consommation_credit'],
                priority=2
            ),
            ContractTypeDefinition(
                key='leasing',
                name='Contrat de Leasing / LOA / LLD',
                category=ContractCategory.DAILY_CONSUMPTION,
                keywords=['leasing', 'loa', 'lld', 'location avec option d\'achat', 'longue durée'],
                legal_codes=['code_commerce'],
                priority=2
            ),
            ContractTypeDefinition(
                key='cgv',
                name='Conditions Générales de Vente (CGV)',
                category=ContractCategory.DAILY_CONSUMPTION,
                keywords=['cgv', 'conditions générales de vente', 'modalités de vente'],
                legal_codes=['code_commerce', 'code_consommation'],
                priority=2
            ),
            ContractTypeDefinition(
                key='cgu',
                name='Conditions Générales d\'Utilisation (CGU)',
                category=ContractCategory.DAILY_CONSUMPTION,
                keywords=['cgu', 'conditions générales d\'utilisation', 'conditions d\'usage'],
                legal_codes=['code_civil_contrats'],
                priority=2
            ),
            ContractTypeDefinition(
                key='abonnement',
                name='Contrat d\'Abonnement',
                category=ContractCategory.DAILY_CONSUMPTION,
                keywords=['abonnement', 'souscription', 'forfait', 'mensuel', 'annuel'],
                legal_codes=['code_consommation'],
                priority=1
            ),
            
            # ========== 3. DAILY CONTRACTS - INSURANCE ==========
            ContractTypeDefinition(
                key='assurance_habitation',
                name='Assurance Habitation',
                category=ContractCategory.DAILY_INSURANCE,
                keywords=['assurance habitation', 'multirisque habitation', 'mrh', 'dégât des eaux'],
                legal_codes=['code_assurances'],
                priority=2
            ),
            ContractTypeDefinition(
                key='assurance_auto',
                name='Assurance Auto / Moto',
                category=ContractCategory.DAILY_INSURANCE,
                keywords=['assurance auto', 'assurance moto', 'responsabilité civile', 'tous risques'],
                legal_codes=['code_assurances'],
                priority=2
            ),
            ContractTypeDefinition(
                key='assurance_sante',
                name='Assurance Santé / Mutuelle',
                category=ContractCategory.DAILY_INSURANCE,
                keywords=['mutuelle', 'assurance santé', 'complémentaire santé', 'remboursement'],
                legal_codes=['code_assurances', 'code_securite_sociale'],
                priority=2
            ),
            ContractTypeDefinition(
                key='assurance_prevoyance',
                name='Assurance Prévoyance',
                category=ContractCategory.DAILY_INSURANCE,
                keywords=['prévoyance', 'incapacité', 'invalidité', 'décès', 'rente'],
                legal_codes=['code_assurances'],
                priority=2
            ),
            ContractTypeDefinition(
                key='assurance_emprunteur',
                name='Assurance Emprunteur',
                category=ContractCategory.DAILY_INSURANCE,
                keywords=['assurance emprunteur', 'assurance prêt', 'garantie décès', 'perte d\'emploi'],
                legal_codes=['code_assurances', 'code_consommation'],
                priority=3
            ),
            ContractTypeDefinition(
                key='assurance_scolaire',
                name='Assurance Scolaire',
                category=ContractCategory.DAILY_INSURANCE,
                keywords=['assurance scolaire', 'école', 'responsabilité civile enfant'],
                legal_codes=['code_assurances'],
                priority=2
            ),
            ContractTypeDefinition(
                key='assurance_protection_juridique',
                name='Assurance Protection Juridique',
                category=ContractCategory.DAILY_INSURANCE,
                keywords=['protection juridique', 'défense juridique', 'litige'],
                legal_codes=['code_assurances'],
                priority=2
            ),
            ContractTypeDefinition(
                key='assurance_professionnelle',
                name='Assurance Professionnelle',
                category=ContractCategory.DAILY_INSURANCE,
                keywords=['assurance professionnelle', 'rc pro', 'responsabilité civile professionnelle'],
                legal_codes=['code_assurances'],
                priority=2
            ),
            
            # ========== 4. EMPLOYMENT ==========
            ContractTypeDefinition(
                key='cdi',
                name='Contrat de Travail CDI',
                category=ContractCategory.EMPLOYMENT,
                keywords=['cdi', 'durée indéterminée', 'salarié', 'employeur', 'contrat de travail'],
                legal_codes=['code_travail_cdi'],
                priority=2
            ),
            ContractTypeDefinition(
                key='cdd',
                name='Contrat de Travail CDD',
                category=ContractCategory.EMPLOYMENT,
                keywords=['cdd', 'durée déterminée', 'terme précis', 'remplacement'],
                legal_codes=['code_travail_cdd'],
                priority=2
            ),
            ContractTypeDefinition(
                key='interim',
                name='Contrat de Travail Temporaire (Intérim)',
                category=ContractCategory.EMPLOYMENT,
                keywords=['intérim', 'travail temporaire', 'ett', 'mission'],
                legal_codes=['code_travail_interim'],
                priority=2
            ),
            ContractTypeDefinition(
                key='apprentissage',
                name='Contrat d\'Apprentissage',
                category=ContractCategory.EMPLOYMENT,
                keywords=['apprentissage', 'apprenti', 'cfa', 'alternance'],
                legal_codes=['code_travail_apprentissage'],
                priority=2
            ),
            ContractTypeDefinition(
                key='professionnalisation',
                name='Contrat de Professionnalisation',
                category=ContractCategory.EMPLOYMENT,
                keywords=['professionnalisation', 'alternance', 'qualification'],
                legal_codes=['code_travail_professionnalisation'],
                priority=2
            ),
            ContractTypeDefinition(
                key='avenant_travail',
                name='Avenant au Contrat de Travail',
                category=ContractCategory.EMPLOYMENT,
                keywords=['avenant', 'modification', 'changement de poste', 'augmentation'],
                legal_codes=['code_travail_cdi'],
                priority=2
            ),
            ContractTypeDefinition(
                key='rupture_conventionnelle',
                name='Rupture Conventionnelle',
                category=ContractCategory.EMPLOYMENT,
                keywords=['rupture conventionnelle', 'accord mutuel', 'indemnité de rupture'],
                legal_codes=['code_travail_cdi'],
                priority=3
            ),
            ContractTypeDefinition(
                key='transaction_licenciement',
                name='Transaction Post-Licenciement',
                category=ContractCategory.EMPLOYMENT,
                keywords=['transaction', 'licenciement', 'conciliation', 'indemnité transactionnelle'],
                legal_codes=['code_travail_cdi'],
                priority=3
            ),
            
            # ========== 5. FREELANCE ==========
            ContractTypeDefinition(
                key='prestation_services',
                name='Contrat de Prestation de Services',
                category=ContractCategory.FREELANCE,
                keywords=['prestation', 'prestataire', 'client', 'mission', 'livrable'],
                legal_codes=['code_civil_contrats', 'code_commerce'],
                priority=1
            ),
            ContractTypeDefinition(
                key='mission_freelance',
                name='Contrat de Mission Freelance',
                category=ContractCategory.FREELANCE,
                keywords=['freelance', 'indépendant', 'auto-entrepreneur', 'mission'],
                legal_codes=['code_civil_contrats'],
                priority=2
            ),
            ContractTypeDefinition(
                key='portage_salarial',
                name='Contrat de Portage Salarial',
                category=ContractCategory.FREELANCE,
                keywords=['portage salarial', 'société de portage', 'consultant porté'],
                legal_codes=['code_travail_portage'],
                priority=3
            ),
            ContractTypeDefinition(
                key='apporteur_affaires',
                name='Contrat d\'Apporteur d\'Affaires',
                category=ContractCategory.FREELANCE,
                keywords=['apporteur d\'affaires', 'commission', 'mise en relation'],
                legal_codes=['code_civil_contrats'],
                priority=2
            ),
            ContractTypeDefinition(
                key='nda',
                name='Accord de Confidentialité (NDA)',
                category=ContractCategory.FREELANCE,
                keywords=['nda', 'confidentialité', 'secret', 'information confidentielle'],
                legal_codes=['code_civil_contrats', 'rgpd'],
                priority=2
            ),
            ContractTypeDefinition(
                key='lettre_mission',
                name='Lettre de Mission',
                category=ContractCategory.FREELANCE,
                keywords=['lettre de mission', 'mandat', 'objectifs', 'honoraires'],
                legal_codes=['code_civil_contrats'],
                priority=2
            ),
            
            # ========== 6. COMMERCIAL & BUSINESS ==========
            ContractTypeDefinition(
                key='contrat_commercial',
                name='Contrat Commercial Général',
                category=ContractCategory.COMMERCIAL,
                keywords=['contrat commercial', 'accord commercial', 'relation commerciale'],
                legal_codes=['code_commerce'],
                priority=1
            ),
            ContractTypeDefinition(
                key='partenariat',
                name='Contrat de Partenariat',
                category=ContractCategory.COMMERCIAL,
                keywords=['partenariat', 'partenaire', 'collaboration', 'coopération'],
                legal_codes=['code_civil_contrats', 'code_commerce'],
                priority=2
            ),
            ContractTypeDefinition(
                key='distribution',
                name='Contrat de Distribution',
                category=ContractCategory.COMMERCIAL,
                keywords=['distribution', 'distributeur', 'réseau', 'exclusivité'],
                legal_codes=['code_commerce'],
                priority=2
            ),
            ContractTypeDefinition(
                key='agent_commercial',
                name='Contrat d\'Agent Commercial',
                category=ContractCategory.COMMERCIAL,
                keywords=['agent commercial', 'mandat', 'commission', 'représentation'],
                legal_codes=['code_commerce_agent'],
                priority=2
            ),
            ContractTypeDefinition(
                key='franchise',
                name='Contrat de Franchise',
                category=ContractCategory.COMMERCIAL,
                keywords=['franchise', 'franchiseur', 'franchisé', 'enseigne', 'savoir-faire'],
                legal_codes=['loi_doubin', 'code_commerce'],
                priority=3
            ),
            ContractTypeDefinition(
                key='licence_commerciale',
                name='Contrat de Licence Commerciale',
                category=ContractCategory.COMMERCIAL,
                keywords=['licence', 'exploitation', 'redevance', 'territoire'],
                legal_codes=['code_commerce'],
                priority=2
            ),
            ContractTypeDefinition(
                key='concession',
                name='Contrat de Concession',
                category=ContractCategory.COMMERCIAL,
                keywords=['concession', 'concessionnaire', 'exclusivité territoriale'],
                legal_codes=['code_commerce'],
                priority=2
            ),
            ContractTypeDefinition(
                key='affiliation',
                name='Contrat d\'Affiliation',
                category=ContractCategory.COMMERCIAL,
                keywords=['affiliation', 'affilié', 'programme d\'affiliation', 'commission'],
                legal_codes=['code_commerce'],
                priority=2
            ),
            ContractTypeDefinition(
                key='vente_b2b',
                name='Contrat de Vente B2B',
                category=ContractCategory.COMMERCIAL,
                keywords=['vente', 'acheteur', 'vendeur', 'marchandise', 'livraison'],
                legal_codes=['code_civil_vente', 'code_commerce'],
                priority=1
            ),
            ContractTypeDefinition(
                key='contrat_fournisseur',
                name='Contrat Fournisseur',
                category=ContractCategory.COMMERCIAL,
                keywords=['fournisseur', 'approvisionnement', 'fourniture'],
                legal_codes=['code_commerce'],
                priority=2
            ),
            ContractTypeDefinition(
                key='contrat_cadre',
                name='Contrat Cadre',
                category=ContractCategory.COMMERCIAL,
                keywords=['contrat cadre', 'accord cadre', 'conditions générales'],
                legal_codes=['code_commerce'],
                priority=2
            ),
            ContractTypeDefinition(
                key='sla',
                name='Accord de Niveau de Service (SLA)',
                category=ContractCategory.COMMERCIAL,
                keywords=['sla', 'niveau de service', 'disponibilité', 'performance'],
                legal_codes=['code_commerce'],
                priority=2
            ),
            
            # ========== 7. DIGITAL & IP ==========
            ContractTypeDefinition(
                key='saas',
                name='Contrat SaaS',
                category=ContractCategory.DIGITAL_IP,
                keywords=['saas', 'software as a service', 'cloud', 'abonnement logiciel'],
                legal_codes=['code_propriete_intellectuelle', 'code_commerce'],
                priority=3
            ),
            ContractTypeDefinition(
                key='hebergement',
                name='Contrat d\'Hébergement Web',
                category=ContractCategory.DIGITAL_IP,
                keywords=['hébergement', 'serveur', 'hosting', 'nom de domaine'],
                legal_codes=['code_commerce', 'rgpd'],
                priority=2
            ),
            ContractTypeDefinition(
                key='maintenance_informatique',
                name='Contrat de Maintenance Informatique',
                category=ContractCategory.DIGITAL_IP,
                keywords=['maintenance', 'support', 'assistance technique', 'tma'],
                legal_codes=['code_civil_contrats'],
                priority=2
            ),
            ContractTypeDefinition(
                key='infogerance',
                name='Contrat d\'Infogérance',
                category=ContractCategory.DIGITAL_IP,
                keywords=['infogérance', 'externalisation it', 'gestion infrastructure'],
                legal_codes=['code_commerce'],
                priority=2
            ),
            ContractTypeDefinition(
                key='developpement_logiciel',
                name='Contrat de Développement Logiciel',
                category=ContractCategory.DIGITAL_IP,
                keywords=['développement', 'logiciel', 'application', 'code source'],
                legal_codes=['code_propriete_intellectuelle'],
                priority=2
            ),
            ContractTypeDefinition(
                key='cybersecurite',
                name='Contrat de Cybersécurité',
                category=ContractCategory.DIGITAL_IP,
                keywords=['cybersécurité', 'sécurité informatique', 'protection données'],
                legal_codes=['rgpd', 'code_commerce'],
                priority=2
            ),
            ContractTypeDefinition(
                key='cession_droits_auteur',
                name='Cession de Droits d\'Auteur',
                category=ContractCategory.DIGITAL_IP,
                keywords=['cession', 'droits d\'auteur', 'œuvre', 'propriété intellectuelle'],
                legal_codes=['code_propriete_intellectuelle'],
                priority=2
            ),
            ContractTypeDefinition(
                key='licence_droits',
                name='Licence de Droits d\'Auteur',
                category=ContractCategory.DIGITAL_IP,
                keywords=['licence', 'exploitation', 'reproduction', 'représentation'],
                legal_codes=['code_propriete_intellectuelle'],
                priority=2
            ),
            ContractTypeDefinition(
                key='contrat_edition',
                name='Contrat d\'Édition',
                category=ContractCategory.DIGITAL_IP,
                keywords=['édition', 'éditeur', 'auteur', 'publication'],
                legal_codes=['code_propriete_intellectuelle'],
                priority=2
            ),
            ContractTypeDefinition(
                key='licence_marque',
                name='Contrat de Licence de Marque',
                category=ContractCategory.DIGITAL_IP,
                keywords=['marque', 'licence de marque', 'inpi', 'titulaire'],
                legal_codes=['code_propriete_intellectuelle'],
                priority=2
            ),
            
            # ========== 8. REAL ESTATE & CONSTRUCTION ==========
            ContractTypeDefinition(
                key='bail_commercial',
                name='Bail Commercial',
                category=ContractCategory.REAL_ESTATE_CONSTRUCTION,
                keywords=['bail commercial', 'fonds de commerce', 'pas-de-porte'],
                legal_codes=['code_commerce_bail'],
                priority=2
            ),
            ContractTypeDefinition(
                key='bail_professionnel',
                name='Bail Professionnel',
                category=ContractCategory.REAL_ESTATE_CONSTRUCTION,
                keywords=['bail professionnel', 'activité libérale', 'cabinet'],
                legal_codes=['loi_86_1290'],
                priority=2
            ),
            ContractTypeDefinition(
                key='ccmi',
                name='Contrat de Construction de Maison Individuelle (CCMI)',
                category=ContractCategory.REAL_ESTATE_CONSTRUCTION,
                keywords=['ccmi', 'construction', 'maison individuelle', 'constructeur'],
                legal_codes=['code_construction'],
                priority=3
            ),
            ContractTypeDefinition(
                key='maitrise_oeuvre',
                name='Contrat de Maîtrise d\'Œuvre',
                category=ContractCategory.REAL_ESTATE_CONSTRUCTION,
                keywords=['maîtrise d\'œuvre', 'architecte', 'conception', 'suivi travaux'],
                legal_codes=['code_construction'],
                priority=2
            ),
            ContractTypeDefinition(
                key='marche_travaux',
                name='Marché de Travaux',
                category=ContractCategory.REAL_ESTATE_CONSTRUCTION,
                keywords=['marché', 'travaux', 'entreprise', 'chantier'],
                legal_codes=['code_construction'],
                priority=2
            ),
            
            # ========== 9. TRANSPORT & LEISURE ==========
            ContractTypeDefinition(
                key='location_vehicule',
                name='Contrat de Location de Véhicule',
                category=ContractCategory.TRANSPORT_LEISURE,
                keywords=['location', 'véhicule', 'voiture', 'loueur'],
                legal_codes=['code_civil_contrats'],
                priority=2
            ),
            ContractTypeDefinition(
                key='transport_marchandises',
                name='Contrat de Transport de Marchandises',
                category=ContractCategory.TRANSPORT_LEISURE,
                keywords=['transport', 'marchandise', 'transporteur', 'lettre de voiture'],
                legal_codes=['code_commerce_transport'],
                priority=2
            ),
            ContractTypeDefinition(
                key='voyage',
                name='Contrat de Voyage / Séjour',
                category=ContractCategory.TRANSPORT_LEISURE,
                keywords=['voyage', 'séjour', 'agence de voyage', 'forfait touristique'],
                legal_codes=['code_tourisme'],
                priority=2
            ),
            ContractTypeDefinition(
                key='location_saisonniere',
                name='Contrat de Location Saisonnière',
                category=ContractCategory.TRANSPORT_LEISURE,
                keywords=['location saisonnière', 'vacances', 'courte durée'],
                legal_codes=['code_tourisme'],
                priority=2
            ),
            
            # ========== 10. HIGH RISK ==========
            ContractTypeDefinition(
                key='pacte_associes',
                name='Pacte d\'Associés',
                category=ContractCategory.HIGH_RISK,
                keywords=['pacte', 'associés', 'actionnaires', 'parts sociales'],
                legal_codes=['code_commerce'],
                priority=3
            ),
            ContractTypeDefinition(
                key='statuts_societe',
                name='Statuts de Société',
                category=ContractCategory.HIGH_RISK,
                keywords=['statuts', 'sas', 'sarl', 'société', 'capital social'],
                legal_codes=['code_commerce'],
                priority=3
            ),
            ContractTypeDefinition(
                key='investissement',
                name='Contrat d\'Investissement',
                category=ContractCategory.HIGH_RISK,
                keywords=['investissement', 'investisseur', 'levée de fonds', 'equity'],
                legal_codes=['code_monetaire'],
                priority=3
            ),
            ContractTypeDefinition(
                key='pret_particuliers',
                name='Contrat de Prêt entre Particuliers',
                category=ContractCategory.HIGH_RISK,
                keywords=['prêt', 'emprunt', 'particuliers', 'reconnaissance de dette'],
                legal_codes=['code_civil_contrats'],
                priority=2
            ),
            ContractTypeDefinition(
                key='transaction_amiable',
                name='Transaction Amiable',
                category=ContractCategory.HIGH_RISK,
                keywords=['transaction', 'amiable', 'conciliation', 'litige'],
                legal_codes=['code_civil_contrats'],
                priority=2
            ),
            
            # ========== 11. INTERNATIONAL ==========
            ContractTypeDefinition(
                key='commercial_international',
                name='Contrat Commercial International',
                category=ContractCategory.INTERNATIONAL,
                keywords=['international', 'export', 'import', 'incoterms'],
                legal_codes=['convention_vienne'],
                priority=2
            ),
            
            # ========== 12. SUBCONTRACTING (ALL TYPES) ==========
            ContractTypeDefinition(
                key='soustraitance_generale',
                name='Contrat de Sous-traitance',
                category=ContractCategory.SUBCONTRACTING,
                keywords=['sous-traitance', 'sous-traitant', 'donneur d\'ordre', 'cotraitance'],
                legal_codes=['code_travail_soustraitance', 'code_civil_contrats'],
                priority=1
            ),
        ]
    
    def _build_legal_database(self) -> Dict[str, List[LegalReference]]:
        """Build legal references database (simplified for now)"""
            # ========== 8. INSURANCE CONTRACTS (NEW) ==========
            ContractTypeDefinition(
                key='assurance_habitation',
                name='Assurance Habitation (MRH)',
                category=ContractCategory.DAILY_INSURANCE,
                keywords=['multirisque habitation', 'mrh', 'dégât des eaux', 'incendie', 'vol', 'catastrophes naturelles', 'résidence principale'],
                legal_codes=['code_assurances'],
                priority=2
            ),
            ContractTypeDefinition(
                key='assurance_auto',
                name='Assurance Auto / Moto',
                category=ContractCategory.DAILY_INSURANCE,
                keywords=['assurance auto', 'bonus-malus', 'responsabilité civile', 'bris de glace', 'tiers collision', 'conducteur principal', 'carte verte', 'véhicule assuré'],
                legal_codes=['code_assurances', 'code_route'],
                priority=2
            ),
            ContractTypeDefinition(
                key='assurance_sante',
                name='Assurance Santé / Mutuelle',
                category=ContractCategory.DAILY_INSURANCE,
                keywords=['mutuelle', 'complémentaire santé', 'ticket modérateur', 'télétransmission', 'noemie', 'soins courants', 'dentaire', 'optique', 'remboursement sécu'],
                legal_codes=['code_assurances', 'code_securite_sociale'],
                priority=2
            ),
            ContractTypeDefinition(
                key='assurance_prevoyance',
                name='Assurance Prévoyance / Décès',
                category=ContractCategory.DAILY_INSURANCE,
                keywords=['prévoyance', 'capital décès', 'incapacité', 'invalidité', 'rente', 'bénéficiaire', 'accident de la vie'],
                legal_codes=['code_assurances'],
                priority=2
            ),
            ContractTypeDefinition(
                key='assurance_emprunteur',
                name='Assurance Emprunteur',
                category=ContractCategory.DAILY_INSURANCE,
                keywords=['assurance emprunteur', 'assurance prêt', 'perte d\'emploi', 'itt', 'ipt', 'quotité', 'hamon', 'bourquin', 'lemoine'],
                legal_codes=['code_assurances', 'code_consommation'],
                priority=3
            ),
            ContractTypeDefinition(
                key='assurance_scolaire',
                name='Assurance Scolaire',
                category=ContractCategory.DAILY_INSURANCE,
                keywords=['assurance scolaire', 'extra-scolaire', 'responsabilité civile enfant', 'dommages corporels', 'activités scolaires'],
                legal_codes=['code_assurances'],
                priority=3
            ),
            ContractTypeDefinition(
                key='protection_juridique',
                name='Protection Juridique',
                category=ContractCategory.DAILY_INSURANCE,
                keywords=['protection juridique', 'frais d\'avocat', 'litige', 'défense pénale', 'recours amiable', 'seuil d\'intervention'],
                legal_codes=['code_assurances'],
                priority=2
            ),
            ContractTypeDefinition(
                key='assurance_rc_pro',
                name='Assurance RC Pro',
                category=ContractCategory.DAILY_INSURANCE,
                keywords=['responsabilité civile professionnelle', 'rc pro', 'dommages causés aux tiers', 'exploitation', 'faute professionnelle'],
                legal_codes=['code_assurances'],
                priority=2
            ),

        ]

    def _build_legal_database(self) -> Dict[str, List[LegalReference]]:
        """Build database of legal references"""
        return {
            'loi_89_462': [
                LegalReference('Loi 89-462', 'Article 1', 'Bail d\'habitation', 
                             'Régit les locations à usage d\'habitation')
            ],
            'code_travail_cdi': [
                LegalReference('Code du Travail', 'L1221-1', 'Contrat de travail',
                             'Règles applicables au CDI'),
                LegalReference('Code du Travail', 'L1231-1', 'Rupture CDI',
                             'Liberté de rupture du CDI sous conditions (licenciement, démission)')
            ],
            'code_assurances': [
                LegalReference('Code des Assurances', 'L112-1', 'Contrat d\'assurance',
                             'Le contrat doit être rédigé par écrit, en français et en caractères apparents.'),
                LegalReference('Code des Assurances', 'L113-1', 'Obligations',
                             'Obligation de payer la prime et de déclarer les risques exacts.'),
                LegalReference('Code des Assurances', 'L113-2', 'Déclaration',
                             'L\'assuré doit déclarer tout sinistre de nature à entraîner la garantie.'),
                LegalReference('Code des Assurances', 'L113-12', 'Résiliation',
                             'Droit de résiliation annuelle à l\'échéance avec préavis de 2 mois.'),
                LegalReference('Code des Assurances', 'L113-15-2', 'Loi Hamon',
                             'Droit de résiliation infra-annuelle après 1 an de contrat (auto/habitation).')
            ],
            'code_consommation': [
                LegalReference('Code de la Consommation', 'L221-18', 'Droit de Rétractation',
                             'Délai de 14 jours pour se rétracter d\'un contrat conclu à distance ou hors établissement.'),
                LegalReference('Code de la Consommation', 'L217-4', 'Garantie de Conformité',
                             'Le vendeur doit livrer un bien conforme au contrat et répond des défauts de conformité existant lors de la délivrance (2 ans).'),
                LegalReference('Code de la Consommation', 'L212-1', 'Clauses Abusives',
                             'Sont abusives les clauses qui créent un déséquilibre significatif entre les droits et obligations des parties.'),
                LegalReference('Code de la Consommation', 'L215-1', 'Loi Chatel',
                             'Le professionnel doit informer le consommateur de la possibilité de ne pas reconduire un contrat tacitement reconductible.'),
                LegalReference('Code de la Consommation', 'L312-1', 'Loi Scrivener (Crédit)',
                             'Obligation d\'information précontractuelle et maintien de l\'offre de crédit pendant 15 jours.')
            ],
            'code_route': [
                LegalReference('Code de la Route', 'L211-1', 'Obligation d\'assurance',
                             'Tout véhicule terrestre à moteur doit être assuré (RC obligatoire).')
            ],
            'code_securite_sociale': [
                LegalReference('Code de la Sécurité Sociale', 'L871-1', 'Contrat Responsable',
                             'Respect des plafonds et planchers de remboursement pour la fiscalité avantageuse.')
            ]
        }
    
    def detect_contract_type(self, text: str) -> Tuple[str, float, str, ContractCategory]:
        """
        Detect contract type from text using intelligent keyword matching
        
        Returns:
            (contract_key, confidence_score, contract_name, category)
        """
        text_lower = text.lower()
        scores = []
        
        for contract_def in self.contract_types:
            score = 0
            matches = []
            
            # Count keyword matches
            for keyword in contract_def.keywords:
                if keyword.lower() in text_lower:
                    score += 1
                    matches.append(keyword)
            
            if score > 0:
                # Normalize by number of keywords
                confidence = (score / len(contract_def.keywords)) * contract_def.priority
                scores.append({
                    'key': contract_def.key,
                    'name': contract_def.name,
                    'category': contract_def.category,
                    'confidence': min(1.0, confidence),
                    'matches': matches
                })
        
        # Get best match
        if not scores:
            return ('prestation_services', 0.5, 'Contrat de Prestation de Services', 
                   ContractCategory.FREELANCE)
        
        best = max(scores, key=lambda x: x['confidence'])
        return (best['key'], best['confidence'], best['name'], best['category'])
    
    def get_legal_references(self, contract_key: str) -> List[LegalReference]:
        """Get legal references for a contract type"""
        # Find contract definition
        contract_def = next((c for c in self.contract_types if c.key == contract_key), None)
        if not contract_def:
            return []
        
        # Collect references
        references = []
        for code in contract_def.legal_codes:
            if code in self.legal_references:
                references.extend(self.legal_references[code])
        
        return references[:6]
    
    def get_all_contract_types(self) -> List[Dict]:
        """Get list of all supported contract types"""
        return [
            {
                'key': c.key,
                'name': c.name,
                'category': c.category.value,
                'keywords_count': len(c.keywords)
            }
            for c in self.contract_types
        ]

# Singleton
contract_detector = ComprehensiveContractDetector()
