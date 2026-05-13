#!/bin/bash
# Quick setup script for local development and AWS deployment testing
# Run this script from the project root directory

set -e

echo "=== Flask Application Setup Script ==="
echo ""

# Check Python version
echo "✓ Checking Python version..."
PYTHON_VERSION=$(python --version 2>&1 | awk '{print $2}')
echo "  Python $PYTHON_VERSION"

# Create virtual environment
echo "✓ Creating virtual environment..."
if [ ! -d "venv" ]; then
    python -m venv venv
    echo "  Virtual environment created at ./venv"
else
    echo "  Virtual environment already exists"
fi

# Activate virtual environment
echo "✓ Activating virtual environment..."
source venv/bin/activate || . venv/Scripts/activate
echo "  Virtual environment activated"

# Upgrade pip
echo "✓ Upgrading pip..."
pip install --upgrade pip setuptools wheel > /dev/null 2>&1
echo "  pip upgraded"

# Install dependencies
echo "✓ Installing dependencies from requirements.txt..."
pip install -r requirements.txt
echo "  Dependencies installed"

# Copy environment file
echo "✓ Setting up environment configuration..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "  .env file created from .env.example"
    echo "  ⚠️  Edit .env with your actual settings before deployment"
else
    echo "  .env file already exists"
fi

# Run tests
echo ""
echo "✓ Running tests..."
python -m pytest tests/ -v --tb=short

# Summary
echo ""
echo "==================================="
echo "✅ Setup Complete!"
echo "==================================="
echo ""
echo "Next steps:"
echo "1. Edit .env with your settings"
echo "2. Run the application: python app.py"
echo "3. Open http://localhost:5000 in your browser"
echo ""
echo "For AWS deployment:"
echo "1. Push code to AWS CodeCommit"
echo "2. Set up CodeBuild project"
echo "3. Create CodePipeline"
echo ""
echo "See AWS_SETUP_GUIDE.md for detailed instructions"
echo ""
