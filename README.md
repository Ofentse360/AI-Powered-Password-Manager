# 🔐 AI-Powered Password Manager

A secure, intelligent password management system with ML-powered security analysis and breach detection.

## ✨ Features

### Core Security

- AES-256 encryption for password storage
- bcrypt hashing for master passwords
- Zero-knowledge architecture
- Secure password generation

### AI-Powered Features

- ML-based password strength prediction
- Anomaly detection for suspicious activity
- Breach pattern analysis
- Smart password expiry recommendations

### User Features

- Intuitive web interface
- Breach checking via Have I Been Pwned API
- Password health dashboard
- Optional CLI tool

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Node.js 18+
- Git

### Backend Setup

```bash
# Clone repository
git clone [https://github.com/yourusername/password-manager.git](https://github.com/yourusername/password-manager.git)
cd password-manager

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
cd backend
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env with your configuration

# Initialize database
python scripts/setup_db.py

# Run server (Once app/main.py is complete)
uvicorn app.main:app --reload
```
