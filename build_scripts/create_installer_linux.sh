#!/bin/bash
# Script to create Linux AppImage for NEL Demo
# Requires: appimagetool or linuxdeploy

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

VERSION="${1:-1.0.0}"

echo -e "${CYAN}================================================${NC}"
echo -e "${CYAN}  NEL Demo - Linux AppImage Creator            ${NC}"
echo -e "${CYAN}================================================${NC}"
echo ""

# Get directories
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"
DIST_DIR="$PROJECT_ROOT/dist"
BUILD_DIR="$PROJECT_ROOT/build"

echo -e "${YELLOW}Project root: $PROJECT_ROOT${NC}"
echo -e "${YELLOW}Version: $VERSION${NC}"
echo ""

# Check if executable exists
if [ ! -d "$DIST_DIR/NEL_Demo" ]; then
    echo -e "${RED}Error: Executable not found in dist/NEL_Demo/${NC}"
    echo -e "${RED}Please run build_executable.sh first${NC}"
    exit 1
fi

# Create AppDir structure
APPDIR="$BUILD_DIR/NEL_Demo.AppDir"
rm -rf "$APPDIR"
mkdir -p "$APPDIR/usr/bin"
mkdir -p "$APPDIR/usr/share/applications"
mkdir -p "$APPDIR/usr/share/icons/hicolor/256x256/apps"
mkdir -p "$APPDIR/usr/share/metainfo"

echo -e "${GREEN}Creating AppDir structure...${NC}"

# Copy executable and resources
cp -r "$DIST_DIR/NEL_Demo" "$APPDIR/usr/bin/"

# Create wrapper script
cat > "$APPDIR/usr/bin/nel-demo" << 'EOF'
#!/bin/bash
# Wrapper script for NEL Demo

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Run the application
exec "$SCRIPT_DIR/NEL_Demo/NEL_Demo" "$@"
EOF

chmod +x "$APPDIR/usr/bin/nel-demo"

# Create .desktop file
cat > "$APPDIR/usr/share/applications/nel-demo.desktop" << EOF
[Desktop Entry]
Type=Application
Name=NEL Demo
Comment=Named Entity Recognition and Linking Demo
Exec=nel-demo
Icon=nel-demo
Categories=Science;Education;
Terminal=false
StartupNotify=true
EOF

# Copy .desktop file to AppDir root (required by AppImage)
cp "$APPDIR/usr/share/applications/nel-demo.desktop" "$APPDIR/"

# Create or copy icon
ICON_SOURCE="$PROJECT_ROOT/icon.png"
ICON_DEST="$APPDIR/usr/share/icons/hicolor/256x256/apps/nel-demo.png"

if [ -f "$ICON_SOURCE" ]; then
    cp "$ICON_SOURCE" "$ICON_DEST"
    cp "$ICON_SOURCE" "$APPDIR/nel-demo.png"
else
    # Create a simple placeholder icon if none exists
    echo -e "${YELLOW}Warning: icon.png not found, creating placeholder${NC}"
    # This would need ImageMagick or similar to create an actual icon
    # For now, we'll just create a symlink to a default icon if available
    if [ -f "/usr/share/pixmaps/python3.png" ]; then
        cp "/usr/share/pixmaps/python3.png" "$ICON_DEST"
        cp "/usr/share/pixmaps/python3.png" "$APPDIR/nel-demo.png"
    fi
fi

# Create AppStream metadata
cat > "$APPDIR/usr/share/metainfo/nel-demo.appdata.xml" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<component type="desktop-application">
  <id>rs.tesla.NELDemo</id>
  <name>NEL Demo</name>
  <summary>Named Entity Recognition and Linking Demo</summary>
  <metadata_license>CC0-1.0</metadata_license>
  <project_license>CC0-1.0</project_license>
  <description>
    <p>
      A demonstration application for Named Entity Recognition (NER) and 
      Named Entity Linking (NEL) using spaCy models with a minimal GUI interface.
    </p>
  </description>
  <url type="homepage">https://github.com/te-sla/NEL_Demo</url>
  <developer_name>TESLA &amp; Jerteh</developer_name>
  <releases>
    <release version="$VERSION" date="$(date +%Y-%m-%d)"/>
  </releases>
