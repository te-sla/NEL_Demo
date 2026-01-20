# NEL Demo - spaCy NER+NEL GUI

**[🇷🇸 Srpska verzija / Serbian version](README.sr.md)**

A simple demonstration application for Named Entity Recognition (NER) and Named Entity Linking (NEL) using spaCy models with a minimal GUI interface.

## Features

- ✅ **Easy Installation**: Automated installers for Windows (PowerShell) and Linux/Mac (Bash)
- ✅ **Standalone Executables**: Pre-built executables for Windows, macOS, and Linux - **no Python required!**
- ✅ **Python Version Check**: Ensures Python 3.10 or higher is installed
- ✅ **Virtual Environment**: Automatically creates and manages a virtual environment
- ✅ **Flexible Dependencies**: Choose between standard spaCy or spacy-transformers
- ✅ **Simple GUI**: User-friendly interface built with tkinter
- ✅ **Model Management**: Load custom trained models from the `models/` directory
- ✅ **Text Processing**: Process any text and extract named entities
- ✅ **Cyrillic Transliteration**: Automatic transliteration from Cyrillic to Latin script for better NER accuracy
- ✅ **Smart Text Chunking**: Automatically handles large texts by chunking on paragraph boundaries
- ✅ **Visual Output**: Generate beautiful HTML visualizations using displaCy
- ✅ **Output Management**: Save all outputs to `data/outputs/` with timestamps
- ✅ **Comprehensive Testing**: Full test suite with pytest
- ✅ **Automated Builds**: GitHub Actions workflow for building releases on all platforms

## 📦 Downloading Pre-built Executables

**The easiest way to use NEL Demo is to download a pre-built executable - no Python installation required!**

### Download Links

