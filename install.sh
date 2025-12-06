#!/bin/bash

# NEL Demo Installer for Linux/Mac
# This script checks Python version, creates a virtual environment, and installs dependencies

echo "NEL Demo Installation Script for Linux/Mac"
echo "=========================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3.10 or higher"
    exit 1
fi

# Check Python version (must be >= 3.10)
PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo "Found: Python $PYTHON_VERSION"

MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$MAJOR" -lt 3 ] || [ "$MAJOR" -eq 3 -a "$MINOR" -lt 10 ]; then
    echo "Error: Python 3.10 or higher is required. Found Python $PYTHON_VERSION"
    exit 1
fi

echo "Python version check passed: $PYTHON_VERSION"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
if [ -d "venv" ]; then
    echo "Virtual environment already exists. Removing..."
    rm -rf venv
fi

python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "Error: Failed to create virtual environment"
    exit 1
fi

echo "Virtual environment created successfully"

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
python -m pip install --upgrade pip

# Ask user which spaCy version to install
echo ""
echo "Which spaCy version would you like to install?"
echo "1. spaCy (standard - faster, smaller)"
echo "2. spacy-transformers (transformer models - more accurate, larger)"
read -p "Enter your choice (1 or 2): " choice

case $choice in
    1)
        echo ""
        echo "Installing spaCy (standard)..."
        python -m pip install -r requirements.txt
        ;;
    2)
        echo ""
        echo "Installing spacy-transformers..."
        python -m pip install -r requirements.txt
        python -m pip install spacy-transformers
        ;;
    *)
        echo "Invalid choice. Installing standard spaCy..."
        python -m pip install -r requirements.txt
        ;;
esac

if [ $? -ne 0 ]; then
    echo "Error: Failed to install dependencies"
    exit 1
fi

echo ""
echo "========================================="
echo "Installation completed successfully!"
echo "========================================="
echo ""
echo "To use the application:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Place your trained model in: models/{model_name}/model-best/"
echo "3. Run the GUI: python src/gui.py"
echo ""
echo "Note: You'll need to download or train a spaCy model first."
echo "Example: python -m spacy download en_core_web_sm"
