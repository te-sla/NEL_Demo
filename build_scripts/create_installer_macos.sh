#!/bin/bash
# Script to create macOS DMG installer for NEL Demo
# Requires: create-dmg utility

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

VERSION="${1:-1.0.0}"

echo -e "${CYAN}================================================${NC}"
echo -e "${CYAN}  NEL Demo - macOS DMG Creator                 ${NC}"
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

# Check if app bundle exists
APP_BUNDLE="$DIST_DIR/NEL_Demo.app"
if [ ! -d "$APP_BUNDLE" ]; then
    # Try the onedir output instead
    if [ -d "$DIST_DIR/NEL_Demo" ]; then
        echo -e "${GREEN}Creating .app bundle from onedir output...${NC}"
        
        # Create .app structure
        mkdir -p "$APP_BUNDLE/Contents/MacOS"
        mkdir -p "$APP_BUNDLE/Contents/Resources"
        
        # Copy executable and resources
        cp -r "$DIST_DIR/NEL_Demo/"* "$APP_BUNDLE/Contents/MacOS/"
        
        # Create Info.plist
        cat > "$APP_BUNDLE/Contents/Info.plist" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>NEL_Demo</string>
    <key>CFBundleIdentifier</key>
    <string>rs.tesla.nel-demo</string>
    <key>CFBundleName</key>
    <string>NEL Demo</string>
    <key>CFBundleDisplayName</key>
    <string>NEL Demo</string>
    <key>CFBundleVersion</key>
    <string>$VERSION</string>
    <key>CFBundleShortVersionString</key>
    <string>$VERSION</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleSignature</key>
    <string>NELD</string>
    <key>NSHighResolutionCapable</key>
    <true/>
    <key>LSMinimumSystemVersion</key>
    <string>10.13</string>
</dict>
</plist>
EOF
        
        # Copy icon if available
        if [ -f "$PROJECT_ROOT/icon.icns" ]; then
            cp "$PROJECT_ROOT/icon.icns" "$APP_BUNDLE/Contents/Resources/"
            echo "    <key>CFBundleIconFile</key>" >> "$APP_BUNDLE/Contents/Info.plist.tmp"
            echo "    <string>icon.icns</string>" >> "$APP_BUNDLE/Contents/Info.plist.tmp"
        fi
        
        echo -e "${CYAN}Created: $APP_BUNDLE${NC}"
    else
        echo -e "${RED}Error: Executable not found in dist/${NC}"
        echo -e "${RED}Please run build_executable.sh first${NC}"
        exit 1
    fi
fi

# Check if create-dmg is installed
if ! command -v create-dmg &> /dev/null; then
    echo -e "${YELLOW}create-dmg not found. Installing via Homebrew...${NC}"
    
    if ! command -v brew &> /dev/null; then
        echo -e "${RED}Homebrew not found. Please install Homebrew first:${NC}"
        echo -e "${CYAN}  /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\"${NC}"
        echo ""
        echo -e "${YELLOW}Alternatively, install create-dmg manually from:${NC}"
        echo -e "${CYAN}  https://github.com/create-dmg/create-dmg${NC}"
        exit 1
    fi
    
    brew install create-dmg
fi

echo -e "${GREEN}Found create-dmg${NC}"
echo ""

# Create temporary directory for DMG contents
DMG_TEMP="$BUILD_DIR/dmg_temp"
rm -rf "$DMG_TEMP"
mkdir -p "$DMG_TEMP"

# Copy app bundle
cp -r "$APP_BUNDLE" "$DMG_TEMP/"

# Create Applications symlink
ln -s /Applications "$DMG_TEMP/Applications"

# Output DMG file
DMG_OUTPUT="$DIST_DIR/NEL_Demo_v$VERSION.dmg"
rm -f "$DMG_OUTPUT"

echo -e "${GREEN}Creating DMG image...${NC}"
echo ""

# Create DMG with create-dmg
create-dmg \
    --volname "NEL Demo" \
    --volicon "$PROJECT_ROOT/icon.icns" \
    --window-pos 200 120 \
    --window-size 600 400 \
    --icon-size 100 \
    --icon "NEL_Demo.app" 150 190 \
    --hide-extension "NEL_Demo.app" \
    --app-drop-link 450 190 \
    --no-internet-enable \
    "$DMG_OUTPUT" \
    "$DMG_TEMP" || {
        # If create-dmg fails, try hdiutil directly
        echo -e "${YELLOW}create-dmg failed, trying hdiutil...${NC}"
        
        hdiutil create -volname "NEL Demo" \
            -srcfolder "$DMG_TEMP" \
            -ov -format UDZO \
            "$DMG_OUTPUT"
    }

# Cleanup
rm -rf "$DMG_TEMP"

if [ -f "$DMG_OUTPUT" ]; then
    FILE_SIZE=$(du -h "$DMG_OUTPUT" | cut -f1)
    echo ""
    echo -e "${GREEN}================================================${NC}"
    echo -e "${GREEN}  DMG created successfully!                    ${NC}"
    echo -e "${GREEN}================================================${NC}"
    echo ""
    echo -e "${YELLOW}DMG location:${NC}"
    echo -e "${CYAN}  $DMG_OUTPUT${NC}"
    echo ""
    echo -e "${YELLOW}File size: $FILE_SIZE${NC}"
    echo ""
    echo -e "${GREEN}You can now distribute this DMG to macOS users.${NC}"
    echo ""
    echo -e "${YELLOW}To install:${NC}"
    echo -e "${CYAN}  1. Open the DMG file${NC}"
    echo -e "${CYAN}  2. Drag NEL Demo.app to Applications folder${NC}"
    echo -e "${CYAN}  3. Launch from Applications${NC}"
    echo ""
    
    # Code signing reminder
    echo -e "${YELLOW}Note: For distribution outside the Mac App Store,${NC}"
    echo -e "${YELLOW}you should code sign the app with a Developer ID:${NC}"
    echo -e "${CYAN}  codesign --deep --force --verify --verbose \\${NC}"
    echo -e "${CYAN}    --sign \"Developer ID Application: YOUR_NAME\" \\${NC}"
    echo -e "${CYAN}    \"$APP_BUNDLE\"${NC}"
    echo ""
else
    echo -e "${RED}Error: DMG creation failed${NC}"
    exit 1
fi
