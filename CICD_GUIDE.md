# CI/CD Setup Guide for Smart Report Assistant

This document provides a comprehensive guide to set up and use the CI/CD pipeline for the Smart Report Assistant project.

## 📋 Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Initial Setup](#initial-setup)
- [CI/CD Pipeline](#cicd-pipeline)
- [Development Workflow](#development-workflow)
- [Deployment](#deployment)
- [Monitoring](#monitoring)
- [Troubleshooting](#troubleshooting)

## 🎯 Overview

The CI/CD pipeline provides:

- **Automated Testing**: Unit tests, integration tests, and coverage reporting
- **Code Quality**: Linting, formatting, and security checks
- **Multi-Environment Deployment**: Staging and production environments
- **Docker Support**: Containerized deployment with health checks
- **Security Scanning**: Dependency vulnerability checks and code security analysis

## 🔧 Prerequisites

### Local Development
- Python 3.9+
- Docker Desktop
- Git
- Make (optional, for convenience commands)

### CI/CD Platform (GitHub Actions)
- GitHub repository
- Docker Hub account (for image hosting)
- Cloud provider account (AWS/GCP/Azure) for production deployment

## 🚀 Initial Setup

### 1. Clone and Setup Repository

```bash
git clone https://github.com/YuryBesiakov/Smart-Report-Assistant.git
cd Smart-Report-Assistant
```

### 2. Install Dependencies

```bash
# Install production dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt
```

### 3. Setup Development Environment

```bash
# Using Make (recommended)
make setup

# Or manually
pre-commit install
cp .env.example .env
# Edit .env with your configuration
```

### 4. Configure GitHub Secrets

Add the following secrets to your GitHub repository:

```
DOCKER_USERNAME=your_docker_username
DOCKER_PASSWORD=your_docker_password
OPENAI_API_KEY=your_openai_api_key (optional)
```

## 🔄 CI/CD Pipeline

### Workflow Triggers

- **Push to main**: Full CI/CD pipeline with deployment
- **Push to develop**: CI pipeline without deployment
- **Pull Requests**: CI pipeline for validation
- **Tags (v*)**: Release pipeline with versioned artifacts

### Pipeline Stages

#### 1. **Test Stage**
- Runs on multiple Python versions (3.9, 3.10, 3.11)
- Unit and integration tests with pytest
- Code coverage reporting
- Uploads coverage to Codecov

#### 2. **Security Stage**
- Dependency vulnerability scanning with Safety
- Code security analysis with Bandit
- Generates security reports

#### 3. **Build Stage** (main branch only)
- Builds multi-architecture Docker images
- Pushes to Docker Hub with tags
- Caches layers for faster builds

#### 4. **Deploy Stages**
- **Staging**: Automatic deployment for testing
- **Production**: Manual approval required

### Pipeline Configuration Files

```
.github/
├── workflows/
│   ├── ci.yml          # Main CI/CD pipeline
│   └── release.yml     # Release workflow for tags
```

## 🛠 Development Workflow

### 1. Feature Development

```bash
# Create feature branch
git checkout -b feature/new-feature

# Make changes and test locally
make test
make lint
make format

# Commit and push
git add .
git commit -m "feat: add new feature"
git push origin feature/new-feature
```

### 2. Code Quality Checks

```bash
# Run all quality checks
make ci

# Individual checks
make test          # Run tests
make test-cov      # Run tests with coverage
make lint          # Run linting
make format        # Format code
make security      # Security checks
```

### 3. Pre-commit Hooks

Automatically runs on each commit:
- Code formatting (Black, isort)
- Linting (flake8)
- Type checking (mypy)
- Security checks (bandit)

### 4. Pull Request Process

1. Create feature branch
2. Make changes and ensure tests pass
3. Create pull request to `main`
4. CI pipeline runs automatically
5. Review and merge after approval

## 🚀 Deployment

### Local Development

```bash
# Using Docker Compose
docker-compose up --build

# Using Make
make docker-build
make docker-run

# Using deployment scripts
./scripts/deploy.sh           # Linux/Mac
scripts\deploy.bat            # Windows
```

### Staging Environment

- Automatically deployed on push to `main`
- Environment: `staging`
- URL: Configure in your cloud provider

### Production Environment

- Manual deployment trigger required
- Environment: `production`
- Requires approval in GitHub Actions

### Deployment Commands

```bash
# Deploy to production (after manual approval)
# Triggered automatically via GitHub Actions

# Manual deployment using scripts
./scripts/deploy.sh deploy     # Deploy
./scripts/deploy.sh status     # Check status
./scripts/deploy.sh logs       # View logs
./scripts/deploy.sh stop       # Stop application
./scripts/deploy.sh rollback   # Rollback deployment
```

## 📊 Monitoring

### Application Health

- **Health Check Endpoint**: `/` (returns 200 if healthy)
- **Docker Health Check**: Built into container
- **Monitoring Interval**: 30 seconds

### Logs

```bash
# View application logs
docker logs smart-report-assistant-container

# Follow logs in real-time
./scripts/deploy.sh logs
```

### Metrics

- **Code Coverage**: Available in GitHub Actions and Codecov
- **Security Reports**: Generated in CI pipeline
- **Performance**: Monitor response times and resource usage

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_ENV` | Flask environment | `production` |
| `FLASK_DEBUG` | Debug mode | `0` |
| `OPENAI_API_KEY` | OpenAI API key | None |
| `MAX_CONTENT_LENGTH` | Max upload size | `50MB` |

### Docker Configuration

- **Base Image**: `python:3.11-slim`
- **Port**: `5000`
- **Health Check**: HTTP GET to `/`
- **Restart Policy**: `unless-stopped`

## 🐛 Troubleshooting

### Common Issues

#### 1. **Tests Failing**
```bash
# Run tests locally to debug
pytest tests/ -v --tb=short

# Check for missing dependencies
pip install -r requirements-dev.txt
```

#### 2. **Docker Build Failures**
```bash
# Check Dockerfile syntax
docker build -t test-image .

# View build logs
docker build --no-cache -t test-image .
```

#### 3. **Deployment Issues**
```bash
# Check container status
docker ps -a

# View container logs
docker logs container-name

# Check health endpoint
curl http://localhost:5000/
```

#### 4. **CI/CD Pipeline Failures**

- Check GitHub Actions logs
- Verify secrets are configured
- Ensure Docker Hub credentials are valid
- Check for dependency conflicts

### Debug Commands

```bash
# Local debugging
make clean          # Clean up generated files
make test-cov       # Run tests with coverage
make docker-build   # Test Docker build locally

# Production debugging
./scripts/deploy.sh status  # Check deployment status
./scripts/deploy.sh logs    # View application logs
```

## 📚 Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Documentation](https://docs.docker.com/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [pytest Documentation](https://docs.pytest.org/)

## 🤝 Contributing

1. Follow the development workflow
2. Ensure all tests pass
3. Add tests for new features
4. Update documentation as needed
5. Follow code style guidelines (enforced by pre-commit hooks)

---

For questions or issues, please open a GitHub issue or contact the development team.
