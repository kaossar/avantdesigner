"""
Integration tests for the complete pipeline
"""

import pytest
from pipeline import ContractAIPipeline

class TestPipeline:
    """Integration tests for contract analysis pipeline"""
    
    @pytest.fixture
    def pipeline(self):
        """Fixture for pipeline instance"""
        return ContractAIPipeline()
    
    @pytest.mark.asyncio
    async def test_full_pipeline_bail(self, pipeline):
        """Test complete pipeline with bail contract"""
        text = """
CONTRAT DE BAIL D'HABITATION

Article 1 - Objet
Le bailleur loue au locataire un appartement situé à Paris.

Article 2 - Loyer
Le loyer mensuel est de 1200 euros, payable le 1er de chaque mois.

Article 3 - Dépôt de garantie
Un dépôt de garantie de 1200 euros est demandé.

Article 4 - Durée
Le bail est conclu pour une durée de 3 ans.
"""
        
        result = await pipeline.process(text)
        
        # Check structure
        assert "contract_type" in result
        assert "clauses" in result
        assert "risks" in result
        assert "score" in result
        assert "recommendations" in result
        
        # Check contract type detection
        assert "Bail" in result["contract_type"]
        
        # Check clauses analysis
        assert len(result["clauses"]) >= 3
        
        # Check score structure
        assert "global" in result["score"]
        assert 0 <= result["score"]["global"] <= 100
    
    @pytest.mark.asyncio
    async def test_pipeline_with_cleaning(self, pipeline):
        """Test pipeline with text that needs cleaning"""
        text = """
Page 1
Header Company Name
Contract text here
Page 2
Header Company Name
More contract text
"""
        
        result = await pipeline.process(text)
        
        # Check cleaning metadata
        assert "metadata" in result
        assert "cleaning_stats" in result["metadata"]
        assert result["metadata"]["cleaning_stats"]["reduction_percent"] >= 0
    
    @pytest.mark.asyncio
    async def test_entity_extraction(self, pipeline):
        """Test entity extraction"""
        text = "Le loyer est de 800 euros. Date: 01/01/2024. Durée: 12 mois."
        
        result = await pipeline.process(text)
        
        assert "entities" in result
        assert "montants" in result["entities"]
        assert "dates" in result["entities"]
        assert "durees" in result["entities"]
    
    @pytest.mark.asyncio
    async def test_risk_detection(self, pipeline):
        """Test risk detection"""
        text = """
Article 1
Cette clause est illégale et abusive.

Article 2
Clause normale et conforme.
"""
        
        result = await pipeline.process(text)
        
        # Should detect at least one risk
        assert len(result["risks"]) > 0
        assert result["risks"][0]["severity"] in ["low", "medium", "high"]
    
    @pytest.mark.asyncio
    async def test_recommendations_generation(self, pipeline):
        """Test recommendations generation"""
        text = "Article 1\nClause standard."
        
        result = await pipeline.process(text)
        
        assert "recommendations" in result
        assert len(result["recommendations"]) > 0
        assert "priority" in result["recommendations"][0]
        assert "action" in result["recommendations"][0]
