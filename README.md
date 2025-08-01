# Smart Report Assistant 🤖📊

An AI-powered business intelligence tool that automatically generates comprehensive reports with visualizations and intelligent insights from CSV data. Built with Flask, featuring both statistical analysis and GPT-enhanced AI capabilities.

## ✨ Features

### 🎯 **Core Functionality**
- **CSV Data Upload**: Simple web interface for uploading business data
- **Automated Visualizations**: 
  - Bar charts for risk category analysis
  - Line charts for temporal trend analysis
- **Intelligent Analysis**: Dual-mode analysis system
- **Professional Reports**: Executive-ready HTML reports
- **Real-time Processing**: Instant analysis and report generation

### 🧠 **AI-Powered Analysis**
- **GPT Integration**: Advanced AI analysis using OpenAI's GPT models
- **Statistical Fallback**: Comprehensive statistical analysis when GPT is unavailable
- **Smart Recommendations**: Context-aware business insights
- **Risk Assessment**: Automated risk pattern detection
- **Trend Analysis**: Temporal data analysis with actionable insights

### 🔧 **Technical Features**
- **Robust Error Handling**: Graceful fallback mechanisms
- **Secure Configuration**: Environment-based API key management
- **Responsive Design**: Clean, professional web interface (German UI)
- **Modular Architecture**: Easy to extend and customize
- **Production Ready**: Comprehensive logging and error handling
- **CI/CD Pipeline**: Automated testing, building, and deployment
- **Docker Support**: Containerized deployment with orchestration
- **Code Quality**: Automated linting, formatting, and security scanning

## 🚀 Quick Start

### **Option 1: Development Setup**
```bash
# Clone the repository
git clone https://github.com/YuryBesiakov/Smart-Report-Assistant.git
cd Smart-Report-Assistant

# Automated setup (recommended)
make setup              # Full environment setup
# OR manually:
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Configure environment
cp .env.example .env
# Edit .env with your OpenAI API key (optional)

# Run the application
make dev                # Using make
# OR
python app/main.py      # Direct run
```

### **Option 2: Docker Deployment**
```bash
# Quick start with Docker
docker-compose up --build

# Or using deployment scripts
./scripts/deploy.sh     # Linux/Mac
scripts\deploy.bat      # Windows
```

### **Option 3: CI/CD Development**
```bash
# Run all quality checks locally
make ci                 # Tests, linting, security checks
make test              # Run tests only
make lint              # Code quality checks
```
### **Access the Web Interface**
Open your browser and navigate to: `http://localhost:5000`

**Note**: The web interface is currently in German. The application displays messages like "Bitte laden Sie eine gültige CSV‑Datei hoch" (Please upload a valid CSV file).

## 🏗️ **CI/CD & DevOps Features**

**Note**: CI/CD badge status depends on your GitHub repository configuration.

### **Automated Pipeline**
- ✅ **Multi-Python Testing** (3.9, 3.10, 3.11)
- ✅ **Code Quality Checks** (flake8, black, mypy)
- ✅ **Security Scanning** (bandit, safety)
- ✅ **Docker Building** (multi-architecture)
- ✅ **Automated Deployment** (staging → production)

### **Development Commands**
```bash
make setup              # Full development setup
make test              # Run test suite
make test-cov          # Run tests with coverage
make lint              # Code quality checks
make format            # Auto-format code
make ci                # Run all CI checks locally
make docker-build      # Build Docker image
make docker-run        # Run in container
```

### **Deployment**
```bash
# Local deployment
docker-compose up --build

# Production deployment
./scripts/deploy.sh deploy
./scripts/deploy.sh status
./scripts/deploy.sh logs
```

📖 **Full CI/CD Documentation**: See [`CICD_GUIDE.md`](CICD_GUIDE.md)

## 📁 Project Structure

```
Smart-Report-Assistant/
├── app/
│   ├── main.py              # Flask application entry point
│   ├── report_generator.py  # Core analysis and GPT integration
│   ├── templates/           # HTML templates
│   ├── static/plots/        # Generated charts storage
│   └── uploads/             # Uploaded files storage
├── tests/                   # Test suite
│   ├── test_main.py         # Flask app tests
│   └── test_report_generator.py  # Core logic tests
├── .github/workflows/       # CI/CD pipeline configuration
├── scripts/                 # Deployment and setup scripts
├── data/                    # Example datasets
├── Dockerfile               # Container configuration
├── docker-compose.yml       # Multi-service orchestration
├── requirements.txt         # Production dependencies
├── requirements-dev.txt     # Development dependencies
├── pyproject.toml          # Project configuration
├── Makefile                # Development commands
└── CICD_GUIDE.md           # Complete DevOps documentation
```

## 🔑 OpenAI GPT Integration

### **Setup Instructions**

