# Changelog

All notable changes to NEL Demo will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-01-20

### Added
- **Standalone Executables**: Pre-built executables for Windows, macOS, and Linux
  - Windows: `.exe` installer and portable ZIP
  - macOS: `.dmg` disk image
  - Linux: `.AppImage` and `.tar.gz`
- **Automated Builds**: GitHub Actions workflow for building releases on all platforms
- **Build Scripts**: Platform-specific build scripts using PyInstaller
  - `build_executable.ps1` for Windows
  - `build_executable.sh` for Linux/macOS
  - Advanced configuration with `build_config.py`
- **Installer Creation**: Professional installers for each platform
  - NSIS installer for Windows
  - DMG creator for macOS
  - AppImage bundler for Linux
- **Size Optimization**: Techniques to reduce executable size
  - Excluded unused modules
  - UPX compression support (optional)
  - Runtime hooks for spaCy optimization
- **Version Display**: About dialog showing version and build information
- **Comprehensive Documentation**:
  - `docs/BUILDING.md` - Building guide for developers
  - `docs/DISTRIBUTING.md` - Installation guide for end users
  - Updated README with download instructions

### Changed
- Updated GUI with Help → About menu item
- Enhanced README with pre-built executable download instructions
- Added version information display in application

### Technical Details
- PyInstaller 6.0+ support
- Python 3.10-3.11 compatibility
- Automated CI/CD pipeline for releases
- SHA256 checksums for all releases
- Code signing support (optional)

## [0.9.0] - Previous Release

### Features
- Named Entity Recognition (NER) with spaCy
- Named Entity Linking (NEL) with Wikidata
- Simple GUI with tkinter
- Cyrillic transliteration support
- Smart text chunking for large documents
- HTML visualization with displaCy
- Comprehensive test suite
