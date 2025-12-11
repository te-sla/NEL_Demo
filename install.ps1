# NEL Demo Installer for Windows
# This script checks Python version, creates a virtual environment, and installs dependencies

Write-Host "NEL Demo Installation Script for Windows" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green

# Function to install Python using winget
function Install-PythonWithWinget {
    param(
        [string]$version = "3.11"
    )
    
    Write-Host "`nAttempting to install Python $version using winget..." -ForegroundColor Cyan
    
    # Check if winget is available
    if (Get-Command winget -ErrorAction SilentlyContinue) {
        Write-Host "winget is available. Installing Python $version..." -ForegroundColor Green
        
        try {
            # Install Python 3.11 using winget
            winget install Python.Python.3.11 --silent --accept-package-agreements --accept-source-agreements
            
            if ($LASTEXITCODE -eq 0) {
                Write-Host "Python $version installed successfully!" -ForegroundColor Green
                Write-Host "Please close and reopen this terminal, then run the installer again." -ForegroundColor Yellow
                exit 0
            } else {
                Write-Host "winget installation failed. Please install manually." -ForegroundColor Red
                return $false
            }
        } catch {
            Write-Host "Error during winget installation: $_" -ForegroundColor Red
            return $false
        }
    } else {
        Write-Host "winget is not available on this system." -ForegroundColor Yellow
        return $false
    }
}

# Check if Python is installed
try {
    $pythonCmd = Get-Command python -ErrorAction Stop
    $pythonVersion = python --version 2>&1
    Write-Host "Found: $pythonVersion" -ForegroundColor Cyan
} catch {
    Write-Host "Error: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host ""
    Write-Host "Python 3.10 or 3.11 is required for this application." -ForegroundColor Yellow
    Write-Host "Python 3.12+ may have compatibility issues with spacy-transformers." -ForegroundColor Yellow
    Write-Host ""
    
    # Offer automatic installation
    $autoInstall = Read-Host "Would you like to automatically install Python 3.11? (y/N)"
    
    if ($autoInstall -eq "y" -or $autoInstall -eq "Y") {
        $installed = Install-PythonWithWinget -version "3.11"
        if (-not $installed) {
            Write-Host "`nAutomatic installation failed." -ForegroundColor Red
        }
    }
    
    # Show manual installation instructions
    Write-Host "`nTo install Python manually:" -ForegroundColor Yellow
    Write-Host "1. Visit: https://www.python.org/downloads/windows/" -ForegroundColor Cyan
    Write-Host "2. Download Python 3.11 (recommended)" -ForegroundColor Cyan
    Write-Host "3. Run the installer and make sure to check 'Add Python to PATH'" -ForegroundColor Cyan
    Write-Host "4. After installation, close this terminal and run this script again" -ForegroundColor Cyan
    
    exit 1
}

# Check Python version (must be >= 3.10, recommend <= 3.11)
try {
    $versionOutput = python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')" 2>&1
    
    # Check if $versionOutput is null, empty, or contains error messages
    if ([string]::IsNullOrWhiteSpace($versionOutput) -or $versionOutput -match "^\s*(error|exception|traceback|'python' is not recognized)") {
        throw "Python version command failed"
    }
    
    $versionParts = $versionOutput.Split('.')
    
    # Validate that we have at least 2 parts (major.minor)
    if ($versionParts.Length -lt 2) {
        throw "Invalid Python version format: $versionOutput"
    }
    
    $major = [int]$versionParts[0]
    $minor = [int]$versionParts[1]
} catch {
    Write-Host "Error: Unable to determine Python version" -ForegroundColor Red
    Write-Host "Python may not be properly installed or configured." -ForegroundColor Red
    Write-Host ""
    Write-Host "Python 3.10 or 3.11 is required for this application." -ForegroundColor Yellow
    Write-Host "Python 3.12+ may have compatibility issues with spacy-transformers." -ForegroundColor Yellow
    Write-Host ""
    
    # Offer automatic installation
    $autoInstall = Read-Host "Would you like to automatically install Python 3.11? (y/N)"
    
    if ($autoInstall -eq "y" -or $autoInstall -eq "Y") {
        $installed = Install-PythonWithWinget -version "3.11"
        if (-not $installed) {
            Write-Host "`nAutomatic installation failed." -ForegroundColor Red
        }
    }
    
    # Show manual installation instructions
    Write-Host "`nTo install Python manually:" -ForegroundColor Yellow
    Write-Host "1. Visit: https://www.python.org/downloads/windows/" -ForegroundColor Cyan
    Write-Host "2. Download Python 3.11 (recommended)" -ForegroundColor Cyan
    Write-Host "3. Run the installer and make sure to check 'Add Python to PATH'" -ForegroundColor Cyan
    Write-Host "4. After installation, close this terminal and run this script again" -ForegroundColor Cyan
    
    exit 1
}

if ($major -lt 3 -or ($major -eq 3 -and $minor -lt 10)) {
    Write-Host "Error: Python 3.10 or higher is required. Found Python $versionOutput" -ForegroundColor Red
    Write-Host ""
    
    # Offer to install newer version
    $upgrade = Read-Host "Would you like to install Python 3.11? (y/N)"
    
    if ($upgrade -eq "y" -or $upgrade -eq "Y") {
        $installed = Install-PythonWithWinget -version "3.11"
        if (-not $installed) {
            Write-Host "`nAutomatic installation failed." -ForegroundColor Red
        }
    }
    
    Write-Host "`nTo upgrade Python manually:" -ForegroundColor Yellow
    Write-Host "Visit: https://www.python.org/downloads/windows/" -ForegroundColor Cyan
    Write-Host "Download and install Python 3.11 (recommended)" -ForegroundColor Cyan
    
    exit 1
}

if ($major -eq 3 -and $minor -gt 11) {
    Write-Host "Warning: Python $versionOutput detected. Python 3.12+ may have compatibility issues with spacy-transformers." -ForegroundColor Yellow
    Write-Host "Python 3.10 or 3.11 is recommended for best compatibility." -ForegroundColor Yellow
    Write-Host ""
    $continue = Read-Host "Do you want to continue anyway? (y/N)"
    if ($continue -ne "y" -and $continue -ne "Y") {
        Write-Host "Installation cancelled." -ForegroundColor Yellow
        Write-Host ""
        Write-Host "To install Python 3.11:" -ForegroundColor Yellow
        Write-Host "Visit: https://www.python.org/downloads/windows/" -ForegroundColor Cyan
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
