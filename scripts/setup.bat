@echo off
REM Setup script for Smart Report Assistant development environment (Windows)

setlocal enabledelayedexpansion

echo [SETUP] Starting Smart Report Assistant development setup...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [SETUP] ERROR: Python is not installed. Please install Python 3.9+ and try again.
    exit /b 1
)
echo [SETUP] Python found

REM Check if pip is installed
pip --version >nul 2>&1
if errorlevel 1 (
    echo [SETUP] ERROR: pip is not installed. Please install pip and try again.
    exit /b 1
)
echo [SETUP] pip found

REM Check if Git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo [SETUP] ERROR: Git is not installed. Please install Git and try again.
    exit /b 1
)
echo [SETUP] Git found

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo [SETUP] WARNING: Docker is not installed. Some features may not work.
    echo [SETUP] INFO: Install Docker from: https://docs.docker.com/get-docker/
) else (
    echo [SETUP] Docker found
)

echo.

REM Install Python dependencies
echo [SETUP] Installing Python dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt
echo [SETUP] Dependencies installed

REM Setup environment file
if not exist .env (
    echo [SETUP] Creating .env file from template...
    copy .env.example .env
    echo [SETUP] INFO: Please edit .env file with your configuration
) else (
    echo [SETUP] INFO: .env file already exists
)

REM Create necessary directories
echo [SETUP] Creating necessary directories...
if not exist app\uploads mkdir app\uploads
if not exist app\static\plots mkdir app\static\plots
echo [SETUP] Directories created

REM Setup pre-commit hooks
echo [SETUP] Setting up pre-commit hooks...
pre-commit install
echo [SETUP] Pre-commit hooks installed

echo.

REM Run initial tests
echo [SETUP] Running initial tests...
python -m pytest tests/ -v --tb=short
if errorlevel 1 (
    echo [SETUP] WARNING: Some tests failed. This might be normal if you haven't configured all dependencies.
)

REM Test Docker build (if available)
docker --version >nul 2>&1
if not errorlevel 1 (
    echo [SETUP] Testing Docker build...
    docker build -t smart-report-assistant-test .
    if not errorlevel 1 (
        echo [SETUP] Docker build successful
        docker rmi smart-report-assistant-test
    ) else (
        echo [SETUP] WARNING: Docker build failed. Check Dockerfile and try again.
    )
) else (
    echo [SETUP] INFO: Skipping Docker test (Docker not available)
)

echo.
echo ======================================
echo [SETUP] Setup completed successfully!
echo ======================================
echo.
echo [SETUP] INFO: Next steps:
echo   1. Edit .env file with your configuration
echo   2. Run the application: python app/main.py
echo   3. Or using Docker: docker-compose up --build
echo   4. Visit: http://localhost:5000
echo.
echo [SETUP] INFO: Development commands:
echo   make test      - Run tests
echo   make lint      - Run linting
echo   make format    - Format code
echo   make ci        - Run all CI checks
echo.
echo [SETUP] INFO: For more information, see:
echo   - README.md
echo   - CICD_GUIDE.md
echo.

pause
