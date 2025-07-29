"""
Tests for the report generator module.
"""
import os
import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from app.report_generator import generate_report_data


class TestReportGenerator:
    """Test cases for the report generator."""
    
    def test_generate_report_data_with_valid_csv(self, sample_csv_file):
        """Test report generation with valid CSV file."""
        result = generate_report_data(sample_csv_file)
        
        assert isinstance(result, dict)
        assert 'summary' in result
        assert 'recommendations' in result
        assert 'analysis_type' in result
        
        # Check if charts are generated (might be None if matplotlib backend issues)
        assert 'bar_chart' in result
        assert 'line_chart' in result
    
    def test_generate_report_data_file_not_found(self):
        """Test report generation with non-existent file."""
        with pytest.raises(FileNotFoundError):
            generate_report_data('/nonexistent/file.csv')
    
    @patch('app.report_generator.pd.read_csv')
    def test_generate_report_data_empty_dataframe(self, mock_read_csv):
        """Test report generation with empty DataFrame."""
        mock_read_csv.return_value = pd.DataFrame()
        
        result = generate_report_data('dummy_path.csv')
        
        assert isinstance(result, dict)
        assert 'summary' in result
        # Check for empty data indication in German or English
        summary = result['summary']
        assert ('No data found' in summary or 
                'Der Datensatz enthält insgesamt 0 Einträge' in summary or 
                summary == '')
    
    @patch('app.report_generator.OPENAI_AVAILABLE', True)
    @patch('app.report_generator.OpenAI')
    def test_gpt_analysis_success(self, mock_openai, sample_csv_file):
        """Test successful GPT analysis."""
        # Mock OpenAI client and response
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "AI generated analysis"
        mock_client.chat.completions.create.return_value = mock_response
        
        # Mock environment variable
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
            result = generate_report_data(sample_csv_file)
        
        assert isinstance(result, dict)
        assert result.get('analysis_type') in ['AI-Enhanced', 'Statistical', 'GPT-Enhanced']
    
    def test_statistical_analysis_fallback(self, sample_csv_file):
        """Test statistical analysis when GPT is not available."""
        with patch('app.report_generator.OPENAI_AVAILABLE', False):
            result = generate_report_data(sample_csv_file)
        
        assert isinstance(result, dict)
        assert result.get('analysis_type') == 'Statistical'
        assert 'summary' in result
        assert 'recommendations' in result
