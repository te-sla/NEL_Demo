#!/bin/bash
# Bash script to build NEL Demo as a standalone executable for Linux/macOS
# Requires Python 3.10+ with PyInstaller

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Parse command line arguments
CLEAN=false
USE_UPX=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --clean)
            CLEAN=true
            shift
            ;;
        --use-upx)
            USE_UPX=true
            shift
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            exit 1
            ;;
    esac
done

echo -e "${CYAN}================================================${NC}"
echo -e "${CYAN}  NEL Demo - Executable Build Script          ${NC}"
echo -e "${CYAN}================================================${NC}"
echo ""

# Get the script directory and project root
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

echo -e "${YELLOW}Project root: $PROJECT_ROOT${NC}"
echo ""

# Change to project root
cd "$PROJECT_ROOT"

# Check if virtual environment exists
VENV_PATH="$PROJECT_ROOT/venv"
VENV_ACTIVATE="$VENV_PATH/bin/activate"

if [ -f "$VENV_ACTIVATE" ]; then
    echo -e "${GREEN}Activating virtual environment...${NC}"
    source "$VENV_ACTIVATE"
else
    echo -e "${YELLOW}Warning: Virtual environment not found at $VENV_PATH${NC}"
    echo -e "${YELLOW}Using system Python. Consider creating a virtual environment first.${NC}"
    echo ""
fi

# Check Python version
echo -e "${GREEN}Checking Python version...${NC}"
PYTHON_VERSION=$(python3 --version 2>&1 || python --version 2>&1)
echo -e "${CYAN}Found: $PYTHON_VERSION${NC}"

# Determine Python command
if command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
else
    PYTHON_CMD=python
fi

# Install/upgrade PyInstaller
echo ""
echo -e "${GREEN}Installing/upgrading PyInstaller...${NC}"
$PYTHON_CMD -m pip install --upgrade pyinstaller

# Clean previous builds if requested
if [ "$CLEAN" = true ]; then
    echo ""
    echo -e "${GREEN}Cleaning previous builds...${NC}"
    if [ -d "$PROJECT_ROOT/build" ]; then
        rm -rf "$PROJECT_ROOT/build"
        echo -e "${YELLOW}Removed: $PROJECT_ROOT/build${NC}"
    fi
    if [ -d "$PROJECT_ROOT/dist" ]; then
        rm -rf "$PROJECT_ROOT/dist"
        echo -e "${YELLOW}Removed: $PROJECT_ROOT/dist${NC}"
    fi
fi

# Update build date in version.py
echo ""
echo -e "${GREEN}Updating build date...${NC}"
BUILD_DATE=$(date +%Y-%m-%d)
VERSION_FILE="$PROJECT_ROOT/src/version.py"

# Use sed for in-place replacement (cross-platform compatible)
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS requires -i '' for in-place editing
    sed -i '' "s/__build_date__ = \".*\"/__build_date__ = \"$BUILD_DATE\"/" "$VERSION_FILE"
    sed -i '' 's/__build_type__ = ".*"/__build_type__ = "standalone"/' "$VERSION_FILE"
else
    # Linux
    sed -i "s/__build_date__ = \".*\"/__build_date__ = \"$BUILD_DATE\"/" "$VERSION_FILE"
    sed -i 's/__build_type__ = ".*"/__build_type__ = "standalone"/' "$VERSION_FILE"
fi
echo -e "${CYAN}Build date set to: $BUILD_DATE${NC}"

# Build PyInstaller command
echo ""
echo -e "${GREEN}Building executable with PyInstaller...${NC}"
echo ""

PYINSTALLER_ARGS=(
    --onedir
    --windowed
    --name NEL_Demo
    --add-data "models:models"
    --add-data "inputs:inputs"
    --add-data "data:data"
    --hidden-import spacy
    --hidden-import cyrtranslit
    --hidden-import tkinter
    --collect-all spacy
    --collect-all cyrtranslit
    --exclude-module matplotlib
    --exclude-module IPython
    --exclude-module notebook
    --exclude-module jupyter
    --exclude-module pandas
    --exclude-module PIL
    --exclude-module pytest
    --strip
)

# Add UPX compression if requested and available
if [ "$USE_UPX" = true ]; then
    echo -e "${CYAN}UPX compression enabled${NC}"
    PYINSTALLER_ARGS+=(--upx-dir upx)
fi

# Add icon if available (for macOS)
ICON_FILE="$PROJECT_ROOT/icon.icns"
if [ -f "$ICON_FILE" ]; then
    echo -e "${CYAN}Using icon: $ICON_FILE${NC}"
    PYINSTALLER_ARGS+=(--icon "$ICON_FILE")
fi

# Run PyInstaller
$PYTHON_CMD -m PyInstaller "${PYINSTALLER_ARGS[@]}" "$PROJECT_ROOT/src/gui.py"

# Create launcher script
echo ""
echo -e "${GREEN}Creating launcher script...${NC}"
LAUNCHER_FILE="$PROJECT_ROOT/dist/launch_nel_demo.sh"

cat > "$LAUNCHER_FILE" << 'EOF'
#!/bin/bash
# Launcher for NEL Demo

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Change to the script directory
cd "$SCRIPT_DIR"

# Run the application
./NEL_Demo/NEL_Demo
EOF

chmod +x "$LAUNCHER_FILE"
echo -e "${CYAN}Created: $LAUNCHER_FILE${NC}"

# Make the main executable also executable (just in case)
chmod +x "$PROJECT_ROOT/dist/NEL_Demo/NEL_Demo"

# Success message
echo ""
echo -e "${GREEN}================================================${NC}"
echo -e "${GREEN}  Build completed successfully!                ${NC}"
echo -e "${GREEN}================================================${NC}"
echo ""
echo -e "${YELLOW}Executable location:${NC}"
echo -e "${CYAN}  $PROJECT_ROOT/dist/NEL_Demo/${NC}"
echo ""
echo -e "${YELLOW}To run the application:${NC}"
echo -e "${CYAN}  1. Navigate to: dist/${NC}"
echo -e "${CYAN}  2. Run: ./launch_nel_demo.sh${NC}"
echo -e "${CYAN}     OR${NC}"
echo -e "${CYAN}  3. Navigate to: dist/NEL_Demo/${NC}"
echo -e "${CYAN}  4. Run: ./NEL_Demo${NC}"
echo ""

if [[ "$OSTYPE" == "darwin"* ]]; then
    echo -e "${YELLOW}To create a DMG installer, run:${NC}"
    echo -e "${CYAN}  ./build_scripts/create_installer_macos.sh${NC}"
else
    echo -e "${YELLOW}To create an AppImage, run:${NC}"
    echo -e "${CYAN}  ./build_scripts/create_installer_linux.sh${NC}"
fi
echo ""
