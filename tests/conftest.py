"""
Test configuration and fixtures.
"""
import os
import pytest
import tempfile
from app.main import app


@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    # Create a temporary file for testing database
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True
    app.config['UPLOAD_FOLDER'] = tempfile.mkdtemp()
    
    with app.test_client() as client:
        with app.app_context():
            yield client
    
    # Clean up
    os.close(db_fd)
    os.unlink(app.config['DATABASE'])


@pytest.fixture
def sample_csv_data():
    """Sample CSV content for testing."""
    return """Date,Product,Sales,Risk_Level
2023-01-01,ProductA,1000,Low
2023-01-02,ProductB,1500,Medium
2023-01-03,ProductC,800,High
2023-01-04,ProductA,1200,Low
2023-01-05,ProductB,1800,Medium"""


@pytest.fixture
def sample_csv_file(tmp_path, sample_csv_data):
    """Create a temporary CSV file for testing."""
    csv_file = tmp_path / "test_data.csv"
    csv_file.write_text(sample_csv_data)
    return str(csv_file)
