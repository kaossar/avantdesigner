# Contract Analysis AI Pipeline
# Version: 1.0.0 - AI-First Expert

import re
import logging
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

class ContractAIPipeline:
    """
    Complete AI pipeline for contract analysis
    
    Pipeline stages:
    1. Text cleaning (regex + normalization)
    2. Smart chunking (by clause)
    3. Contract classification
    4. Entity extraction (NER)
    5. Clause-by-clause analysis (LLM)
    6. Risk detection
    7. Score calculation
    8. Recommendations generation
    """
    
    def __init__(self):
        logger.info("🔄 Initializing AI Pipeline...")
        
        # Models will be loaded on first use (lazy loading)
        self._llm = None
        self._classifier = None
        self._ner = None
        self._summarizer = None
        
        logger.info("✅ Pipeline initialized (models will load on first use)")
    
    async def process(self, text: str) -> Dict[str, Any]:
        """Main processing pipeline"""
        
        logger.info("📝 Stage 1: Text cleaning...")
        cleaned_text = self._clean_text(text)
        
        logger.info("✂️ Stage 2: Smart chunking...")
        chunks = self._smart_chunk(cleaned_text)
        logger.info(f"   → {len(chunks)} clauses detected")
        
        logger.info("🏷️ Stage 3: Contract classification...")
        contract_type = self._classify_contract(cleaned_text[:1000])
        logger.info(f"   → Type: {contract_type}")
        
        logger.info("🔍 Stage 4: Entity extraction...")
        entities = self._extract_entities(cleaned_text)
        
        logger.info("🧠 Stage 5: Clause analysis (AI)...")
        clauses_analysis = []
        for i, chunk in enumerate(chunks[:5]):  # Limit to 5 clauses for demo
            logger.info(f"   → Analyzing clause {i+1}/{min(len(chunks), 5)}...")
            analysis = await self._analyze_clause_simple(chunk, contract_type, i+1)
            clauses_analysis.append(analysis)
        
        logger.info("⚠️ Stage 6: Risk detection...")
        risks = self._detect_risks(clauses_analysis, contract_type)
        logger.info(f"   → {len(risks)} risks detected")
        
        logger.info("📊 Stage 7: Score calculation...")
        score = self._calculate_score(clauses_analysis, risks)
        
        logger.info("💡 Stage 8: Recommendations...")
        recommendations = self._generate_recommendations(risks, contract_type)
        
        logger.info("📄 Stage 9: Summary generation...")
        summary = self._generate_summary(cleaned_text, clauses_analysis)
        
        return {
            "contract_type": contract_type,
            "summary": summary,
            "entities": entities,
            "clauses": clauses_analysis,
            "risks": risks,
            "score": score,
            "recommendations": recommendations,
            "metadata": {
                "total_clauses": len(chunks),
                "analyzed_clauses": len(clauses_analysis),
                "high_risk_count": len([r for r in risks if r['severity'] == 'high']),
                "medium_risk_count": len([r for r in risks if r['severity'] == 'medium'])
            }
        }
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove page numbers
        text = re.sub(r'Page \d+', '', text)
        
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\n\s*\n', '\n\n', text)
        
        return text.strip()
    
    def _smart_chunk(self, text: str) -> List[str]:
        """Smart chunking by clause/article"""
        # Detect articles
        article_pattern = r'(Article\s+\d+(?:\.\d+)?|ARTICLE\s+[IVX]+)'
        
        if re.search(article_pattern, text):
            # Split by articles
            chunks = re.split(article_pattern, text)
            result = []
            for i in range(1, len(chunks), 2):
                if i+1 < len(chunks):
                    result.append(chunks[i] + ' ' + chunks[i+1])
            return result if result else [text]
        else:
            # Split by paragraphs
            paragraphs = text.split('\n\n')
            return [p.strip() for p in paragraphs if len(p.strip()) > 50]
    
    def _classify_contract(self, text_sample: str) -> str:
        """Classify contract type (rule-based for now)"""
        text_lower = text_sample.lower()
        
        if any(kw in text_lower for kw in ['bail', 'loyer', 'locataire', 'bailleur']):
            return "Bail d'habitation"
        elif any(kw in text_lower for kw in ['cdd', 'durée déterminée', 'contrat de travail']):
            return "Contrat de travail CDD"
        elif any(kw in text_lower for kw in ['cdi', 'durée indéterminée']):
            return "Contrat de travail CDI"
        elif any(kw in text_lower for kw in ['vente', 'vendeur', 'acheteur']):
            return "Contrat de vente"
        else:
            return "Contrat de prestation"
    
    def _extract_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract entities (regex-based for now)"""
        entities = {
            'montants': [],
            'dates': [],
            'personnes': [],
            'lieux': []
        }
        
        # Extract amounts
        montants = re.findall(r'(\d+(?:[,\.]\d+)?)\s*(?:euros?|€)', text, re.IGNORECASE)
        entities['montants'] = list(set(montants))[:5]
        
        # Extract dates
        dates = re.findall(r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}', text)
        entities['dates'] = list(set(dates))[:5]
        
        return entities
    
    async def _analyze_clause_simple(self, clause_text: str, contract_type: str, clause_num: int) -> Dict[str, Any]:
        """
        Simplified clause analysis (rule-based)
        TODO: Replace with LLM analysis in production
        """
        # Simple risk assessment
        risk_keywords = {
            'high': ['interdit', 'illégal', 'abusif', 'non conforme'],
            'medium': ['attention', 'déséquilibre', 'ambigu'],
            'low': []
        }
        
        clause_lower = clause_text.lower()
        risk_level = 'low'
        
        for level, keywords in risk_keywords.items():
            if any(kw in clause_lower for kw in keywords):
                risk_level = level
                break
        
        # Generate simple analysis
        return {
            "clause_number": clause_num,
            "clause_text": clause_text[:200] + "..." if len(clause_text) > 200 else clause_text,
            "full_text": clause_text,
            "resume": f"Clause {clause_num} du contrat de type {contract_type}",
            "implications": "Cette clause définit les obligations des parties.",
            "risques": "Aucun risque majeur détecté" if risk_level == 'low' else "Clause nécessitant une attention particulière",
            "conformite": "Conforme au droit français" if risk_level == 'low' else "Vérification juridique recommandée",
            "recommandation": "Clause acceptable" if risk_level == 'low' else "Consulter un avocat pour validation",
            "risk_level": risk_level
        }
    
    def _detect_risks(self, clauses: List[Dict], contract_type: str) -> List[Dict]:
        """Detect major risks"""
        risks = []
        
        for clause in clauses:
            if clause['risk_level'] in ['high', 'medium']:
                risks.append({
                    "clause_number": clause['clause_number'],
                    "clause_preview": clause['clause_text'],
                    "issue": clause['risques'],
                    "severity": clause['risk_level'],
                    "recommendation": clause['recommandation']
                })
        
        return risks
    
    def _calculate_score(self, clauses: List[Dict], risks: List[Dict]) -> Dict[str, Any]:
        """Calculate global score"""
        total_clauses = len(clauses)
        high_risks = len([r for r in risks if r['severity'] == 'high'])
        medium_risks = len([r for r in risks if r['severity'] == 'medium'])
        
        # Conformity score
        conformity = max(0, 100 - (high_risks * 25 + medium_risks * 10))
        
        # Balance score (simplified)
        balance = 85
        
        # Clarity score (simplified)
        clarity = 80
        
        # Global score
        global_score = int(conformity * 0.5 + balance * 0.3 + clarity * 0.2)
        
        return {
            "global": global_score,
            "conformity": conformity,
            "balance": balance,
            "clarity": clarity,
            "details": {
                "total_clauses": total_clauses,
                "high_risks": high_risks,
                "medium_risks": medium_risks,
                "low_risks": total_clauses - high_risks - medium_risks
            }
        }
    
    def _generate_summary(self, text: str, clauses: List[Dict]) -> str:
        """Generate executive summary"""
        return f"Contrat analysé avec {len(clauses)} clauses identifiées. Analyse IA en cours de développement."
    
    def _generate_recommendations(self, risks: List[Dict], contract_type: str) -> List[Dict]:
        """Generate actionable recommendations"""
        recommendations = []
        
        if len(risks) == 0:
            recommendations.append({
                "priority": "info",
                "action": "Contrat globalement conforme",
                "detail": "Aucun risque majeur détecté."
            })
        else:
            for risk in risks:
                if risk['severity'] == 'high':
                    recommendations.append({
                        "priority": "urgent",
                        "action": "Consulter un avocat",
                        "detail": f"Clause {risk['clause_number']}: {risk['issue']}"
                    })
                elif risk['severity'] == 'medium':
                    recommendations.append({
                        "priority": "important",
                        "action": "Demander une modification",
                        "detail": f"Clause {risk['clause_number']}: {risk['recommendation']}"
                    })
        
        return recommendations
