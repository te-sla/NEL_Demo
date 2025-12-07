#!/bin/bash

# NEL Demo Installer for Linux/Mac
# This script checks Python version, creates a virtual environment, and installs dependencies

echo "NEL Demo Installation Script for Linux/Mac"
echo "=========================================="

# Function to detect OS
detect_os() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    elif [ -f /etc/os-release ]; then
        . /etc/os-release
        echo "${ID}"
    else
        echo "unknown"
    fi
}

# Function to show Python installation instructions
show_python_install_instructions() {
    local os_type=$(detect_os)
    
    echo ""
    echo "Python 3.10 or 3.11 is required for this application."
    echo "Python 3.12+ may have compatibility issues with spacy-transformers."
    echo ""
    
    case "$os_type" in
        "macos")
            echo "To install Python 3.11 on macOS:"
            echo ""
            # Check if Homebrew is installed
            if command -v brew &> /dev/null; then
                echo "Using Homebrew (recommended):"
                echo "  brew install python@3.11"
                echo ""
                read -p "Would you like to install Python 3.11 using Homebrew now? (y/N): " -n 1 -r
                echo
                if [[ $REPLY =~ ^[Yy]$ ]]; then
                    echo "Installing Python 3.11 with Homebrew..."
                    brew install python@3.11
                    if [ $? -eq 0 ]; then
                        echo "Python 3.11 installed successfully!"
                        echo "Please run this script again."
                        exit 0
                    else
                        echo "Homebrew installation failed. Please try manual installation."
                    fi
                fi
            else
                echo "Homebrew is not installed. Install Homebrew first:"
                echo "  /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
                echo ""
                echo "Then run: brew install python@3.11"
            fi
            echo ""
            echo "Or download from: https://www.python.org/downloads/macos/"
            ;;
        "ubuntu"|"debian")
            echo "To install Python 3.11 on Ubuntu/Debian:"
            echo "  sudo apt update"
            echo "  sudo apt install python3.11 python3.11-venv"
            echo ""
            read -p "Would you like to install Python 3.11 now? (y/N): " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                echo "Installing Python 3.11..."
                sudo apt update && sudo apt install -y python3.11 python3.11-venv
                if [ $? -eq 0 ]; then
                    echo "Python 3.11 installed successfully!"
                    echo "Please run this script again using: python3.11 or update your python3 symlink."
                    exit 0
                fi
            fi
            ;;
        "fedora"|"rhel"|"centos")
            echo "To install Python 3.11 on Fedora/RHEL/CentOS:"
            echo "  sudo dnf install python3.11"
            echo ""
            read -p "Would you like to install Python 3.11 now? (y/N): " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                echo "Installing Python 3.11..."
                sudo dnf install -y python3.11
                if [ $? -eq 0 ]; then
                    echo "Python 3.11 installed successfully!"
                    echo "Please run this script again using: python3.11"
                    exit 0
                fi
            fi
            ;;
        "arch"|"manjaro")
            echo "To install Python 3.11 on Arch Linux:"
            echo "  sudo pacman -S python"
            echo ""
            read -p "Would you like to install Python now? (y/N): " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                echo "Installing Python..."
                sudo pacman -S --noconfirm python
                if [ $? -eq 0 ]; then
                    echo "Python installed successfully!"
                    echo "Please run this script again."
                    exit 0
                fi
            fi
            ;;
        *)
            echo "For your system, please visit: https://www.python.org/downloads/"
            ;;
    esac
}

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    show_python_install_instructions
    exit 1
fi

# Check Python version (must be >= 3.10, recommend <= 3.11)
PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo "Found: Python $PYTHON_VERSION"

MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$MAJOR" -lt 3 ] || [ "$MAJOR" -eq 3 -a "$MINOR" -lt 10 ]; then
    echo "Error: Python 3.10 or higher is required. Found Python $PYTHON_VERSION"
    show_python_install_instructions
    exit 1
fi

if [ "$MAJOR" -eq 3 -a "$MINOR" -gt 11 ]; then
    echo "Warning: Python $PYTHON_VERSION detected. Python 3.12+ may have compatibility issues with spacy-transformers."
    echo "Python 3.10 or 3.11 is recommended for best compatibility."
    echo ""
    read -p "Do you want to continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Installation cancelled."
        echo ""
        show_python_install_instructions
        exit 1
    fi
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
