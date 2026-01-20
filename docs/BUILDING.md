# Building NEL Demo

Comprehensive guide for building standalone executables of NEL Demo for Windows, macOS, and Linux.

## Table of Contents

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Local Building](#local-building)
  - [Windows](#windows)
  - [macOS](#macos)
  - [Linux](#linux)
- [Creating Installers](#creating-installers)
- [Optimization Tips](#optimization-tips)
- [Automated Builds](#automated-builds)
- [Troubleshooting](#troubleshooting)
- [Code Signing](#code-signing-optional)

## Introduction

NEL Demo can be built as a standalone executable that users can run without having Python installed. This guide covers:

- Building executables locally for testing
- Creating professional installers
- Optimizing executable size
- Using automated GitHub Actions builds

## Prerequisites

### All Platforms

- **Python**: 3.10 or 3.11 (as specified in pyproject.toml)
- **pip**: Latest version
- **Virtual Environment**: Recommended for clean builds
- **PyInstaller**: Version 6.0 or higher (installed automatically by build scripts)

### Windows

- **PowerShell**: Built-in with Windows
- **NSIS** (for installers): [Download](https://nsis.sourceforge.io/Download) or install via Chocolatey:
  ```powershell
  choco install nsis
  ```

### macOS

- **Bash**: Built-in
- **Homebrew**: [Install Homebrew](https://brew.sh/)
- **create-dmg** (for DMG creation):
  ```bash
  brew install create-dmg
  ```

### Linux

- **Bash**: Built-in
- **python3-tk**: Required for GUI
  ```bash
  sudo apt-get install python3-tk  # Ubuntu/Debian
  sudo dnf install python3-tkinter  # Fedora
  ```
- **appimagetool** (for AppImage): Downloaded automatically by script

## Local Building

### Windows

1. **Open PowerShell** in the project root directory

2. **Run the build script**:
   ```powershell
   .\build_scripts\build_executable.ps1
   ```

3. **Optional flags**:
   ```powershell
   # Clean previous builds
   .\build_scripts\build_executable.ps1 -Clean
   
   # Enable UPX compression (if UPX is installed)
   .\build_scripts\build_executable.ps1 -UseUPX
   ```

4. **Output location**: `dist/NEL_Demo/`

5. **Run the executable**:
   ```powershell
   # Using launcher
   .\dist\Launch_NEL_Demo.bat
   
   # OR directly
   .\dist\NEL_Demo\NEL_Demo.exe
   ```

#### What the Script Does

- Checks Python version
- Activates virtual environment (if available)
- Installs/upgrades PyInstaller
- Updates build date in version.py
- Builds executable with optimized settings
- Bundles models, inputs, and data folders
- Excludes unnecessary modules to reduce size
- Creates launcher script

### macOS

1. **Open Terminal** in the project root directory

2. **Make script executable** (first time only):
   ```bash
   chmod +x ./build_scripts/build_executable.sh
   ```

3. **Run the build script**:
   ```bash
   ./build_scripts/build_executable.sh
   ```

4. **Optional flags**:
   ```bash
   # Clean previous builds
   ./build_scripts/build_executable.sh --clean
   
   # Enable UPX compression (if UPX is installed)
   ./build_scripts/build_executable.sh --use-upx
   ```

5. **Output location**: `dist/NEL_Demo/`

6. **Run the executable**:
   ```bash
   # Using launcher
   ./dist/launch_nel_demo.sh
   
   # OR directly
   ./dist/NEL_Demo/NEL_Demo
   ```

### Linux

Same as macOS (uses the same bash script):

1. **Open Terminal** in the project root directory

2. **Make script executable** (first time only):
   ```bash
   chmod +x ./build_scripts/build_executable.sh
   ```

3. **Run the build script**:
   ```bash
   ./build_scripts/build_executable.sh
   ```

4. **Optional flags**:
   ```bash
   ./build_scripts/build_executable.sh --clean
   ./build_scripts/build_executable.sh --use-upx
   ```

5. **Output location**: `dist/NEL_Demo/`

6. **Run the executable**:
   ```bash
   ./dist/launch_nel_demo.sh
   # OR
   ./dist/NEL_Demo/NEL_Demo
   ```

## Creating Installers

### Windows Installer (NSIS)

**Prerequisites**: NSIS must be installed

1. **Build the executable first** (see above)

2. **Run the installer creation script**:
   ```powershell
   .\build_scripts\create_installer_windows.ps1
   ```

3. **Specify version** (optional):
   ```powershell
   .\build_scripts\create_installer_windows.ps1 -Version "1.0.0"
   ```

4. **Output**: `dist/NEL_Demo_Setup_v1.0.0.exe`

**Features**:
- Modern UI with installation wizard
- Start Menu shortcuts
- Desktop shortcut option
- Uninstaller included
- Registry entries for proper uninstallation
- LZMA compression

### macOS DMG

**Prerequisites**: create-dmg (Homebrew)

1. **Build the executable first**

2. **Run the DMG creation script**:
   ```bash
   chmod +x ./build_scripts/create_installer_macos.sh
   ./build_scripts/create_installer_macos.sh
   ```

3. **Specify version** (optional):
   ```bash
   ./build_scripts/create_installer_macos.sh "1.0.0"
   ```

4. **Output**: `dist/NEL_Demo_v1.0.0.dmg`

**Features**:
- Drag-to-Applications folder UI
- Volume icon and branding
- Properly formatted .app bundle
- Info.plist metadata

### Linux AppImage

**Prerequisites**: appimagetool (downloaded automatically)

1. **Build the executable first**

2. **Run the AppImage creation script**:
   ```bash
   chmod +x ./build_scripts/create_installer_linux.sh
   ./build_scripts/create_installer_linux.sh
   ```

3. **Specify version** (optional):
   ```bash
   ./build_scripts/create_installer_linux.sh "1.0.0"
   ```

4. **Output**: 
   - `dist/NEL_Demo-v1.0.0-x86_64.AppImage`
   - `dist/NEL_Demo_Linux_v1.0.0.tar.gz` (alternative)

**Features**:
- Self-contained portable executable
- Desktop integration (.desktop file)
- No installation required
- Works on most Linux distributions

## Optimization Tips

### Reducing Executable Size

1. **Exclude unused modules** (already in build scripts):
   - matplotlib, pandas, IPython, jupyter
   - PIL/Pillow (if not used)
   - pytest and test frameworks

2. **Use UPX compression** (optional):
   - Install UPX: https://upx.github.io/
   - Add `--use-upx` flag to build script
   - Can reduce size by 30-50%
   - Trade-off: Slightly slower startup time

3. **Model management**:
   - Only include models you need
   - Consider downloading models on first run
   - Create "lite" versions without pre-bundled models

4. **Strip debug symbols**:
   - Automatically done by build scripts with `--strip` flag

### Improving Startup Performance

1. **Use onedir mode** (default):
   - Faster than onefile
   - Better for large applications

2. **Optimize imports**:
   - Lazy import heavy modules
   - Use runtime imports where possible

3. **Runtime hooks**:
   - `build_scripts/hook-spacy.py` optimizes spaCy loading
   - Customize for your specific needs

### Expected Sizes

Without heavy optimization:
- **Windows**: 200-400 MB
- **macOS**: 250-450 MB
- **Linux**: 200-400 MB

With models included, sizes may increase by 50-200 MB depending on model complexity.

## Automated Builds

### GitHub Actions Workflow

The `.github/workflows/build-releases.yml` workflow automatically builds executables and installers for all platforms.

#### Triggering Builds

**Option 1: Create a Git Tag**
```bash
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

**Option 2: Manual Workflow Dispatch**
1. Go to GitHub repository
2. Click "Actions" tab
3. Select "Build Releases" workflow
4. Click "Run workflow"
5. Enter version number

#### What Happens

1. **Three parallel build jobs** (Windows, macOS, Linux):
   - Check out code
   - Set up Python 3.11
   - Install dependencies
   - Build executable
   - Create installer
   - Generate SHA256 checksums
   - Upload artifacts

2. **Release creation job**:
   - Downloads all artifacts
   - Combines checksums
   - Generates release notes
   - Creates GitHub Release
   - Uploads all files

#### Artifacts

After successful build, the release includes:
- Windows installer (.exe)
- Windows portable (.zip)
- macOS DMG (.dmg)
- macOS portable (.zip)
- Linux AppImage (.AppImage)
- Linux tarball (.tar.gz)
- SHA256SUMS.txt (checksums for all files)

## Troubleshooting

### Common Issues

#### "Module not found" errors

**Problem**: PyInstaller missed a dependency

**Solution**:
```bash
# Add to build script hidden-import
--hidden-import module_name

# Or update build_scripts/hook-spacy.py
```

#### "Permission denied" on scripts

**Problem**: Scripts not executable (Linux/macOS)

**Solution**:
```bash
chmod +x ./build_scripts/*.sh
```

#### Large executable size

**Problem**: Executable is larger than expected

**Solution**:
1. Check what's being included: `pyinstaller --log-level DEBUG ...`
2. Add more exclusions to build script
3. Use UPX compression
4. Consider excluding models

#### GUI doesn't appear

**Problem**: Console window appears but no GUI (Windows)

**Solution**:
- Ensure `--windowed` flag is used
- Check tkinter is properly bundled
- Try running without `--windowed` to see errors

#### spaCy model not found

**Problem**: Model loading fails in executable

**Solution**:
1. Ensure model is in `models/` directory before building
2. Check `--add-data` includes models directory
3. Verify model path in application code

### Build Script Fails

#### Windows PowerShell Execution Policy

**Problem**: Script won't run

**Solution**:
```powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
```

#### Python not found

**Problem**: "Python is not recognized"

**Solution**:
- Ensure Python is in PATH
- Use full path to python.exe
- Reinstall Python with "Add to PATH" checked

### Platform-Specific Issues

#### macOS: "App is damaged"

**Problem**: macOS Gatekeeper blocks app

**Solution**:
```bash
# Remove quarantine attribute
xattr -cr /path/to/NEL_Demo.app

# Or right-click app and select "Open"
```

#### Linux: Missing libraries

**Problem**: Executable won't run due to missing .so files

**Solution**:
```bash
# Check missing dependencies
ldd dist/NEL_Demo/NEL_Demo

# Install missing packages
sudo apt-get install <package>
```

## Code Signing (Optional)

Code signing provides security and trust for distributed applications.

### Windows (Authenticode)

**Requirements**: Code signing certificate from trusted CA

```powershell
# Sign executable
signtool sign /f certificate.pfx /p password /t http://timestamp.digicert.com NEL_Demo.exe

# Verify signature
signtool verify /pa NEL_Demo.exe
```

### macOS (Developer ID)

**Requirements**: Apple Developer account ($99/year)

```bash
# Sign app bundle
codesign --deep --force --verify --verbose \
  --sign "Developer ID Application: Your Name" \
  NEL_Demo.app

# Verify signature
codesign --verify --deep --strict --verbose=2 NEL_Demo.app

# Notarize (required for macOS 10.15+)
xcrun notarytool submit NEL_Demo.dmg \
  --apple-id your@email.com \
  --team-id TEAM_ID \
  --password app-specific-password
```

### Linux

Linux typically doesn't require code signing, but you can sign with GPG:

```bash
# Sign AppImage
gpg --detach-sign --armor NEL_Demo.AppImage

# Verify
gpg --verify NEL_Demo.AppImage.asc NEL_Demo.AppImage
```

### Why Code Sign?

- **Windows**: Removes SmartScreen warnings
- **macOS**: Required for distribution outside Mac App Store
- **Trust**: Users know software hasn't been tampered with
- **Professional**: Shows commitment to security

## Additional Resources

- [PyInstaller Documentation](https://pyinstaller.org/en/stable/)
- [NSIS Documentation](https://nsis.sourceforge.io/Docs/)
- [create-dmg Repository](https://github.com/create-dmg/create-dmg)
- [AppImage Documentation](https://docs.appimage.org/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

## Support

For build issues:
1. Check this documentation
2. Review build script output
3. Open an issue on GitHub: https://github.com/te-sla/NEL_Demo/issues

---

**Made by [TESLA](https://tesla.rgf.bg.ac.rs/) and [Jerteh](https://jerteh.rs/)**
