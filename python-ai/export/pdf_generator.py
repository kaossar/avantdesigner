"""
PDF Generator Service - Professional Contract Analysis Reports

Generates professional PDF reports from contract analysis data using pdfkit.
"""

import os
import pdfkit
from jinja2 import Template, Environment, FileSystemLoader
from typing import Dict, Any
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class PDFGenerator:
    """
    Professional PDF report generator for contract analysis
    
    Features:
    - HTML template rendering with Jinja2
    - PDF generation with pdfkit
    - Professional layout with all analysis sections
    - Legal references included
    """
    
    def __init__(self, template_dir: str = "export/templates"):
        """Initialize PDF generator with template directory"""
        self.template_dir = template_dir
        self.env = Environment(loader=FileSystemLoader(template_dir))
        
        # PDF options for professional output
        self.pdf_options = {
            'page-size': 'A4',
            'margin-top': '20mm',
            'margin-right': '20mm',
            'margin-bottom': '20mm',
            'margin-left': '20mm',
            'encoding': 'UTF-8',
            'enable-local-file-access': None,
            'no-outline': None,
            'print-media-type': None,
        }
    
    def generate_report(self, analysis_data: Dict[str, Any]) -> bytes:
        """
        Generate PDF report from analysis data
        
        Args:
            analysis_data: Complete analysis results from pipeline
        
        Returns:
            PDF file as bytes
        """
        logger.info("📄 Generating PDF report...")
        
        try:
            # Load template
            template = self.env.get_template('report.html')
            
            # Prepare data for template
            context = self._prepare_context(analysis_data)
            
            # Render HTML
            html_content = template.render(**context)
            
            # Generate PDF
            pdf_bytes = pdfkit.from_string(
                html_content,
                False,  # Return bytes instead of file
                options=self.pdf_options
            )
            
            logger.info("✅ PDF generated successfully")
            return pdf_bytes
            
        except Exception as e:
            logger.error(f"❌ PDF generation failed: {e}")
            raise
    
    def _prepare_context(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare template context from analysis data"""
        
        # Extract key metrics
        score = analysis_data.get('score', {})
        risks = analysis_data.get('risks', [])
        clauses = analysis_data.get('clauses', [])
        entities = analysis_data.get('entities', {})
        
        # Count risks by level
        risk_counts = {
            'high': len([r for r in risks if r.get('severity') == 'high']),
            'medium': len([r for r in risks if r.get('severity') == 'medium']),
            'low': len([r for r in risks if r.get('severity') == 'low']),
        }
        
        # Get top recommendations
        top_recommendations = [
            r.get('recommendation', '') 
            for r in risks[:3] 
            if r.get('severity') in ['high', 'medium']
        ]
        
        return {
            'report_date': datetime.now().strftime('%d/%m/%Y'),
            'contract_type': analysis_data.get('contract_type', 'Inconnu'),
            'score': score,
            'total_clauses': len(clauses),
            'risk_counts': risk_counts,
            'total_risks': len(risks),
            'top_recommendations': top_recommendations,
            'risks': risks,
            'clauses': clauses,
            'entities': entities,
            'metadata': analysis_data.get('metadata', {}),
        }

# Singleton instance
_pdf_generator = None

def get_pdf_generator() -> PDFGenerator:
    """Get or create PDF generator singleton"""
    global _pdf_generator
    if _pdf_generator is None:
        _pdf_generator = PDFGenerator()
    return _pdf_generator

def generate_pdf_report(analysis_data: Dict[str, Any]) -> bytes:
    """
    Generate PDF report from analysis data
    
    Args:
        analysis_data: Complete analysis results
    
    Returns:
        PDF file as bytes
    """
    generator = get_pdf_generator()
    return generator.generate_report(analysis_data)
