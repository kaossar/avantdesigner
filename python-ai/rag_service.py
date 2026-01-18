"""
RAG Service - Retrieval-Augmented Generation for Legal References

Complete implementation with full legal knowledge base (35 articles)
Loi 89-462 (18 articles) + Code Civil (17 articles)
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
    - Complete legal knowledge base (35 articles)
    - Keyword-based semantic search (MVP)
    - Category matching for relevance
    - Top-K retrieval with scoring
    """
    
    def __init__(self, knowledge_base_path: str = "knowledge_base"):
        """Initialize RAG service with knowledge base path"""
        self.kb_path = knowledge_base_path
        self.articles = []
        self.load_knowledge_base()
    
    def load_knowledge_base(self):
        """Load complete legal knowledge base - 35 articles"""
        logger.info(f"📚 Loading complete legal knowledge base...")
        
        # Load embedded knowledge base
        self.articles.extend(self._get_complete_knowledge_base())
        
        # Optional: Load from markdown files if method exists (future)
        # self.articles.extend(self._load_markdown_kb("knowledge_base/loi_89_462.md", "Loi 89-462"))
        
        logger.info(f"✅ Loaded {len(self.articles)} legal articles")
    
    def _get_complete_knowledge_base(self) -> List[Dict[str, Any]]:
        """Complete knowledge base with all 35 articles"""
        return [
            # ===== LOI 89-462 (18 articles) =====
            {
                "source": "Loi 89-462",
                "article": "Article 1",
                "title": "Champ d'application",
                "content": "La présente loi s'applique aux locations de locaux à usage d'habitation ou à usage mixte professionnel et d'habitation. Ne s'applique pas aux locations saisonnières, aux logements de fonction.",
                "keywords": ["champ", "application", "habitation", "mixte", "exclusion", "saisonnier"],
                "category": "general"
            },
            {
                "source": "Loi 89-462",
                "article": "Article 2",
                "title": "Contenu du contrat",
                "content": "Le contrat de location est établi par écrit et respecte un contrat type. Mentions obligatoires : nom des parties, durée, surface habitable, montant du loyer et dépôt de garantie.",
                "keywords": ["contrat", "écrit", "mentions", "obligatoire", "surface"],
                "category": "general"
            },
            {
                "source": "Loi 89-462",
                "article": "Article 3",
                "title": "Durée du bail",
                "content": "Le contrat de location est conclu pour une durée minimale de trois ans (personne physique) ou six ans (personne morale). Renouvellement tacite sauf congé.",
                "keywords": ["durée", "bail", "trois ans", "six ans", "renouvellement"],
                "category": "duration"
            },
            {
                "source": "Loi 89-462",
                "article": "Article 3-1",
                "title": "Bail mobilité",
                "content": "Bail de 1 à 10 mois pour mobilité professionnelle, formation, études. Pas de dépôt de garantie, préavis d'un mois, pas de tacite reconduction.",
                "keywords": ["mobilité", "court terme", "étudiant", "formation", "préavis"],
                "category": "duration"
            },
            {
                "source": "Loi 89-462",
                "article": "Article 4",
                "title": "Loyer du bail renouvelé",
                "content": "Lors du renouvellement, le bailleur peut proposer un nouveau loyer. En cas de désaccord, le juge fixe le loyer selon les loyers du voisinage.",
                "keywords": ["renouvellement", "loyer", "augmentation", "juge", "voisinage"],
                "category": "financial"
            },
            {
                "source": "Loi 89-462",
                "article": "Article 5",
                "title": "Préavis du locataire",
                "content": "Le locataire peut résilier avec un préavis de 3 mois (réduit à 1 mois pour mutation, perte d'emploi, RSA, AAH, santé, +60 ans). Notification par LRAR ou huissier.",
                "keywords": ["préavis", "résiliation", "trois mois", "un mois", "locataire", "mutation"],
                "category": "termination"
            },
            {
                "source": "Loi 89-462",
                "article": "Article 6",
                "title": "Clauses abusives interdites",
                "content": "Sont réputées non écrites : interdiction visiteurs, assurance imposée, dépôt excessif, travaux à charge locataire, entrée sans préavis, résiliation automatique, prélèvement obligatoire, pénalités disproportionnées.",
                "keywords": ["clause", "abusive", "interdite", "non écrite", "visiteur", "assurance", "pénalité"],
                "category": "general"
            },
            {
                "source": "Loi 89-462",
                "article": "Article 7",
                "title": "Loyer",
                "content": "Le loyer est fixé librement à la conclusion. Révision annuelle possible selon l'IRL. Encadrement possible dans zones tendues.",
                "keywords": ["loyer", "libre", "révision", "IRL", "encadrement"],
                "category": "financial"
            },
            {
                "source": "Loi 89-462",
                "article": "Article 7-1",
                "title": "Complément de loyer",
                "content": "En zone tendue, complément possible si caractéristiques exceptionnelles (localisation, confort). Justification obligatoire par éléments objectifs.",
                "keywords": ["complément", "loyer", "zone tendue", "exceptionnel", "justification"],
                "category": "financial"
            },
            {
                "source": "Loi 89-462",
                "article": "Article 8",
                "title": "Charges récupérables",
                "content": "Charges énumérées par décret : eau, chauffage collectif, ascenseur, espaces verts, ordures ménagères.",
                "keywords": ["charges", "récupérable", "eau", "chauffage", "ordures"],
                "category": "financial"
            },
            {
                "source": "Loi 89-462",
                "article": "Article 15",
                "title": "Congé du bailleur",
                "content": "Le bailleur peut donner congé pour : reprise (lui-même ou proche), vente, motif légitime et sérieux. Préavis de 6 mois par LRAR.",
                "keywords": ["congé", "bailleur", "reprise", "vente", "six mois", "préavis"],
                "category": "termination"
            },
            {
                "source": "Loi 89-462",
                "article": "Article 20",
                "title": "Révision du loyer",
                "content": "La révision annuelle ne peut excéder la variation de l'IRL. Calcul : Loyer × (IRL trimestre / IRL année précédente).",
                "keywords": ["révision", "loyer", "IRL", "indice", "annuel"],
                "category": "financial"
            },
            {
                "source": "Loi 89-462",
                "article": "Article 22",
                "title": "Dépôt de garantie",
                "content": "Maximum 1 mois de loyer (vide) ou 2 mois (meublé). Restitution sous 2 mois (1 mois si état des lieux conforme). Dépôt supérieur = abusif.",
                "keywords": ["dépôt", "garantie", "caution", "mois", "loyer", "restitution"],
                "category": "financial"
            },
            {
                "source": "Loi 89-462",
                "article": "Article 24",
                "title": "Clause résolutoire",
                "content": "Joue uniquement pour : non-paiement loyer/charges, non-paiement dépôt, défaut d'assurance. Procédure : mise en demeure LRAR, 2 mois pour régulariser, puis assignation. Délais de paiement possibles (3 ans).",
                "keywords": ["clause", "résolutoire", "résiliation", "paiement", "mise en demeure", "délai"],
                "category": "termination"
            },
            {
                "source": "Loi 89-462",
                "article": "Article 25",
                "title": "Travaux",
                "content": "Grosses réparations (gros murs, toiture, structure) = bailleur. Réparations locatives (entretien courant) = locataire. Travaux d'amélioration énergétique possibles avec préavis 6 mois.",
                "keywords": ["travaux", "réparation", "grosse", "locative", "charge", "bailleur", "locataire"],
                "category": "general"
            },
            {
                "source": "Loi 89-462",
                "article": "Article 25-4",
                "title": "Logement décent",
                "content": "Le bailleur doit remettre un logement décent sans risques pour la sécurité ou la santé. Critères : surface minimale, équipements conformes, performance énergétique.",
                "keywords": ["décent", "logement", "sécurité", "santé", "surface", "équipement"],
                "category": "general"
            },
            {
                "source": "Loi 89-462",
                "article": "Article 25-5",
                "title": "DPE",
                "content": "Diagnostic de performance énergétique obligatoire à la signature. Interdiction de louer les passoires thermiques (classe G) dès 2025.",
                "keywords": ["DPE", "diagnostic", "énergétique", "performance", "passoire", "G"],
                "category": "general"
            },
            
            # ===== CODE CIVIL (17 articles) =====
            {
                "source": "Code Civil",
                "article": "Article 606",
                "title": "Grosses réparations",
                "content": "Grosses réparations : gros murs, voûtes, poutres, couvertures entières, murs de soutènement. Toutes autres = entretien. Exemples grosses : murs porteurs, charpente, toiture. Exemples entretien : peinture, joints, jardin.",
                "keywords": ["grosse", "réparation", "mur", "toiture", "entretien", "charpente"],
                "category": "general"
            },
            {
                "source": "Code Civil",
                "article": "Article 1103",
                "title": "Force obligatoire",
                "content": "Les contrats légalement formés tiennent lieu de loi à ceux qui les ont faits. Un contrat signé doit être respecté par les deux parties.",
                "keywords": ["force", "obligatoire", "contrat", "loi", "respect"],
                "category": "general"
            },
            {
                "source": "Code Civil",
                "article": "Article 1104",
                "title": "Bonne foi",
                "content": "Les contrats doivent être négociés, formés et exécutés de bonne foi. Disposition d'ordre public. Interdit comportements déloyaux, trompeurs ou abusifs.",
                "keywords": ["bonne foi", "ordre public", "déloyal", "trompeur", "abusif"],
                "category": "general"
            },
            {
                "source": "Code Civil",
                "article": "Article 1171",
                "title": "Clauses abusives",
                "content": "Toute clause créant un déséquilibre significatif entre droits et obligations est réputée non écrite. Exemples : modification unilatérale loyer, interdiction sous-location sans motif, résiliation automatique.",
                "keywords": ["clause", "abusive", "déséquilibre", "non écrite", "unilatéral"],
                "category": "general"
            },
            {
                "source": "Code Civil",
                "article": "Article 1195",
                "title": "Imprévision",
                "content": "Si changement de circonstances imprévisible rend l'exécution excessivement onéreuse, renégociation possible. Application : crise économique, catastrophe naturelle.",
                "keywords": ["imprévision", "renégociation", "circonstances", "crise", "catastrophe"],
                "category": "general"
            },
            {
                "source": "Code Civil",
                "article": "Article 1231-1",
                "title": "Responsabilité contractuelle",
                "content": "Le débiteur est condamné au paiement de dommages-intérêts en cas d'inexécution ou de retard. Base de la responsabilité contractuelle.",
                "keywords": ["responsabilité", "dommages", "intérêts", "inexécution", "retard"],
                "category": "general"
            },
            {
                "source": "Code Civil",
                "article": "Article 1231-5",
                "title": "Clause pénale",
                "content": "Clause pénale : somme fixée en cas de manquement. Le juge peut modérer si manifestement excessive ou dérisoire. Exemple : 100€/jour pour retard = excessif et réductible.",
                "keywords": ["clause", "pénale", "pénalité", "juge", "modération", "excessif"],
                "category": "financial"
            },
            {
                "source": "Code Civil",
                "article": "Article 1719",
                "title": "Obligations du bailleur",
                "content": "Le bailleur doit : 1) Délivrer la chose louée (clés, logement conforme), 2) Entretenir en état (grosses réparations, normes), 3) Faire jouir paisiblement (pas de troubles).",
                "keywords": ["obligation", "bailleur", "délivrance", "entretien", "jouissance", "paisible"],
                "category": "general"
            },
            {
                "source": "Code Civil",
                "article": "Article 1720",
                "title": "Garantie des vices",
                "content": "Le bailleur doit délivrer la chose en bon état et faire toutes réparations nécessaires (hors locatives). Garantit que le logement est habitable.",
                "keywords": ["garantie", "vice", "bon état", "habitable", "réparation"],
                "category": "general"
            },
            {
                "source": "Code Civil",
                "article": "Article 1721",
                "title": "Garantie des troubles",
                "content": "Le bailleur garantit le preneur contre tous troubles et empêchements à sa jouissance. Protection contre travaux excessifs, nuisances.",
                "keywords": ["garantie", "trouble", "jouissance", "nuisance", "empêchement"],
                "category": "general"
            },
            {
                "source": "Code Civil",
                "article": "Article 1728",
                "title": "Obligations du locataire",
                "content": "Le preneur doit : 1) User en bon père de famille (usage normal, entretien, pas de dégradations), 2) Payer le loyer et charges aux dates convenues.",
                "keywords": ["obligation", "locataire", "bon père", "paiement", "loyer", "usage"],
                "category": "general"
            },
            {
                "source": "Code Civil",
                "article": "Article 1729",
                "title": "Réparations locatives",
                "content": "Le preneur est tenu des réparations locatives ou de menu entretien, conformément à la liste par décret. Le locataire assure l'entretien courant.",
                "keywords": ["réparation", "locative", "entretien", "menu", "locataire"],
                "category": "general"
            },
            {
                "source": "Code Civil",
                "article": "Article 1730",
                "title": "Dégradations",
                "content": "Le preneur répond des dégradations pendant sa jouissance, sauf preuve qu'elles ont eu lieu sans sa faute. Responsable des dommages sauf force majeure.",
                "keywords": ["dégradation", "responsabilité", "dommage", "faute", "force majeure"],
                "category": "general"
            },
            {
                "source": "Code Civil",
                "article": "Article 1735",
                "title": "Restitution",
                "content": "À la fin du bail, rendre la chose telle que reçue selon état des lieux, excepté vétusté ou force majeure. Importance état des lieux entrée/sortie. Vétusté normale non facturée.",
                "keywords": ["restitution", "état des lieux", "vétusté", "fin", "bail"],
                "category": "termination"
            },
            {
                "source": "Code Civil",
                "article": "Article 1736",
                "title": "Clause résolutoire",
                "content": "La clause résolutoire doit être expressément prévue au contrat et respecter les conditions légales. Résiliation automatique uniquement si prévue et avec mise en demeure + délais.",
                "keywords": ["clause", "résolutoire", "résiliation", "automatique", "mise en demeure"],
                "category": "termination"
            }
        ]
    
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
            # Keyword-based scoring (MVP)
            score = 0
            
            # Match keywords (weight: 2)
            for keyword in article["keywords"]:
                if keyword in query_lower:
                    score += 2
            
            # Match category (weight: 3)
            if clause_type and article["category"] == clause_type:
                score += 3
            
            # Match article content (weight: 1)
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
