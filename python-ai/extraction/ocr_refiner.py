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
        
        # 🔒 LEGAL-GRADE SAFETY CHECK
        if not self._is_safe_refinement(paragraph, refined):
            logger.warning("⚠️ Unsafe AI refinement detected, reverting to original")
            return paragraph, [{'type': 'rejected', 'reason': 'unsafe_divergence'}]
        
        # Detect changes
        changes = self._detect_changes(paragraph, refined)
        
        return refined, changes
    
    def _is_safe_refinement(self, original: str, refined: str) -> bool:
        """
        🔒 LEGAL-GRADE SAFETY CHECK
        Rejects refinement if it diverges too much or modifies critical legal terms
        """
        if original == refined:
            return True
        
        # 1. Length must be quasi-identical (max 5% difference)
        len_ratio = min(len(original), len(refined)) / max(len(original), len(refined))
        if len_ratio < 0.95:
            logger.warning(f"⚠️ Length divergence: {len_ratio:.2%}")
            return False
        
        # 2. Critical legal terms must be unchanged
        critical_terms = [
            # Négations
            "ne", "pas", "aucun", "jamais", "sans",
            # Modaux juridiques
            "doit", "peut", "pourra", "devra",
            # Obligations
            "obligatoire", "interdit", "autorisé", "requis",
            # Temporalité
            "avant", "après", "pendant", "jusqu'à",
            # Conditions
            "si", "sauf", "excepté", "sous réserve"
        ]
        
        original_lower = original.lower()
        refined_lower = refined.lower()
        
        for term in critical_terms:
            original_count = original_lower.count(term)
            refined_count = refined_lower.count(term)
            
            if original_count != refined_count:
                logger.warning(f"⚠️ Critical term '{term}' count changed: {original_count} → {refined_count}")
                return False
        
        # 3. Word count must be very similar (max 10% difference)
        original_words = len(original.split())
        refined_words = len(refined.split())
        word_ratio = min(original_words, refined_words) / max(original_words, refined_words)
        
        if word_ratio < 0.90:
            logger.warning(f"⚠️ Word count divergence: {original_words} → {refined_words}")
            return False
        
        return True
    
    def _detect_changes(self, original: str, refined: str) -> List[Dict]:
        """
        Improved change detection with character-level analysis
        Returns detailed change information for transparency
        """
        changes = []
        
        if original == refined:
            return changes
        
        # 1. Character-level diff
        char_changes = 0
        for i, (c1, c2) in enumerate(zip(original, refined)):
            if c1 != c2:
                char_changes += 1
        
        # Account for length difference
        char_changes += abs(len(original) - len(refined))
        
        change_ratio = char_changes / max(len(original), len(refined))
        
        changes.append({
            'type': 'character_diff',
            'chars_changed': char_changes,
            'change_ratio': round(change_ratio, 3),
            'severity': 'high' if change_ratio > 0.1 else 'medium' if change_ratio > 0.05 else 'low'
        })
        
        # 2. Word-level diff
        original_words = original.split()
        refined_words = refined.split()
        
        if len(original_words) != len(refined_words):
            changes.append({
                'type': 'structure',
                'severity': 'high',
                'original_words': len(original_words),
                'refined_words': len(refined_words)
            })
        
        # 3. Punctuation changes
        original_punct = sum(1 for c in original if c in '.,;:!?')
        refined_punct = sum(1 for c in refined if c in '.,;:!?')
        
        if original_punct != refined_punct:
            changes.append({
                'type': 'punctuation',
                'severity': 'low',
                'original_count': original_punct,
                'refined_count': refined_punct
            })
        
        # 4. Sample of actual changes (first 200 chars)
        if original[:200] != refined[:200]:
            changes.append({
                'type': 'text_sample',
                'original': original[:200],
                'refined': refined[:200]
            })
        
        return changes
    
    def _calculate_confidence(self, original: str, refined: str) -> float:
        """
        Conservative confidence scoring for legal-grade refinement
        Lower scores = more prudent
        """
        if original == refined:
            return 1.0
        
        # Check if refinement passed safety check
        if not self._is_safe_refinement(original, refined):
            return 0.3  # Low confidence for unsafe refinement
        
        # Calculate change magnitude
        char_changes = sum(1 for c1, c2 in zip(original, refined) if c1 != c2)
        char_changes += abs(len(original) - len(refined))
        change_ratio = char_changes / max(len(original), len(refined))
        
        # Conservative scoring
        if change_ratio < 0.02:  # < 2% change (mostly accents/punctuation)
            return 0.8
        elif change_ratio < 0.05:  # < 5% change
            return 0.7
        elif change_ratio < 0.10:  # < 10% change
            return 0.6
        else:
            return 0.5  # Significant changes = lower confidence

    
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