1. **Get an OpenAI API Key**:
   - Visit [OpenAI API Keys](https://platform.openai.com/api-keys)
   - Create an account or sign in
   - Generate a new API key

2. **Configure the Application**:
   ```bash
   # Copy the example file
   cp .env.example .env
   
   # Edit .env and replace with your actual API key
   OPENAI_API_KEY=sk-your-actual-api-key-here
   OPENAI_MODEL=gpt-3.5-turbo  # or gpt-4 for enhanced analysis
   ```

3. **Test the Integration**:
   ```bash
   python test_gpt.py
   ```

### **Analysis Modes**

| Mode | Description | Use Case |
|------|-------------|----------|
| **GPT-Enhanced** | AI-powered analysis with advanced insights | When OpenAI API key is configured and quota available |
| **Statistical** | Comprehensive statistical analysis | Fallback mode or when GPT is not needed |

### **Cost Considerations**
- **GPT-3.5-turbo**: ~$0.001-0.002 per report
- **GPT-4**: ~$0.03-0.06 per report
- **Statistical Mode**: Free (no API calls)

## 📊 Expected Data Format

Your CSV file should include these columns:

| Column | Description | Required |
|--------|-------------|----------|
| `Date` | Date in YYYY-MM-DD format | ✅ Yes |
| `RiskCategory` | Risk category (e.g., "Operational", "Credit") | ✅ Yes |
| `Risikoscore` | Numerical risk score | ✅ Yes |
| `Verluste` | Financial losses | ⚪ Optional |
| `Kundenzahlen` | Customer numbers | ⚪ Optional |

### **Example Data Structure**
```csv
Date,Kundenzahlen,Risikoscore,Verluste,RiskCategory
2024-01-01,1258,34.04,796.96,Operational
2024-01-01,1025,24.46,691.23,Credit
2024-01-01,1373,15.30,560.77,Market
```

## 🔧 Dependencies

### **Core Requirements**
```
Flask>=2.3.0          # Web framework
pandas>=2.0.0         # Data processing
matplotlib>=3.7.0     # Visualization
Werkzeug>=2.3.0       # WSGI utilities
```

### **AI Integration**
```
openai>=1.0.0         # GPT integration
python-dotenv>=1.0.0  # Environment management
```

## 🧪 Testing

### **Test GPT Integration**
```bash
python test_gpt.py
```

### **Test with Example Data**
1. Start the application: `python app/main.py`
2. Open: `http://localhost:5000`
3. Upload: `data/beispiel.csv`
4. Review the generated report

## 🛡️ Security Features

- **API Key Protection**: Environment-based configuration
- **Input Validation**: Secure file upload handling
- **Error Handling**: No sensitive data in error messages
- **Path Security**: Secure filename handling with Werkzeug
- **Gitignore**: API keys and uploads excluded from version control

## 🚀 Deployment

### **Development**
```bash
# Local development server
python app/main.py
# OR with auto-reload
make dev
```

### **Docker Deployment**
```bash
# Development with Docker
docker-compose up --build

# Production deployment
docker-compose --profile production up --build

# Using deployment scripts
./scripts/deploy.sh          # Linux/Mac
scripts\deploy.bat           # Windows
```

### **Production Deployment**
The project includes automated CI/CD with GitHub Actions:

1. **Push to GitHub** → Triggers automated testing
2. **Tests Pass** → Builds Docker image
3. **Main Branch** → Deploys to staging automatically
4. **Manual Approval** → Promotes to production

**Production Features:**
- Multi-architecture Docker images (AMD64/ARM64)
- Nginx reverse proxy with SSL
- Health checks and monitoring
- Automatic rollback capabilities
- Zero-downtime deployments

### **Cloud Deployment Ready**
- AWS ECS/EKS
- Google Cloud Run/GKE
- Azure Container Instances/AKS
- DigitalOcean App Platform
- Heroku (using container deployment)

## 🔄 Development Workflow

### **Adding New Features**
1. **Analysis Functions**: Add to `report_generator.py`
2. **Web Routes**: Extend `main.py`
3. **Templates**: Modify HTML templates in `templates/`
4. **Testing**: Update `test_gpt.py`

### **Extending Visualizations**
```python
# Add new chart types in report_generator.py
def generate_custom_chart(df: pd.DataFrame) -> str:
    # Your visualization logic here
    pass
```

## 📈 Roadmap

- [ ] **PDF Export**: Convert reports to PDF format
- [ ] **Multiple File Types**: Support Excel, JSON inputs
- [ ] **Advanced Visualizations**: Interactive charts with Plotly
- [ ] **User Authentication**: Multi-user support
- [ ] **Database Integration**: Persistent data storage
- [ ] **API Endpoints**: RESTful API for programmatic access
- [ ] **Real-time Updates**: WebSocket-based live updates
- [ ] **Internationalization**: Multi-language support (currently German UI)
- [ ] **Enhanced Data Processing**: Support for larger datasets
- [ ] **Custom Report Templates**: User-defined report layouts

## 🤝 Contributing

1. **Fork the Repository**
2. **Create a Feature Branch**: `git checkout -b feature/amazing-feature`
3. **Commit Changes**: `git commit -m 'Add amazing feature'`
4. **Push to Branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

### **Common Issues**

**GPT API Issues**:
- Check your API key in `.env`
- Verify OpenAI account billing
- Review usage quotas

**Installation Problems**:
- Ensure Python 3.8+ is installed
- Use virtual environments
- Check dependency versions

**Data Upload Issues**:
- Verify CSV format matches expected structure
- Check file permissions
- Ensure file size is reasonable  
- Note: Error messages are displayed in German

**Language Note**:
- The web interface uses German language
- Error messages and labels are in German
- Code comments are primarily in German

### **Getting Help**
- 💬 **Issues**: [GitHub Issues](https://github.com/YuryBesiakov/Smart-Report-Assistant/issues)
- 📖 **Documentation**: See `GPT_SETUP.md` for detailed GPT configuration
- 🌐 **Language**: Interface is currently in German - see roadmap for internationalization plans

## 🙏 Acknowledgments

- **OpenAI** for GPT API access
- **Flask Community** for the excellent web framework
- **Pandas Team** for powerful data processing tools
- **Matplotlib** for visualization capabilities

---

**Made with ❤️ for intelligent business reporting**

*Transform your data into actionable insights with AI-powered analysis*