Visit the [Releases page](https://github.com/te-sla/NEL_Demo/releases) to download the latest version for your platform:

#### Windows
- **Installer** (recommended): `NEL_Demo_Setup_v1.0.0.exe`
  - Professional installer with Start Menu shortcuts
  - Easy uninstallation through Control Panel
- **Portable**: `NEL_Demo_Windows_v1.0.0.zip`
  - No installation needed, run directly
  - Can be used from USB drive

#### macOS
- **DMG** (recommended): `NEL_Demo_v1.0.0.dmg`
  - Drag and drop to Applications folder
  - Native macOS experience
- **ZIP**: `NEL_Demo_macOS_v1.0.0.zip`
  - Alternative compressed format

#### Linux
- **AppImage** (recommended): `NEL_Demo-v1.0.0-x86_64.AppImage`
  - Universal Linux package
  - Works on most distributions
  - No installation required
- **Tarball**: `NEL_Demo_Linux_v1.0.0.tar.gz`
  - Manual installation option

### Quick Start

#### Windows
1. Download the installer
2. Run `NEL_Demo_Setup_v1.0.0.exe`
3. Follow installation wizard
4. Launch from Start Menu

#### macOS
1. Download the DMG file
2. Open it and drag NEL Demo to Applications
3. Right-click and select "Open" (first time only)

#### Linux
1. Download the AppImage
2. Make executable: `chmod +x NEL_Demo-v1.0.0-x86_64.AppImage`
3. Run: `./NEL_Demo-v1.0.0-x86_64.AppImage`

### Security Note

Verify file integrity using SHA256 checksums provided in `SHA256SUMS.txt`:

```bash
# Linux/macOS
sha256sum -c SHA256SUMS.txt

# Windows PowerShell
Get-FileHash <filename> -Algorithm SHA256
```

For detailed installation instructions, see [docs/DISTRIBUTING.md](docs/DISTRIBUTING.md).

## Project Structure

```
NEL_Demo/
├── install.ps1              # Windows installer (PowerShell)
├── install.sh               # Linux/Mac installer (Bash)
├── requirements.txt         # Python dependencies
├── README.md               # This file
├── src/
│   ├── gui.py              # Main GUI application
│   └── text_chunker.py     # Text chunking module for large documents
├── tests/
│   └── test_text_chunker.py # Test suite for text chunking
├── models/                 # Place your trained models here
│   └── {model_name}/
│       └── model-best/     # Your trained spaCy model
├── inputs/                 # Input text files
│   └── sample_text.txt     # Sample text file
├── data/
│   └── outputs/            # HTML visualization outputs
└── venv/                   # Virtual environment (created by installer)
```

## Requirements

### For Pre-built Executables (Recommended)

**No requirements!** Just download and run. Python is NOT needed.

- **Operating System**: Windows 10+, macOS 10.13+, or modern Linux
- **RAM**: 4 GB minimum, 8 GB recommended
- **Disk Space**: 500 MB free space

### For Development (Building from Source)

- **Python**: 3.10 or 3.11 (as specified in pyproject.toml)
- **Operating System**: Windows, Linux, or macOS
- **spaCy Model**: A trained spaCy model placed in `models/{model_name}/model-best/`
- **Additional tools**: For building executables, see [docs/BUILDING.md](docs/BUILDING.md)

## Installation

### Option 1: Pre-built Executables (Easiest)

Download from the [Releases page](https://github.com/te-sla/NEL_Demo/releases) and follow the quick start instructions above.

See [docs/DISTRIBUTING.md](docs/DISTRIBUTING.md) for detailed instructions.

### Option 2: Development Installation

For developers or users who want to run from source:

#### Windows (PowerShell)

1. Open PowerShell
2. Navigate to the project directory
3. Run the installer:

```powershell
.\install.ps1
```

### Linux/Mac (Bash)

1. Open a terminal
2. Navigate to the project directory
3. Run the installer:

```bash
./install.sh
```

### What the Installer Does

The installer will:
1. ✅ Check if Python 3.10+ is installed
2. ✅ Create a virtual environment in `venv/`
3. ✅ Activate the virtual environment
4. ✅ Upgrade pip to the latest version
5. ✅ Ask you to choose between:
   - Standard spaCy (faster, smaller)
   - spacy-transformers (more accurate, larger)
6. ✅ Install all required dependencies

## Setting Up a Model

### Pre-installed Model

A Serbian NER+NEL model (`trsic4-CNN-ner-nel`) is already installed in the `models/` directory and ready to use. No additional setup is required!

### Using Your Own Trained Model

If you have a trained spaCy model:

1. Create a directory: `models/{your_model_name}/`
2. Place your trained model in: `models/{your_model_name}/model-best/`

The structure should look like:
```
models/
└── your_model_name/
    └── model-best/
        ├── config.cfg
        ├── meta.json
        ├── tokenizer
        ├── ner/
        └── ... (other model files)
```

## Usage

### Starting the Application

**Windows:**
```powershell
.\venv\Scripts\Activate.ps1
python src/gui.py
```

**Linux/Mac:**
```bash
source venv/bin/activate
python src/gui.py
```

### Using the GUI

1. **Select a Model**: 
   - Choose your model from the dropdown
   - Click "Load Model" to load it
   - Wait for the confirmation message

2. **Configure Processing Options**:
   - **Transliterate Cyrillic to Latin**: Enabled by default (if `cyrtranslit` is installed)
   - This option automatically converts Cyrillic text to Latin before processing for better entity recognition

3. **Enter Text**:
   - Type or paste text into the input area
   - Or click "Load Sample Text" for a demo
   - Or click "Load from File" to load a text file from the `inputs/` folder

4. **Process Text**:
   - Click "Process Text (NER)" to analyze the text
   - View entities in the results section
   - HTML visualization is automatically saved

5. **View Results**:
   - Click "View Last Output" to open the HTML in your browser
   - Click "Open Output Folder" to see all saved outputs

### Cyrillic Transliteration Feature

The application includes automatic Cyrillic-to-Latin transliteration to improve NER accuracy when using models trained primarily on Latin script:

- **Automatic Conversion**: Converts Cyrillic text to Latin script (supports Serbian, Montenegrin, Macedonian, Russian, Ukrainian, Kazakh, and Bulgarian) before processing
- **Enabled by Default**: The transliteration option is checked by default (if `cyrtranslit` is installed)
- **Toggleable**: Can be disabled via the checkbox if you prefer to process Cyrillic text directly
- **Preserves Entities**: Latin text remains unchanged; only Cyrillic characters are transliterated
- **Better Accuracy**: Models trained on Latin script typically perform better with transliterated text

**Example**: The Cyrillic text "Новак Ђоковић рођен у Београду" is automatically transliterated to "Novak Đoković rođen u Beogradu" before being sent to the NER pipeline.

**Note**: If you have a model specifically trained on Cyrillic text, you can disable this option by unchecking the "Transliterate Cyrillic to Latin before processing" checkbox.

### Example

Try this sample text:
```
Apple Inc. is an American multinational technology company headquartered 
in Cupertino, California. Tim Cook is the CEO of Apple. The company was 
founded by Steve Jobs, Steve Wozniak, and Ronald Wayne in 1976.
```

The application will:
- Extract entities like "Apple Inc." (ORG), "Tim Cook" (PERS), "Cupertino" (LOC)
- Link entities to Wikidata (NEL) with Q-IDs where available
- Show entity labels and positions
- Generate an HTML visualization with highlighted entities
- Save the output to `data/outputs/ner_output_YYYYMMDD_HHMMSS.html`

**Note**: The Serbian NER+NEL model (`trsic4-CNN-ner-nel`) recognizes these entity types: PERS (person), LOC (location), ORG (organization), EVENT, DEMO (demonym), IDEO (ideology), PRODUCT, ROLE, and WORK.

### Text Processing with Paragraph Chunking

The application automatically uses chunking for any text with multiple paragraphs:
- **Smart Chunking**: Paragraphs are grouped into appropriately sized chunks (up to 100K chars each) to preserve logical structure and improve NER accuracy
- **Automatic Processing**: Each chunk is processed separately with spaCy NER
- **Merged Output**: All chunks are combined into a single HTML visualization
- **Visual Separation**: Section breaks are added between chunks in the output
- **Better Context**: Processing text with paragraph boundaries helps spaCy maintain clearer context for entity recognition

Single-paragraph texts are processed normally without chunking overhead. This approach ensures optimal NER performance while maintaining the readability and structure of the original text.

## Output Format

Each processed text generates an HTML file with:
- Original text with highlighted entities
- Color-coded entity types
- Interactive visualization
- Timestamp in the filename

Output files are saved in: `data/outputs/`

## Troubleshooting

### "Python is not installed or not in PATH"
- Install Python 3.10 or higher from [python.org](https://www.python.org/downloads/)
- Make sure to check "Add Python to PATH" during installation

### "No models found"
- Make sure you've placed a trained model in `models/{model_name}/model-best/`
- Check that the model directory structure is correct
- Try downloading a pre-trained model (see "Setting Up a Model")

### "Error loading model"
- Verify the model files are complete and not corrupted
- Make sure the model is compatible with your spaCy version
- Try re-downloading or re-training the model

### GUI doesn't start
- Make sure you've activated the virtual environment
- Check that all dependencies are installed: `pip list`
- On Linux, you may need to install tkinter: `sudo apt-get install python3-tk`

## Advanced Usage

### Training Your Own Model

To train a custom NER+NEL model with spaCy:

1. Prepare your training data
2. Create a spaCy project or config
3. Train the model:
   ```bash
   python -m spacy train config.cfg --output ./models/my_model
   ```
4. The trained model will be in `models/my_model/model-best/`

For more information, see the [spaCy training documentation](https://spacy.io/usage/training).

### Using Transformer Models

For better accuracy, use transformer-based models:

1. Install spacy-transformers during setup (option 2)
2. Train or download a transformer model
3. Place it in the models directory

Note: Transformer models are larger and slower but more accurate.

## Dependencies

Core dependencies (installed automatically):
- `spacy>=3.7.0` - Core NLP library
- `cyrtranslit>=1.0.0` - Cyrillic-to-Latin transliteration
- `tkinter-tooltip>=2.0.0` - GUI tooltips (optional)

Optional:
- `spacy-transformers` - For transformer-based models

Development dependencies:
- `pytest` - For running tests

## Testing

The project includes comprehensive tests for the text chunking functionality.

To run the tests:

```bash
# Activate the virtual environment first
# Windows:
.\venv\Scripts\Activate.ps1

# Linux/Mac:
source venv/bin/activate

# Install pytest (if not already installed)
pip install pytest

# Run all tests
python -m pytest tests/test_text_chunker.py -v

# Run specific test class
python -m pytest tests/test_text_chunker.py::TestChunkText -v
```

The test suite includes:
- **Paragraph splitting tests**: Verify correct handling of various paragraph formats
- **Text chunking tests**: Ensure proper chunking at different size limits
- **HTML merging tests**: Validate correct merging of multiple HTML outputs
- **Edge case tests**: Test Unicode, special characters, very long sentences
- **Integration tests**: End-to-end workflow validation

## 🔨 Building Standalone Executables

Want to build your own standalone executables? The project includes comprehensive build scripts for all platforms.

### Prerequisites

- Python 3.10 or 3.11
- PyInstaller (installed automatically by build scripts)
- Platform-specific tools (optional, for creating installers)

### Quick Build

#### Windows
```powershell
.\build_scripts\build_executable.ps1 -Clean
```

#### Linux/macOS
```bash
./build_scripts/build_executable.sh --clean
```

### Creating Installers

#### Windows (NSIS)
```powershell
.\build_scripts\create_installer_windows.ps1 -Version "1.0.0"
```

#### macOS (DMG)
```bash
./build_scripts/create_installer_macos.sh "1.0.0"
```

#### Linux (AppImage)
```bash
./build_scripts/create_installer_linux.sh "1.0.0"
```

### Build Output

- **Executables**: `dist/NEL_Demo/`
- **Installers**: `dist/`
- **Expected size**: 200-500 MB depending on platform and optimization

### Detailed Documentation

For comprehensive building instructions, see [docs/BUILDING.md](docs/BUILDING.md), which covers:

- Local building on all platforms
- Creating professional installers
- Size optimization techniques
- Troubleshooting build issues
- Automated builds with GitHub Actions
- Code signing (optional)

## 🚀 Creating Releases

For maintainers who want to create official releases with automated builds:

### Automatic Build on Tag Push

The easiest way to trigger a release build:

```bash
# Create and push a version tag
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

This automatically:
1. Builds executables for Windows, macOS, and Linux
2. Creates installers for all platforms
3. Generates SHA256 checksums
4. Creates a GitHub Release with all artifacts
5. Publishes release notes

### Manual Workflow Dispatch

Alternatively, trigger builds manually:

1. Go to GitHub repository → Actions tab
2. Select "Build Releases" workflow
3. Click "Run workflow"
4. Enter version number (e.g., "1.0.0")
5. Click "Run workflow"

### What Gets Built

Each release includes:

- **Windows**: 
  - `NEL_Demo_Setup_v1.0.0.exe` (installer)
  - `NEL_Demo_Windows_v1.0.0.zip` (portable)
- **macOS**: 
  - `NEL_Demo_v1.0.0.dmg` (disk image)
  - `NEL_Demo_macOS_v1.0.0.zip` (app bundle)
- **Linux**: 
  - `NEL_Demo-v1.0.0-x86_64.AppImage` (universal)
  - `NEL_Demo_Linux_v1.0.0.tar.gz` (tarball)
- **Security**: `SHA256SUMS.txt` (checksums for verification)

### Release Workflow

The automated workflow (`.github/workflows/build-releases.yml`):

1. **Build Jobs** (parallel):
   - Sets up Python 3.11
   - Installs dependencies
   - Builds executable with PyInstaller
   - Creates platform-specific installer
   - Generates checksums
   - Uploads artifacts

2. **Release Job**:
   - Downloads all artifacts
   - Combines checksums
   - Generates release notes
   - Creates GitHub Release
   - Uploads all files

See [docs/BUILDING.md](docs/BUILDING.md) for more details on the automated build process.

## License

This project is dedicated to the public domain under CC0 1.0 Universal (CC0 1.0) Public Domain Dedication - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues or questions:
- Check the troubleshooting section
- Visit [spaCy documentation](https://spacy.io/)
- Open an issue on GitHub

## Acknowledgments

- Built with [spaCy](https://spacy.io/)
- Visualization powered by [displaCy](https://spacy.io/usage/visualizers)
- GUI built with Python's tkinter

Made by:
- [**TESLA** - Text Embeddings - Serbian Language Applications](https://tesla.rgf.bg.ac.rs/)
- [**Language Resources and Technologies Society - Jerteh**](https://jerteh.rs/)

---

**Happy Entity Recognition! 🎯**