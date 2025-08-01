"""
Integration tests for GPT functionality.

These tests require a real OpenAI API key and make actual API calls.
Run with: pytest -m integration
Skip with: pytest -m "not integration"
"""

import os
import pytest
import pandas as pd
from app.report_generator import generate_summary_gpt, read_csv
from dotenv import load_dotenv


class TestGPTIntegration:
    """Integration tests for GPT functionality with real API calls."""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Load environment variables for each test."""
        load_dotenv()
    
    @pytest.mark.integration
    @pytest.mark.skipif(
        not os.getenv('OPENAI_API_KEY') or os.getenv('OPENAI_API_KEY') == 'your-openai-api-key-here',
        reason="No valid OpenAI API key configured"
    )
    def test_gpt_integration_with_example_data(self):
        """Test GPT integration with the example dataset using real API calls."""
        # Load example data
        example_file = 'data/beispiel.csv'
        if not os.path.exists(example_file):
            pytest.skip(f"Example file {example_file} not found")
        
        df = read_csv(example_file)
        assert len(df) > 0, "Example dataset should not be empty"
        
        # Test GPT analysis with real API call
        result = generate_summary_gpt(df)
        
        # Validate result structure
        assert isinstance(result, dict), "Result should be a dictionary"
        assert 'summary' in result, "Result should contain summary"
        assert 'recommendations' in result, "Result should contain recommendations"
        
        # Validate content quality
        summary = result.get('summary', '')
        recommendations = result.get('recommendations', '')
        
        assert len(summary) > 0, "Summary should not be empty"
        assert len(recommendations) > 0, "Recommendations should not be empty"
        
        # Basic content validation (GPT should generate meaningful content)
        assert len(summary.split()) > 10, "Summary should be substantial"
        assert len(recommendations.split()) > 10, "Recommendations should be substantial"
        
        print("✅ GPT Integration Test Results:")
        print("-" * 50)
        print(f"📋 Summary ({len(summary)} chars):")
        print(summary[:200] + "..." if len(summary) > 200 else summary)
        print(f"\n💡 Recommendations ({len(recommendations)} chars):")
        print(recommendations[:200] + "..." if len(recommendations) > 200 else recommendations)
        print("-" * 50)
    
    @pytest.mark.integration
    @pytest.mark.skipif(
        not os.getenv('OPENAI_API_KEY') or os.getenv('OPENAI_API_KEY') == 'your-openai-api-key-here',
        reason="No valid OpenAI API key configured"
    )
    def test_gpt_api_key_validation(self):
        """Test that the API key is properly configured and accessible."""
        api_key = os.getenv('OPENAI_API_KEY')
        
        # Validate API key format
        assert api_key is not None, "API key should be set"
        assert api_key != 'your-openai-api-key-here', "API key should be real, not placeholder"
        assert api_key.startswith('sk-'), "OpenAI API key should start with 'sk-'"
        assert len(api_key) > 20, "API key should be of reasonable length"
        
        print(f"✅ API key found: {api_key[:10]}...")
    
    @pytest.mark.integration  
    @pytest.mark.skipif(
        not os.getenv('OPENAI_API_KEY') or os.getenv('OPENAI_API_KEY') == 'your-openai-api-key-here',
        reason="No valid OpenAI API key configured"
    )
    def test_gpt_with_minimal_data(self):
        """Test GPT analysis with minimal dataset."""
        # Create minimal test data
        minimal_data = pd.DataFrame({
            'Date': ['2024-01-01', '2024-01-02'],
            'RiskCategory': ['Operational', 'Credit'],
            'Risikoscore': [25.5, 30.2],
            'Verluste': [1000, 1500],  
            'Kundenzahlen': [100, 150]
        })
        minimal_data['Date'] = pd.to_datetime(minimal_data['Date'])
        
        result = generate_summary_gpt(minimal_data)
        
        assert isinstance(result, dict)
        assert 'summary' in result
        assert 'recommendations' in result
        assert len(result['summary']) > 0
        assert len(result['recommendations']) > 0
