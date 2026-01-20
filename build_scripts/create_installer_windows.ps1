# PowerShell script to create Windows installer using NSIS
# Requires: NSIS (Nullsoft Scriptable Install System)

param(
    [string]$Version = "1.0.0"
)

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  NEL Demo - Windows Installer Creator        " -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

$ErrorActionPreference = "Stop"

# Get directories
$SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path
$PROJECT_ROOT = Split-Path -Parent $SCRIPT_DIR
$DIST_DIR = Join-Path $PROJECT_ROOT "dist"
$BUILD_SCRIPTS_DIR = Join-Path $PROJECT_ROOT "build_scripts"

Write-Host "Project root: $PROJECT_ROOT" -ForegroundColor Yellow
Write-Host "Version: $Version" -ForegroundColor Yellow
Write-Host ""

# Check if dist folder exists
if (-not (Test-Path (Join-Path $DIST_DIR "NEL_Demo"))) {
    Write-Host "Error: Executable not found in dist/NEL_Demo/" -ForegroundColor Red
    Write-Host "Please run build_executable.ps1 first" -ForegroundColor Red
    exit 1
}

# Check if NSIS is installed
$NSIS_PATHS = @(
    "${env:ProgramFiles}\NSIS\makensis.exe",
    "${env:ProgramFiles(x86)}\NSIS\makensis.exe",
    "C:\Program Files\NSIS\makensis.exe",
    "C:\Program Files (x86)\NSIS\makensis.exe"
)

$NSIS_EXE = $null
foreach ($path in $NSIS_PATHS) {
    if (Test-Path $path) {
        $NSIS_EXE = $path
        break
    }
}

if (-not $NSIS_EXE) {
    Write-Host "NSIS not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install NSIS from:" -ForegroundColor Yellow
    Write-Host "  https://nsis.sourceforge.io/Download" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Or install using Chocolatey:" -ForegroundColor Yellow
    Write-Host "  choco install nsis" -ForegroundColor Cyan
    Write-Host ""
    exit 1
}

Write-Host "Found NSIS: $NSIS_EXE" -ForegroundColor Green
Write-Host ""

# Generate NSIS script from template
Write-Host "Generating NSIS script..." -ForegroundColor Green
$NSI_TEMPLATE = Join-Path $BUILD_SCRIPTS_DIR "installer_template.nsi"
$NSI_SCRIPT = Join-Path $PROJECT_ROOT "installer.nsi"

if (-not (Test-Path $NSI_TEMPLATE)) {
    Write-Host "Error: NSIS template not found: $NSI_TEMPLATE" -ForegroundColor Red
    exit 1
}

# Read template and replace variables
$NSI_CONTENT = Get-Content $NSI_TEMPLATE -Raw
$NSI_CONTENT = $NSI_CONTENT -replace '\$\{VERSION\}', $Version
$NSI_CONTENT = $NSI_CONTENT -replace '\$\{PROJECT_ROOT\}', $PROJECT_ROOT
$NSI_CONTENT = $NSI_CONTENT -replace '\$\{DIST_DIR\}', $DIST_DIR

Set-Content -Path $NSI_SCRIPT -Value $NSI_CONTENT
Write-Host "Created: $NSI_SCRIPT" -ForegroundColor Cyan

# Compile installer
Write-Host ""
Write-Host "Compiling installer with NSIS..." -ForegroundColor Green
Write-Host ""

& $NSIS_EXE $NSI_SCRIPT

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "Error: NSIS compilation failed" -ForegroundColor Red
    exit 1
}

# Find the created installer
$INSTALLER_FILE = Join-Path $DIST_DIR "NEL_Demo_Setup_v$Version.exe"

if (Test-Path $INSTALLER_FILE) {
    $FILE_SIZE = (Get-Item $INSTALLER_FILE).Length / 1MB
    Write-Host ""
    Write-Host "================================================" -ForegroundColor Green
    Write-Host "  Installer created successfully!              " -ForegroundColor Green
    Write-Host "================================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Installer location:" -ForegroundColor Yellow
    Write-Host "  $INSTALLER_FILE" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "File size: $([math]::Round($FILE_SIZE, 2)) MB" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "You can now distribute this installer to users." -ForegroundColor Green
    Write-Host ""
} else {
    Write-Host "Warning: Installer file not found at expected location" -ForegroundColor Yellow
    Write-Host "Check the dist/ directory for the installer" -ForegroundColor Yellow
}

# Cleanup
Remove-Item -Path $NSI_SCRIPT -Force -ErrorAction SilentlyContinue
