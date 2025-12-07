# NEL Demo Installer for Windows
# This script checks Python version, creates a virtual environment, and installs dependencies

Write-Host "NEL Demo Installation Script for Windows" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green

# Check if Python is installed
try {
    $pythonCmd = Get-Command python -ErrorAction Stop
    $pythonVersion = python --version 2>&1
    Write-Host "Found: $pythonVersion" -ForegroundColor Cyan
} catch {
    Write-Host "Error: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Python 3.10 or 3.11 from https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host "Note: Python 3.10 or 3.11 is recommended for best compatibility with spaCy." -ForegroundColor Yellow
    Write-Host "Python 3.12+ may have compatibility issues with spacy-transformers." -ForegroundColor Yellow
    exit 1
}

# Check Python version (must be >= 3.10, recommend <= 3.11)
$versionOutput = python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"
$versionParts = $versionOutput.Split('.')
$major = [int]$versionParts[0]
$minor = [int]$versionParts[1]

if ($major -lt 3 -or ($major -eq 3 -and $minor -lt 10)) {
    Write-Host "Error: Python 3.10 or higher is required. Found Python $versionOutput" -ForegroundColor Red
    Write-Host "Please install Python 3.10 or 3.11 from https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

if ($major -eq 3 -and $minor -gt 11) {
    Write-Host "Warning: Python $versionOutput detected. Python 3.12+ may have compatibility issues with spacy-transformers." -ForegroundColor Yellow
    Write-Host "Python 3.10 or 3.11 is recommended for best compatibility." -ForegroundColor Yellow
    Write-Host ""
    $continue = Read-Host "Do you want to continue anyway? (y/N)"
    if ($continue -ne "y" -and $continue -ne "Y") {
        Write-Host "Installation cancelled. Please install Python 3.10 or 3.11." -ForegroundColor Yellow
        exit 1
    }
}

Write-Host "Python version check passed: $versionOutput" -ForegroundColor Green

# Create virtual environment
Write-Host "`nCreating virtual environment..." -ForegroundColor Cyan
if (Test-Path "venv") {
    Write-Host "Virtual environment already exists. Removing..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force venv
}

python -m venv venv
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Failed to create virtual environment" -ForegroundColor Red
    exit 1
}

Write-Host "Virtual environment created successfully" -ForegroundColor Green

# Activate virtual environment
Write-Host "`nActivating virtual environment..." -ForegroundColor Cyan
& .\venv\Scripts\Activate.ps1

# Upgrade pip
Write-Host "`nUpgrading pip..." -ForegroundColor Cyan
python -m pip install --upgrade pip

# Ask user which spaCy version to install
Write-Host "`nWhich spaCy version would you like to install?" -ForegroundColor Cyan
Write-Host "1. spaCy (standard - faster, smaller)" -ForegroundColor White
Write-Host "2. spacy-transformers (transformer models - more accurate, larger)" -ForegroundColor White
$choice = Read-Host "Enter your choice (1 or 2)"

switch ($choice) {
    "1" {
        Write-Host "`nInstalling spaCy (standard)..." -ForegroundColor Cyan
        python -m pip install -r requirements.txt
    }
    "2" {
        Write-Host "`nInstalling spacy-transformers..." -ForegroundColor Cyan
        python -m pip install -r requirements.txt
        python -m pip install spacy-transformers
    }
    default {
        Write-Host "Invalid choice. Installing standard spaCy..." -ForegroundColor Yellow
        python -m pip install -r requirements.txt
    }
}

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Failed to install dependencies" -ForegroundColor Red
    exit 1
}

Write-Host "`n=========================================" -ForegroundColor Green
Write-Host "Installation completed successfully!" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green
Write-Host "`nTo use the application:" -ForegroundColor Cyan
Write-Host "1. Activate the virtual environment: .\venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "2. Place your trained model in: models/{model_name}/model-best/" -ForegroundColor White
Write-Host "3. Run the GUI: python src/gui.py" -ForegroundColor White
Write-Host "`nNote: You'll need to download or train a spaCy model first." -ForegroundColor Yellow
Write-Host "Example: python -m spacy download en_core_web_sm" -ForegroundColor Yellow
