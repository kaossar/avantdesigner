"""
Legal-Grade OCR Text Refinement with HuggingFace Inference API
Couche 2 : AI Grammar Correction (SAFE & LIGHTWEIGHT)
"""
import requests
from typing import Dict, List
import logging
import os

logger = logging.getLogger(__name__)

class OCRTextRefiner:
    """
    AI-powered text refinement for OCR output using HuggingFace Inference API
    STRICT: Only corrects grammar/spelling, never rewrites legal content
    NO LOCAL MODEL DOWNLOAD REQUIRED
    """
    
    def __init__(self):
        self.model_name = "pszemraj/flan-t5-base-grammar-synthesis"
        self.api_url = f"https://api-inference.huggingface.co/models/{self.model_name}"
        self.api_token = os.getenv("HUGGINGFACE_API_TOKEN", "")  # Optional, works without token but slower
        
        # Strict prompt to prevent creative rewriting
        self.system_prompt = """Corrige uniquement les fautes d'orthographe, de ponctuation et les erreurs typiques d'OCR.

Ne reformule pas les phrases.
Ne modifie pas le sens.
Ne supprime aucune information juridique.
Ne résume pas.

Texte :
"""
    
    def refine_text(self, text: str, timeout: int = 10) -> Dict:
        """
        Refine text using AI grammar correction via HuggingFace API
        
        Args:
            text: Cleaned text from Couche 1
            timeout: API timeout in seconds
        
        Returns:
            {
                'original': original text,
                'refined': AI-corrected text,
                'changes': list of changes made,
                'confidence': confidence score,
                'used_ai': whether AI was used (False if fallback)
            }
        """
        # If no API token and text is too long, skip AI refinement
        if not self.api_token and len(text) > 1000:
            logger.warning("⚠️ No HuggingFace API token, skipping AI refinement for long text")
            return self._fallback_response(text)
        
        try:
            # Split into paragraphs to avoid token limit
            paragraphs = text.split('\n\n')
            refined_paragraphs = []
            all_changes = []
            
            for i, para in enumerate(paragraphs):
                if not para.strip():
                    refined_paragraphs.append(para)
                    continue
                
                # Limit to first 5 paragraphs for free tier
                if i >= 5 and not self.api_token:
                    logger.info(f"⚠️ Skipping paragraph {i+1}+ (no API token)")
                    refined_paragraphs.append(para)
                    continue
                
                # Refine paragraph
                try:
                    refined_para, changes = self._refine_paragraph(para, timeout)
                    refined_paragraphs.append(refined_para)
                    all_changes.extend(changes)
                except Exception as e:
                    logger.warning(f"⚠️ Failed to refine paragraph {i+1}: {e}")
                    refined_paragraphs.append(para)  # Fallback to original
            
            refined_text = '\n\n'.join(refined_paragraphs)
            
            return {
                'original': text,
                'refined': refined_text,
                'changes': all_changes,
                'confidence': self._calculate_confidence(text, refined_text),
                'used_ai': len(all_changes) > 0
            }
            
        except Exception as e:
            logger.error(f"❌ Refinement failed: {e}")
            return self._fallback_response(text, error=str(e))
    
    def _refine_paragraph(self, paragraph: str, timeout: int) -> tuple:
        """Refine a single paragraph via API"""
        # Prepare input with strict prompt
        input_text = f"{self.system_prompt}\n{paragraph}"
        
        # Prepare headers
        headers = {}
        if self.api_token:
            headers["Authorization"] = f"Bearer {self.api_token}"
        
        # Call API
        response = requests.post(
            self.api_url,
            headers=headers,
            json={
                "inputs": input_text,
                "parameters": {
                    "max_length": 512,
                    "temperature": 0.3,  # Low = conservative
                    "do_sample": False,  # Deterministic
                    "num_beams": 4
                }
            },
            timeout=timeout
        )
        
        if response.status_code != 200:
            raise Exception(f"API error: {response.status_code} - {response.text}")
        
        # Parse response
        result = response.json()
        
        if isinstance(result, list) and len(result) > 0:
            refined = result[0].get('generated_text', paragraph)
        else:
            refined = paragraph
        
        # Detect changes
        changes = self._detect_changes(paragraph, refined)
        
        return refined, changes
    
    def _detect_changes(self, original: str, refined: str) -> List[Dict]:
        """Detect what changed between original and refined"""
        changes = []
        
        if original == refined:
            return changes
        
        # Simple word-level diff
        original_words = original.split()
        refined_words = refined.split()
        
        if len(original_words) != len(refined_words):
            # Structure changed - might be risky
            changes.append({
                'type': 'structure',
                'severity': 'high',
                'original_words': len(original_words),
                'refined_words': len(refined_words)
            })
        
        # Character-level changes
        changes.append({
            'type': 'text',
            'original': original[:100],
            'refined': refined[:100]
        })
        
        return changes
    
    def _calculate_confidence(self, original: str, refined: str) -> float:
        """Calculate confidence in the refinement"""
        if original == refined:
            return 1.0
        
        # Calculate similarity
        original_len = len(original)
        refined_len = len(refined)
        
        # If length changed significantly, low confidence
        len_ratio = min(original_len, refined_len) / max(original_len, refined_len)
        
        if len_ratio < 0.9:
            return 0.5  # Low confidence
        
        return 0.8  # Moderate confidence
    
    def _fallback_response(self, text: str, error: str = None) -> Dict:
        """Return fallback response when AI refinement fails"""
        return {
            'original': text,
            'refined': text,
            'changes': [],
            'confidence': 0.0,
            'used_ai': False,
            'error': error
        }
    
    def generate_diff(self, original: str, refined: str) -> str:
        """
        Generate user-friendly diff for transparency
        
        Returns markdown diff
        """
        lines = []
        lines.append("### 📝 Modifications apportées\n")
        
        if original == refined:
            lines.append("✅ Aucune modification nécessaire\n")
            return '\n'.join(lines)
        
        # Show first few differences
        original_lines = original.split('\n')
        refined_lines = refined.split('\n')
        
        for i, (orig, ref) in enumerate(zip(original_lines[:5], refined_lines[:5])):
            if orig != ref:
                lines.append(f"**Ligne {i+1} :**")
                lines.append(f"```diff")
                lines.append(f"- {orig}")
                lines.append(f"+ {ref}")
                lines.append(f"```\n")
        
        return '\n'.join(lines)


# Singleton
ocr_refiner = OCRTextRefiner()
