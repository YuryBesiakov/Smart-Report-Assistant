#!/bin/bash
# Setup script for Smart Report Assistant development environment

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
log() {
    echo -e "${GREEN}[SETUP] $1${NC}"
}

warn() {
    echo -e "${YELLOW}[SETUP] WARNING: $1${NC}"
}

error() {
    echo -e "${RED}[SETUP] ERROR: $1${NC}"
}

info() {
    echo -e "${BLUE}[SETUP] INFO: $1${NC}"
}

# Check if Python is installed
check_python() {
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
        log "Python $PYTHON_VERSION found ✓"
    else
        error "Python 3 is not installed. Please install Python 3.9+ and try again."
        exit 1
    fi
}

# Check if pip is installed
check_pip() {
    if command -v pip3 &> /dev/null; then
        log "pip3 found ✓"
    else
        error "pip3 is not installed. Please install pip and try again."
        exit 1
    fi
}

# Check if Docker is installed
check_docker() {
    if command -v docker &> /dev/null; then
        log "Docker found ✓"
        if ! docker info &> /dev/null; then
            warn "Docker is installed but not running. Please start Docker."
        fi
    else
        warn "Docker is not installed. Some features may not work."
        info "Install Docker from: https://docs.docker.com/get-docker/"
    fi
}

# Check if Git is installed
check_git() {
    if command -v git &> /dev/null; then
        log "Git found ✓"
    else
        error "Git is not installed. Please install Git and try again."
        exit 1
    fi
}

# Install Python dependencies
install_dependencies() {
    log "Installing Python dependencies..."
    
    # Upgrade pip
    python3 -m pip install --upgrade pip
    
    # Install production dependencies
    pip3 install -r requirements.txt
    
    # Install development dependencies
    pip3 install -r requirements-dev.txt
    
    log "Dependencies installed ✓"
}

# Setup environment file
setup_environment() {
    if [ ! -f .env ]; then
        log "Creating .env file from template..."
        cp .env.example .env
        info "Please edit .env file with your configuration:"
        info "  - Add your OpenAI API key (optional)"
        info "  - Configure other settings as needed"
    else
        info ".env file already exists ✓"
    fi
}

# Setup pre-commit hooks
setup_pre_commit() {
    log "Setting up pre-commit hooks..."
    pre-commit install
    log "Pre-commit hooks installed ✓"
}

# Create necessary directories
create_directories() {
    log "Creating necessary directories..."
    mkdir -p app/uploads
    mkdir -p app/static/plots
    log "Directories created ✓"
}

# Run initial tests
run_tests() {
    log "Running initial tests..."
    if python3 -m pytest tests/ -v --tb=short; then
        log "All tests passed ✓"
    else
        warn "Some tests failed. This might be normal if you haven't configured all dependencies."
    fi
}

# Test Docker build
test_docker() {
    if command -v docker &> /dev/null && docker info &> /dev/null; then
        log "Testing Docker build..."
        if docker build -t smart-report-assistant-test .; then
            log "Docker build successful ✓"
            docker rmi smart-report-assistant-test
        else
            warn "Docker build failed. Check Dockerfile and try again."
        fi
    else
        info "Skipping Docker test (Docker not available)"
    fi
}

# Display setup summary
display_summary() {
    echo ""
    echo "======================================"
    log "Setup completed successfully! 🚀"
    echo "======================================"
    echo ""
    info "Next steps:"
    echo "  1. Edit .env file with your configuration"
    echo "  2. Run the application: python app/main.py"
    echo "  3. Or using Docker: docker-compose up --build"
    echo "  4. Visit: http://localhost:5000"
    echo ""
    info "Development commands:"
    echo "  make test      - Run tests"
    echo "  make lint      - Run linting"
    echo "  make format    - Format code"
    echo "  make ci        - Run all CI checks"
    echo ""
    info "For more information, see:"
    echo "  - README.md"
    echo "  - CICD_GUIDE.md"
    echo "  - Documentation in docs/"
    echo ""
}

# Main setup function
main() {
    log "Starting Smart Report Assistant development setup..."
    echo ""
    
    # Check prerequisites
    check_python
    check_pip
    check_git
    check_docker
    
    echo ""
    
    # Setup environment
    install_dependencies
    setup_environment
    create_directories
    setup_pre_commit
    
    echo ""
    
    # Run tests
    run_tests
    test_docker
    
    # Display summary
    display_summary
}

# Run main function
main "$@"
