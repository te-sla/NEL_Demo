# Build Scripts

This directory contains all the scripts and configuration files needed to build standalone executables and installers for NEL Demo.

## Overview

These scripts package NEL Demo into distributable executables that users can run without having Python installed. They use PyInstaller to bundle the Python interpreter and all dependencies into a single application.

## Files

### Build Scripts

- **`build_executable.ps1`** - Windows PowerShell script to build executable
  - Activates virtual environment
  - Installs PyInstaller
  - Builds executable with optimized settings
  - Creates launcher script
  - Usage: `.\build_executable.ps1 [-Clean] [-UseUPX]`

- **`build_executable.sh`** - Linux/macOS Bash script to build executable
  - Same functionality as PowerShell version
  - Cross-platform for Linux and macOS
  - Usage: `./build_executable.sh [--clean] [--use-upx]`

### Installer Creation Scripts

- **`create_installer_windows.ps1`** - Creates Windows NSIS installer
  - Requires NSIS installed
  - Generates professional installer with wizard
  - Usage: `.\create_installer_windows.ps1 [-Version "1.0.0"]`

- **`create_installer_macos.sh`** - Creates macOS DMG disk image
  - Requires create-dmg (Homebrew)
  - Creates drag-to-Applications DMG
  - Usage: `./create_installer_macos.sh ["1.0.0"]`

- **`create_installer_linux.sh`** - Creates Linux AppImage
  - Downloads appimagetool automatically
  - Creates universal Linux package
  - Also creates tarball alternative
  - Usage: `./create_installer_linux.sh ["1.0.0"]`

### Configuration Files

- **`build_config.py`** - PyInstaller spec file generator
  - Advanced configuration for builds
  - Conditional exclusions
  - Platform-specific settings
  - Usage: `python build_config.py [--use-upx]`

- **`hook-spacy.py`** - PyInstaller runtime hook for spaCy
  - Optimizes spaCy loading in executables
  - Collects necessary spaCy data
  - Excludes unnecessary components

- **`.pyinstaller-exclude-list.txt`** - List of modules to exclude
  - Reduces executable size
  - Excludes testing, documentation, and unused libraries

- **`installer_template.nsi`** - NSIS installer template
  - Modern UI configuration
  - Start Menu and Desktop shortcuts
  - Uninstaller generation
  - Registry entries

## Quick Start

### Building an Executable

#### Windows
```powershell
# Clean build
.\build_scripts\build_executable.ps1 -Clean

# Output: dist/NEL_Demo/NEL_Demo.exe
```

#### Linux/macOS
```bash
# Clean build
./build_scripts/build_executable.sh --clean

# Output: dist/NEL_Demo/NEL_Demo
```

### Creating an Installer

#### Windows (requires NSIS)
```powershell
.\build_scripts\create_installer_windows.ps1 -Version "1.0.0"
# Output: dist/NEL_Demo_Setup_v1.0.0.exe
```

#### macOS (requires create-dmg)
```bash
./build_scripts/create_installer_macos.sh "1.0.0"
# Output: dist/NEL_Demo_v1.0.0.dmg
```

#### Linux
```bash
./build_scripts/create_installer_linux.sh "1.0.0"
# Output: dist/NEL_Demo-v1.0.0-x86_64.AppImage
```

## How It Works

### PyInstaller Process

1. **Analysis**: PyInstaller analyzes your script to find all dependencies
2. **Collection**: Collects Python interpreter, libraries, and data files
3. **Bundling**: Packages everything into executable format
4. **Optimization**: Applies exclusions and compression

### Included Components

- Python interpreter (3.11)
- All dependencies (spacy, cyrtranslit, tkinter)
- Application code (`src/`)
- Models directory (`models/`)
- Input files (`inputs/`)
- Data directory (`data/`)

### Excluded Components (for size optimization)

- matplotlib, pandas, numpy (testing)
- IPython, jupyter (development)
- pytest (testing)
- Documentation tools
- Unused spaCy components

## Output Structure

### Windows
```
dist/
├── NEL_Demo/
│   ├── NEL_Demo.exe          # Main executable
│   ├── models/               # Bundled models
│   ├── inputs/               # Sample inputs
│   ├── data/                 # Data directory
│   └── _internal/            # PyInstaller files
└── Launch_NEL_Demo.bat       # Launcher script
```

### macOS
```
dist/
├── NEL_Demo.app/
│   ├── Contents/
│   │   ├── MacOS/
│   │   │   └── NEL_Demo      # Main executable
│   │   ├── Resources/
│   │   └── Info.plist
```

### Linux
```
dist/
├── NEL_Demo/
│   ├── NEL_Demo              # Main executable
│   ├── models/               # Bundled models
│   ├── inputs/               # Sample inputs
│   ├── data/                 # Data directory
│   └── _internal/            # PyInstaller files
└── launch_nel_demo.sh        # Launcher script
```

## Size Optimization

Expected sizes:
- **Base executable**: 150-250 MB
- **With models**: 200-500 MB (depending on model size)

### Techniques Used

1. **Module exclusion**: Removes unused libraries
2. **Strip symbols**: Removes debug information
3. **Onedir mode**: More efficient than onefile
4. **UPX compression** (optional): Reduces size by 30-50%

### Further Optimization

```powershell
# Enable UPX compression (requires UPX installed)
.\build_scripts\build_executable.ps1 -UseUPX
```

To reduce size further:
- Exclude larger models
- Use smaller spaCy models
- Download models on first run instead of bundling

## Troubleshooting

### Common Issues

**"Module not found" errors**
- Add to `--hidden-import` in build script
- Update `hook-spacy.py`

**Large executable size**
- Add exclusions to `.pyinstaller-exclude-list.txt`
- Use UPX compression
- Consider not bundling models

**GUI doesn't appear (Windows)**
- Ensure `--windowed` flag is used
- Check tkinter is properly bundled

**Missing dependencies in executable**
- Use `--collect-all` for the package
- Check PyInstaller analysis output

### Debug Mode

Remove `--windowed` flag to see console output:

```powershell
# In build_executable.ps1, temporarily remove:
# "--windowed"
```

This shows any runtime errors or import issues.

## Platform-Specific Notes

### Windows
- Requires PowerShell 5.0+
- NSIS needed for installers
- May trigger SmartScreen warnings (normal for unsigned executables)

### macOS
- Requires macOS 10.13+
- create-dmg installed via Homebrew
- Gatekeeper may block unsigned apps (right-click → Open)

### Linux
- Requires FUSE for AppImage
- Works on most distributions (Ubuntu 18.04+, Fedora 30+)
- AppImage is most portable format

## Automated Builds

These scripts are also used by GitHub Actions (`.github/workflows/build-releases.yml`) for automated releases. See [../docs/BUILDING.md](../docs/BUILDING.md) for details.

## References

- [PyInstaller Documentation](https://pyinstaller.org/)
- [NSIS Documentation](https://nsis.sourceforge.io/Docs/)
- [create-dmg](https://github.com/create-dmg/create-dmg)
- [AppImage](https://appimage.org/)

## Support

For build issues:
- Check [../docs/BUILDING.md](../docs/BUILDING.md)
- Review script output for errors
- Open issue on GitHub

---

**Last Updated**: 2026-01-20