</component>
EOF

# Create AppRun script
cat > "$APPDIR/AppRun" << 'EOF'
#!/bin/bash
# AppRun script for NEL Demo

# Get the directory where this AppImage is mounted
HERE="$(dirname "$(readlink -f "${0}")")"

# Set up environment
export PATH="${HERE}/usr/bin:${PATH}"
export LD_LIBRARY_PATH="${HERE}/usr/lib:${LD_LIBRARY_PATH}"

# Run the application
exec "${HERE}/usr/bin/nel-demo" "$@"
EOF

chmod +x "$APPDIR/AppRun"

echo -e "${CYAN}AppDir created: $APPDIR${NC}"
echo ""

# Check for appimagetool
APPIMAGETOOL=""

if command -v appimagetool &> /dev/null; then
    APPIMAGETOOL="appimagetool"
elif [ -f "$HOME/.local/bin/appimagetool-x86_64.AppImage" ]; then
    APPIMAGETOOL="$HOME/.local/bin/appimagetool-x86_64.AppImage"
fi

# Download appimagetool if not found
if [ -z "$APPIMAGETOOL" ]; then
    echo -e "${YELLOW}appimagetool not found. Downloading...${NC}"
    
    APPIMAGETOOL="$BUILD_DIR/appimagetool-x86_64.AppImage"
    curl -L "https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage" \
        -o "$APPIMAGETOOL"
    chmod +x "$APPIMAGETOOL"
    
    echo -e "${CYAN}Downloaded appimagetool${NC}"
fi

echo -e "${GREEN}Building AppImage...${NC}"
echo ""

# Output AppImage file
APPIMAGE_OUTPUT="$DIST_DIR/NEL_Demo-v$VERSION-x86_64.AppImage"
rm -f "$APPIMAGE_OUTPUT"

# Build AppImage
ARCH=x86_64 "$APPIMAGETOOL" "$APPDIR" "$APPIMAGE_OUTPUT"

if [ $? -eq 0 ] && [ -f "$APPIMAGE_OUTPUT" ]; then
    FILE_SIZE=$(du -h "$APPIMAGE_OUTPUT" | cut -f1)
    
    echo ""
    echo -e "${GREEN}================================================${NC}"
    echo -e "${GREEN}  AppImage created successfully!               ${NC}"
    echo -e "${GREEN}================================================${NC}"
    echo ""
    echo -e "${YELLOW}AppImage location:${NC}"
    echo -e "${CYAN}  $APPIMAGE_OUTPUT${NC}"
    echo ""
    echo -e "${YELLOW}File size: $FILE_SIZE${NC}"
    echo ""
    echo -e "${GREEN}You can now distribute this AppImage to Linux users.${NC}"
    echo ""
    echo -e "${YELLOW}To install and run:${NC}"
    echo -e "${CYAN}  chmod +x NEL_Demo-v$VERSION-x86_64.AppImage${NC}"
    echo -e "${CYAN}  ./NEL_Demo-v$VERSION-x86_64.AppImage${NC}"
    echo ""
    
    # Create tarball as alternative
    echo -e "${GREEN}Creating tarball alternative...${NC}"
    TARBALL="$DIST_DIR/NEL_Demo_Linux_v$VERSION.tar.gz"
    tar -czf "$TARBALL" -C "$DIST_DIR" NEL_Demo
    
    if [ -f "$TARBALL" ]; then
        TARBALL_SIZE=$(du -h "$TARBALL" | cut -f1)
        echo -e "${CYAN}Created tarball: $TARBALL ($TARBALL_SIZE)${NC}"
    fi
    echo ""
else
    echo -e "${RED}Error: AppImage creation failed${NC}"
    exit 1
fi

# Cleanup
# Keep AppDir for debugging if needed
# rm -rf "$APPDIR"
