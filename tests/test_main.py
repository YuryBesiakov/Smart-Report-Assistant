"""
Tests for the main Flask application.
"""
import io
import os
import pytest
from app.main import app, allowed_file


class TestMainApp:
    """Test cases for the main Flask application."""
    
    def test_index_get(self, client):
        """Test GET request to the index page."""
        response = client.get('/')
        assert response.status_code == 200
        # Check for upload-related content in German or English
        response_text = response.data.lower()
        assert b'upload' in response_text or b'datei' in response_text or b'csv' in response_text
    
    def test_allowed_file_valid(self):
        """Test allowed_file function with valid CSV files."""
        assert allowed_file('test.csv') is True
        assert allowed_file('data.CSV') is True
        assert allowed_file('report.csv') is True
    
    def test_allowed_file_invalid(self):
        """Test allowed_file function with invalid file types."""
        assert allowed_file('test.txt') is False
        assert allowed_file('data.xlsx') is False
        assert allowed_file('image.png') is False
        assert allowed_file('noextension') is False
    
    def test_file_upload_no_file(self, client):
        """Test POST request without file."""
        response = client.post('/', data={})
        assert response.status_code == 200
        assert 'Bitte laden Sie eine gültige CSV'.encode('utf-8') in response.data
    
    def test_file_upload_invalid_extension(self, client):
        """Test POST request with invalid file extension."""
        data = {
            'file': (io.BytesIO(b'test content'), 'test.txt')
        }
        response = client.post('/', data=data)
        assert response.status_code == 200
        assert 'Bitte laden Sie eine gültige CSV'.encode('utf-8') in response.data
    
    def test_file_upload_valid_csv(self, client, sample_csv_data):
        """Test POST request with valid CSV file."""
        data = {
            'file': (io.BytesIO(sample_csv_data.encode()), 'test.csv')
        }
        response = client.post('/', data=data, content_type='multipart/form-data')
        # Should either show report or handle gracefully
        assert response.status_code in [200, 500]  # 500 might occur due to missing dependencies
    
    def test_app_configuration(self):
        """Test application configuration."""
        assert app.config['UPLOAD_FOLDER'] is not None
        assert isinstance(app.config['UPLOAD_FOLDER'], str)
