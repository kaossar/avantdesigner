"""
AI Model Service - Sprint 3
Manages loading and inference for specialized NLP models:
- Mistral-7B (via Hugging Face API or Local)
- CamemBERT (Classification & NER)
- BARThez (Summarization)
"""

import os
import logging
from typing import Dict, Any, List, Optional
from transformers import pipeline, AutoTokenizer, AutoModelForTokenClassification, AutoModelForSequenceClassification

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIModelService:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AIModelService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        self.hf_token = os.getenv("HUGGINGFACE_API_KEY")
        self.device = -1 # CPU by default, change to 0 for GPU
        
        # Lazy loading of models
        self.ner_pipeline = None
        self.classifier_pipeline = None
        self.summarizer_pipeline = None
        
        self._initialized = True
        logger.info("🤖 AI Model Service Initialized")

    def load_ner_model(self):
        """Load CamemBERT for NER (Entities)"""
        if not self.ner_pipeline:
            logger.info("⏳ Loading CamemBERT NER model...")
            try:
                # Using a lighter model for dev/local: Jean-Baptiste/camembert-ner
                self.ner_pipeline = pipeline(
                    "ner", 
                    model="Jean-Baptiste/camembert-ner", 
                    tokenizer="Jean-Baptiste/camembert-ner",
                    aggregation_strategy="simple",
                    device=self.device
                )
                logger.info("✅ CamemBERT NER loaded")
            except Exception as e:
                logger.error(f"❌ Failed to load NER model: {e}")

    def load_classifier_model(self):
        """Load CamemBERT for Zero-Shot Classification"""
        if not self.classifier_pipeline:
            logger.info("⏳ Loading CamemBERT Classification model...")
            try:
                self.classifier_pipeline = pipeline(
                    "zero-shot-classification", 
                    model="facebook/bart-large-mnli", # Multi-lingual capable usually, or use specific fr model
                    device=self.device
                )
                logger.info("✅ Classifier loaded")
            except Exception as e:
                logger.error(f"❌ Failed to load Classifier model: {e}")

    def load_summarizer_model(self):
        """Load BARThez for Summarization"""
        if not self.summarizer_pipeline:
            logger.info("⏳ Loading BARThez Summarization model...")
            try:
                self.summarizer_pipeline = pipeline(
                    "summarization", 
                    model="moussaKam/barthez", 
                    tokenizer="moussaKam/barthez",
                    device=self.device
                )
                logger.info("✅ BARThez loaded")
            except Exception as e:
                logger.error(f"❌ Failed to load Summarizer model: {e}")

    def extract_entities(self, text: str) -> List[Dict[str, Any]]:
        """Extract named entities using CamemBERT"""
        self.load_ner_model()
        if not self.ner_pipeline:
            return []
            
        # Limit text length for BERT models
        truncated_text = text[:512] 
        results = self.ner_pipeline(truncated_text)
        
        # specific processing can be added here
        return results

    def classify_contract(self, text: str, candidate_labels: List[str]) -> Dict[str, Any]:
        """Classify contract type using Zero-Shot"""
        self.load_classifier_model()
        if not self.classifier_pipeline:
            return {"labels": [], "scores": []}
            
        truncated_text = text[:1024]
        return self.classifier_pipeline(truncated_text, candidate_labels)

    def summarize_clause(self, text: str) -> str:
        """Summarize legal text using BARThez"""
        self.load_summarizer_model()
        if not self.summarizer_pipeline:
            return text[:200] + "..."
            
        try:
            # Min/Max length relative to input
            input_len = len(text.split())
            if input_len < 30:
                return text
                
            summary = self.summarizer_pipeline(
                text, 
                max_length=min(150, int(input_len * 0.8)), 
                min_length=min(30, int(input_len * 0.3)), 
                do_sample=False
            )
            return summary[0]['summary_text']
        except Exception as e:
            logger.warning(f"Summarization failed: {e}")
            return text[:200] + "..." # Fallback

    def analyze_risk_mistral(self, clause_text: str, clause_type: str, contract_type: str) -> Dict[str, Any]:
        """
        Analyze clause risks using Mistral-7B-Instruct via Hugging Face API
        """
        if not self.hf_token:
            logger.warning("⚠️ No Hugging Face token found. Using keyword fallback.")
            return None

        API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
        headers = {"Authorization": f"Bearer {self.hf_token}"}
        
        prompt = f"""[INST] Tu es un expert juridique français. Analyse la clause suivante extraite d'un {contract_type}.
Type de clause : {clause_type}
Texte : "{clause_text}"

Identifie les risques juridiques potentiels pour le locataire/salarié.
Format de réponse JSON attendu :
{{
  "risk_level": "low" | "medium" | "high",
  "explanation": "explication courte du risque",
  "recommendation": "action recommandée"
}}
Réponds uniquement en JSON valide.
[/INST]"""

        import requests
        try:
            response = requests.post(API_URL, headers=headers, json={"inputs": prompt, "parameters": {"max_new_tokens": 256, "return_full_text": False}})
            
            if response.status_code == 200:
                result = response.json()
                generated_text = result[0]['generated_text']
                
                # Attempt to parse JSON from response (Mistral might add chat text)
                import json
                try:
                    # Find JSON block
                    start = generated_text.find('{')
                    end = generated_text.rfind('}') + 1
                    if start != -1 and end != -1:
                        json_str = generated_text[start:end]
                        return json.loads(json_str)
                except:
                    logger.warning("Failed to parse Mistral JSON response")
            else:
                logger.warning(f"Mistral API Error: {response.status_code}")
                
        except Exception as e:
            logger.error(f"Mistral Inference Failed: {e}")
            
        return None
