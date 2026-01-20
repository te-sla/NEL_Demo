# PowerShell script to build NEL Demo as a standalone Windows executable
# Requires Python 3.10+ with PyInstaller

param(
    [switch]$Clean = $false,
    [switch]$UseUPX = $false
)

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  NEL Demo - Windows Executable Build Script  " -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Set error action preference
$ErrorActionPreference = "Stop"

# Get the script directory and project root
$SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path
$PROJECT_ROOT = Split-Path -Parent $SCRIPT_DIR

Write-Host "Project root: $PROJECT_ROOT" -ForegroundColor Yellow
Write-Host ""

# Change to project root
Set-Location $PROJECT_ROOT

# Check if virtual environment exists
$VENV_PATH = Join-Path $PROJECT_ROOT "venv"
$VENV_ACTIVATE = Join-Path $VENV_PATH "Scripts\Activate.ps1"

if (Test-Path $VENV_ACTIVATE) {
    Write-Host "Activating virtual environment..." -ForegroundColor Green
    & $VENV_ACTIVATE
} else {
    Write-Host "Warning: Virtual environment not found at $VENV_PATH" -ForegroundColor Yellow
    Write-Host "Using system Python. Consider creating a virtual environment first." -ForegroundColor Yellow
    Write-Host ""
}

# Detect Python command
Write-Host "Detecting Python command..." -ForegroundColor Green
$pythonCandidates = @("py", "python", "python3")
$PYTHON_CMD = $null

foreach ($cmd in $pythonCandidates) {
    try {
        $null = & $cmd --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            $PYTHON_CMD = $cmd
            break
        }
    } catch {
        # Ignore and try next candidate
        continue
    }
}

if (-not $PYTHON_CMD) {
    Write-Host "Error: No suitable Python interpreter found." -ForegroundColor Red
    Write-Host "Please install Python 3.10+ and ensure it is on your PATH." -ForegroundColor Red
    exit 1
}

# Check Python version
Write-Host "Checking Python version using: $PYTHON_CMD" -ForegroundColor Green
$PYTHON_VERSION = & $PYTHON_CMD --version 2>&1
Write-Host "Found: $PYTHON_VERSION" -ForegroundColor Cyan

# Install/upgrade PyInstaller
Write-Host ""
Write-Host "Installing/upgrading PyInstaller..." -ForegroundColor Green
& $PYTHON_CMD -m pip install --upgrade pyinstaller
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Failed to install PyInstaller" -ForegroundColor Red
    exit 1
}

# Clean previous builds if requested
if ($Clean) {
    Write-Host ""
    Write-Host "Cleaning previous builds..." -ForegroundColor Green
    $BUILD_DIR = Join-Path $PROJECT_ROOT "build"
    $DIST_DIR = Join-Path $PROJECT_ROOT "dist"
    if (Test-Path $BUILD_DIR) {
        Remove-Item -Recurse -Force $BUILD_DIR
        Write-Host "Removed: $BUILD_DIR" -ForegroundColor Yellow
    }
    if (Test-Path $DIST_DIR) {
        Remove-Item -Recurse -Force $DIST_DIR
        Write-Host "Removed: $DIST_DIR" -ForegroundColor Yellow
    }
}

# Update build date in version.py
Write-Host ""
Write-Host "Updating build date..." -ForegroundColor Green
$BUILD_DATE = Get-Date -Format "yyyy-MM-dd"
$VERSION_FILE = Join-Path $PROJECT_ROOT "src\version.py"
$VERSION_CONTENT = Get-Content $VERSION_FILE -Raw
$VERSION_CONTENT = $VERSION_CONTENT -replace '__build_date__ = ".*"', "__build_date__ = `"$BUILD_DATE`""
$VERSION_CONTENT = $VERSION_CONTENT -replace '__build_type__ = ".*"', '__build_type__ = "standalone"'
Set-Content -Path $VERSION_FILE -Value $VERSION_CONTENT
Write-Host "Build date set to: $BUILD_DATE" -ForegroundColor Cyan

# Build PyInstaller command
Write-Host ""
Write-Host "Building executable with PyInstaller..." -ForegroundColor Green
Write-Host ""

$PYINSTALLER_ARGS = @(
    "--onedir",
    "--windowed",
    "--name", "NEL_Demo",
    "--add-data", "models;models",
    "--add-data", "inputs;inputs",
    "--add-data", "data;data",
    "--hidden-import", "spacy",
    "--hidden-import", "cyrtranslit",
    "--hidden-import", "tkinter",
    "--collect-all", "spacy",
    "--collect-all", "cyrtranslit",
    "--exclude-module", "matplotlib",
    "--exclude-module", "IPython",
    "--exclude-module", "notebook",
    "--exclude-module", "jupyter",
    "--exclude-module", "pandas",
    "--exclude-module", "PIL",
    "--exclude-module", "pytest",
    "--strip"
)

# Add UPX compression if requested and available
if ($UseUPX) {
    Write-Host "UPX compression enabled" -ForegroundColor Cyan
    $PYINSTALLER_ARGS += "--upx-dir", "upx"
}

# Add icon if available
$ICON_FILE = Join-Path $PROJECT_ROOT "icon.ico"
if (Test-Path $ICON_FILE) {
    Write-Host "Using icon: $ICON_FILE" -ForegroundColor Cyan
    $PYINSTALLER_ARGS += "--icon", $ICON_FILE
}

# Run PyInstaller
$PYINSTALLER_ARGS += Join-Path $PROJECT_ROOT "src\gui.py"
& $PYTHON_CMD -m PyInstaller @PYINSTALLER_ARGS

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "Error: PyInstaller build failed" -ForegroundColor Red
    exit 1
}

# Create launcher script
Write-Host ""
Write-Host "Creating launcher script..." -ForegroundColor Green
$LAUNCHER_CONTENT = @"
@echo off
REM Launcher for NEL Demo
cd /d "%~dp0"
start "" "NEL_Demo\NEL_Demo.exe"
"@
$LAUNCHER_FILE = Join-Path $PROJECT_ROOT "dist\Launch_NEL_Demo.bat"
Set-Content -Path $LAUNCHER_FILE -Value $LAUNCHER_CONTENT
Write-Host "Created: $LAUNCHER_FILE" -ForegroundColor Cyan

# Success message
Write-Host ""
Write-Host "================================================" -ForegroundColor Green
Write-Host "  Build completed successfully!                " -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Executable location:" -ForegroundColor Yellow
Write-Host "  $PROJECT_ROOT\dist\NEL_Demo\" -ForegroundColor Cyan
Write-Host ""
Write-Host "To run the application:" -ForegroundColor Yellow
Write-Host "  1. Navigate to: dist\" -ForegroundColor Cyan
Write-Host "  2. Double-click: Launch_NEL_Demo.bat" -ForegroundColor Cyan
Write-Host "     OR" -ForegroundColor Cyan
Write-Host "  3. Navigate to: dist\NEL_Demo\" -ForegroundColor Cyan
Write-Host "  4. Double-click: NEL_Demo.exe" -ForegroundColor Cyan
Write-Host ""
Write-Host "To create an installer, run:" -ForegroundColor Yellow
Write-Host "  .\build_scripts\create_installer_windows.ps1" -ForegroundColor Cyan
Write-Host ""
