# NEL Demo - Installation and User Guide

Guide for end users to install and run NEL Demo standalone executables.

## Table of Contents

- [Overview](#overview)
- [System Requirements](#system-requirements)
- [Downloading](#downloading)
- [Installation](#installation)
  - [Windows](#windows)
  - [macOS](#macos)
  - [Linux](#linux)
- [First Run](#first-run)
- [Using the Application](#using-the-application)
- [Troubleshooting](#troubleshooting)
- [Uninstallation](#uninstallation)
- [FAQ](#faq)

## Overview

NEL Demo is a standalone application for Named Entity Recognition (NER) and Named Entity Linking (NEL) using spaCy models. **No Python installation required!**

### What's Included

- Complete NEL Demo application
- Pre-trained Serbian NER+NEL model
- Sample texts for testing
- HTML visualization tools
- User-friendly GUI

## System Requirements

### Minimum Requirements

#### Windows
- **OS**: Windows 10 or later (64-bit)
- **RAM**: 4 GB minimum, 8 GB recommended
- **Disk Space**: 500 MB free space
- **Display**: 1024x768 or higher

#### macOS
- **OS**: macOS 10.13 (High Sierra) or later
- **RAM**: 4 GB minimum, 8 GB recommended
- **Disk Space**: 500 MB free space
- **Display**: 1024x768 or higher

#### Linux
- **OS**: Most modern distributions (Ubuntu 18.04+, Fedora 30+, Debian 10+, etc.)
- **RAM**: 4 GB minimum, 8 GB recommended
- **Disk Space**: 500 MB free space
- **Display**: 1024x768 or higher
- **Dependencies**: Usually none (AppImage is self-contained)

### Recommended Requirements

- **RAM**: 8 GB or more
- **Disk Space**: 1 GB free space
- **Display**: 1920x1080 or higher

## Downloading

### From GitHub Releases

1. Visit: https://github.com/te-sla/NEL_Demo/releases
2. Find the latest release
3. Download the appropriate file for your platform:

#### Windows
- **Recommended**: `NEL_Demo_Setup_v1.0.0.exe` (Installer)
- **Alternative**: `NEL_Demo_Windows_v1.0.0.zip` (Portable)

#### macOS
- **Recommended**: `NEL_Demo_v1.0.0.dmg` (Disk Image)
- **Alternative**: `NEL_Demo_macOS_v1.0.0.zip` (Compressed app)

#### Linux
- **Recommended**: `NEL_Demo-v1.0.0-x86_64.AppImage` (Universal)
- **Alternative**: `NEL_Demo_Linux_v1.0.0.tar.gz` (Tarball)

### Verifying Downloads

For security, verify file integrity using SHA256 checksums:

**Windows (PowerShell)**:
```powershell
Get-FileHash NEL_Demo_Setup_v1.0.0.exe -Algorithm SHA256
```

**macOS/Linux**:
```bash
sha256sum NEL_Demo-v1.0.0-x86_64.AppImage
```

Compare the output with values in `SHA256SUMS.txt` from the release.

## Installation

### Windows

#### Method 1: Installer (Recommended)

1. **Download** `NEL_Demo_Setup_v1.0.0.exe`

2. **Run the installer**:
   - Double-click the downloaded file
   - Windows may show a SmartScreen warning (click "More info" → "Run anyway")
   - Follow the installation wizard

3. **Choose installation options**:
   - Installation location (default: `C:\Program Files\NEL Demo`)
   - Start Menu shortcuts
   - Desktop shortcut

4. **Complete installation**:
   - Click "Install"
   - Wait for installation to complete
   - Click "Finish"

5. **Launch the application**:
   - From Start Menu: Search "NEL Demo"
   - From Desktop: Double-click "NEL Demo" icon
   - From installation folder: Run `NEL_Demo.exe`

#### Method 2: Portable (No Installation)

1. **Download** `NEL_Demo_Windows_v1.0.0.zip`

2. **Extract the archive**:
   - Right-click → "Extract All..."
   - Choose a location (e.g., `C:\Programs\NEL_Demo`)

3. **Run the application**:
   - Option A: Double-click `Launch_NEL_Demo.bat`
   - Option B: Open `NEL_Demo` folder and run `NEL_Demo.exe`

**Portable Benefits**:
- No installation required
- Can run from USB drive
- Easy to move or delete
- No registry entries

### macOS

#### Method 1: DMG (Recommended)

1. **Download** `NEL_Demo_v1.0.0.dmg`

2. **Open the DMG file**:
   - Double-click the downloaded file
   - A window will open showing the NEL Demo icon

3. **Install the application**:
   - Drag the "NEL Demo" icon to the "Applications" folder
   - Wait for the copy to complete
   - Eject the DMG (right-click → Eject)

4. **Launch the application**:
   - Open "Applications" folder
   - Find "NEL Demo"
   - Right-click → "Open" (first time only)
   - Click "Open" in the security dialog

**Note**: On first launch, macOS Gatekeeper may show a warning. Right-click the app and select "Open" to bypass this.

#### Method 2: ZIP Archive

1. **Download** `NEL_Demo_macOS_v1.0.0.zip`

2. **Extract**:
   - Double-click the ZIP file
   - Move `NEL_Demo.app` to Applications folder

3. **Launch**:
   - Right-click → "Open" (first time only)

### Linux

#### Method 1: AppImage (Recommended)

1. **Download** `NEL_Demo-v1.0.0-x86_64.AppImage`

2. **Make it executable**:
   ```bash
   chmod +x NEL_Demo-v1.0.0-x86_64.AppImage
   ```

3. **Run the application**:
   ```bash
   ./NEL_Demo-v1.0.0-x86_64.AppImage
   ```

**Optional: Desktop Integration**
```bash
# Move to a permanent location
mkdir -p ~/Applications
mv NEL_Demo-v1.0.0-x86_64.AppImage ~/Applications/

# Create desktop shortcut (Ubuntu/GNOME)
cat > ~/.local/share/applications/nel-demo.desktop << EOF
[Desktop Entry]
Type=Application
Name=NEL Demo
Exec=$HOME/Applications/NEL_Demo-v1.0.0-x86_64.AppImage
Icon=nel-demo
Categories=Science;Education;
Terminal=false
EOF
```

#### Method 2: Tarball

1. **Download** `NEL_Demo_Linux_v1.0.0.tar.gz`

2. **Extract**:
   ```bash
   tar -xzf NEL_Demo_Linux_v1.0.0.tar.gz
   cd NEL_Demo
   ```

3. **Run**:
   ```bash
   ./NEL_Demo
   ```

## First Run

### Initial Setup

On first launch, the application will:

1. **Load the GUI** - May take 5-10 seconds initially
2. **Scan for models** - Detects pre-installed Serbian model
3. **Initialize directories** - Creates `data/outputs/` for results

### Loading a Model

1. **Select model** from dropdown (e.g., "trsic4-CNN-ner-nel")
2. **Click "Load Model"**
3. **Wait** for confirmation (10-20 seconds)
4. **Model is ready** when status turns green

### Quick Test

1. **Click "Load Sample Text"** - Loads Serbian sample text
2. **Click "Process Text (NER)"** - Analyzes entities
3. **View results** in the results panel
4. **Click "View Last Output"** - Opens HTML visualization in browser

## Using the Application

### Basic Workflow

1. **Load a model** (one time per session)
2. **Enter or load text** to analyze
3. **Configure options** (e.g., transliteration)
4. **Process the text** to extract entities
5. **View results** and visualizations

### Features

#### Text Input Methods

- **Type directly** in the text area
- **Load sample text** for demonstration
- **Load from file** (supports .txt files up to 10 MB)
- **Paste** from clipboard

#### Processing Options

- **Transliterate Cyrillic to Latin**: Enabled by default for better entity recognition with models trained on Latin script

#### Results

- **Entity list** with labels and positions
- **HTML visualization** with color-coded entities
- **Entity counts** and statistics
- **Automatic chunking** for large texts

#### Output Management

- **Timestamped HTML files** in `data/outputs/`
- **Open last output** in browser
- **Access output folder** directly

### Tips for Best Results

1. **Model Selection**: Use the pre-installed Serbian model for Serbian text
2. **Text Quality**: Clean, well-formatted text works best
3. **Transliteration**: Keep enabled for Cyrillic text if your model expects Latin script
4. **Large Texts**: The app automatically chunks large texts for better processing
5. **Outputs**: Check the HTML visualizations for beautiful entity highlighting

## Troubleshooting

### Application Won't Start

#### Windows

**Problem**: Double-clicking does nothing

**Solutions**:
- Right-click → "Run as administrator"
- Check if antivirus is blocking (add exception)
- Install Visual C++ Redistributable if missing
- Try portable version instead

**Problem**: "Windows protected your PC" warning

**Solution**: Click "More info" → "Run anyway"

#### macOS

**Problem**: "App is damaged and can't be opened"

**Solutions**:
```bash
# Remove quarantine attribute
xattr -cr /Applications/NEL\ Demo.app

# Or
sudo spctl --master-disable  # Disable Gatekeeper (not recommended)
```

**Problem**: "App can't be opened because it is from an unidentified developer"

**Solution**: Right-click → "Open" → Click "Open" in dialog

#### Linux

**Problem**: AppImage won't run

**Solutions**:
```bash
# Ensure it's executable
chmod +x NEL_Demo-v1.0.0-x86_64.AppImage

# Check for FUSE (required for AppImage)
sudo apt-get install fuse libfuse2

# Or extract and run directly
./NEL_Demo-v1.0.0-x86_64.AppImage --appimage-extract
./squashfs-root/AppRun
```

### Application Issues

#### Model Won't Load

**Problem**: "Error loading model"

**Solutions**:
- Ensure sufficient RAM (4+ GB)
- Close other applications
- Restart the application
- Try a smaller model if available

#### Text Processing Fails

**Problem**: Error during processing

**Solutions**:
- Check text isn't too long (>10 MB)
- Ensure text is in supported format
- Try with smaller text first
- Check error message for specifics

#### GUI Looks Strange

**Problem**: UI elements are misaligned or missing

**Solutions**:
- Try resizing the window
- Check display scaling (100% recommended)
- Update graphics drivers
- Restart application

### Performance Issues

#### Slow Startup

**Expected**: First launch may take 10-15 seconds

**If slower**:
- Close unnecessary applications
- Ensure app is on local drive (not network)
- Check antivirus isn't scanning app

#### Slow Processing

**Expected**: 1-2 seconds per 1000 words

**If slower**:
- Close memory-intensive applications
- Process smaller chunks of text
- Consider system RAM upgrade

### File Issues

#### Can't Load Text Files

**Problem**: "Error loading file"

**Solutions**:
- Check file size (<10 MB)
- Ensure file encoding is UTF-8
- Check file isn't corrupted
- Try copying text instead

#### Can't View Output

**Problem**: "View Last Output" does nothing

**Solutions**:
- Check default browser is set
- Look for files in `data/outputs/`
- Open HTML files manually
- Check disk space

## Uninstallation

### Windows

#### Installer Version
1. **Control Panel** → "Programs and Features"
2. Find "NEL Demo"
3. Click "Uninstall"
4. Follow uninstaller prompts

#### Portable Version
- Simply delete the extracted folder

### macOS

1. Open "Applications" folder
2. Drag "NEL Demo" to Trash
3. Empty Trash

**Optional**: Remove preferences
```bash
rm -rf ~/Library/Preferences/rs.tesla.nel-demo*
```

### Linux

#### AppImage
- Delete the AppImage file
- Remove desktop shortcut if created:
  ```bash
  rm ~/.local/share/applications/nel-demo.desktop
  ```

#### Tarball
- Delete the extracted folder

## FAQ

### General Questions

**Q: Do I need Python installed?**
A: No! The standalone executable includes everything needed.

**Q: How much disk space does it need?**
A: Approximately 300-500 MB depending on platform.

**Q: Can I run it from a USB drive?**
A: Yes! Use the portable/AppImage versions.

**Q: Is my data stored online?**
A: No. Everything runs locally on your computer.

**Q: Can I use my own models?**
A: Yes, but this requires building from source. See BUILDING.md.

### Technical Questions

**Q: What languages are supported?**
A: The pre-installed model supports Serbian. Other models can be added.

**Q: How accurate is the entity recognition?**
A: Depends on the model and text quality. The Serbian model is optimized for Serbian text.

**Q: Can I process multiple files at once?**
A: Currently, process files one at a time through the GUI.

**Q: What file formats are supported?**
A: Plain text (.txt) files. HTML output for visualizations.

### Privacy & Security

**Q: Is my text sent anywhere?**
A: No. All processing happens locally on your computer.

**Q: Is it safe to download?**
A: Yes. Verify SHA256 checksums and download from official GitHub releases.

**Q: Why does antivirus flag it?**
A: Some antivirus programs flag PyInstaller executables. This is a false positive.

## Getting Help

### Support Channels

- **Issues**: https://github.com/te-sla/NEL_Demo/issues
- **Documentation**: https://github.com/te-sla/NEL_Demo
- **Email**: Contact through GitHub

### Before Reporting Issues

1. Check this troubleshooting guide
2. Verify you have the latest version
3. Check existing GitHub issues
4. Note your OS version and error messages

### Useful Information to Include

- Operating system and version
- NEL Demo version
- Steps to reproduce the problem
- Error messages (exact text)
- Screenshots if relevant

## Additional Resources

- **Project Homepage**: https://tesla.rgf.bg.ac.rs/
- **GitHub Repository**: https://github.com/te-sla/NEL_Demo
- **TESLA**: https://tesla.rgf.bg.ac.rs/
- **Jerteh**: https://jerteh.rs/

---

**Made by [TESLA](https://tesla.rgf.bg.ac.rs/) - Text Embeddings - Serbian Language Applications**  
**and [Language Resources and Technologies Society - Jerteh](https://jerteh.rs/)**

**License**: CC0 1.0 Universal (Public Domain)
