# NEL Demo - spaCy NER+NEL GUI

A simple demonstration application for Named Entity Recognition (NER) and Named Entity Linking (NEL) using spaCy models with a minimal GUI interface.

## Features

- ✅ **Easy Installation**: Automated installers for Windows (PowerShell) and Linux/Mac (Bash)
- ✅ **Python Version Check**: Ensures Python 3.10 or higher is installed
- ✅ **Virtual Environment**: Automatically creates and manages a virtual environment
- ✅ **Flexible Dependencies**: Choose between standard spaCy or spacy-transformers
- ✅ **Simple GUI**: User-friendly interface built with tkinter
- ✅ **Model Management**: Load custom trained models from the `models/` directory
- ✅ **Text Processing**: Process any text and extract named entities
- ✅ **Smart Text Chunking**: Automatically handles large texts by chunking on paragraph boundaries
- ✅ **Visual Output**: Generate beautiful HTML visualizations using displaCy
- ✅ **Output Management**: Save all outputs to `data/outputs/` with timestamps
- ✅ **Comprehensive Testing**: Full test suite with pytest

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
├── data/
│   └── outputs/            # HTML visualization outputs
└── venv/                   # Virtual environment (created by installer)
```

## Requirements

- **Python**: 3.10 or higher
- **Operating System**: Windows, Linux, or macOS
- **spaCy Model**: A trained spaCy model placed in `models/{model_name}/model-best/`

## Installation

### Windows (PowerShell)

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

### Option 1: Download a Pre-trained Model

After installation, activate your virtual environment and download a spaCy model:

**Windows:**
```powershell
.\venv\Scripts\Activate.ps1
python -m spacy download en_core_web_sm
```

**Linux/Mac:**
```bash
source venv/bin/activate
python -m spacy download en_core_web_sm
```

Then create the directory structure and copy the model:
```bash
# Create the directory structure
mkdir -p models/en_core_web_sm/model-best

# Find and copy the model (the actual model is in a versioned subdirectory)
# Linux/Mac:
python -c "import en_core_web_sm, shutil, pathlib; src = pathlib.Path(en_core_web_sm.__file__).parent / list(pathlib.Path(en_core_web_sm.__file__).parent.glob('en_core_web_sm-*'))[0].name; shutil.copytree(src, 'models/en_core_web_sm/model-best', dirs_exist_ok=True)"

# Windows PowerShell:
# python -c "import en_core_web_sm, shutil, pathlib; src = pathlib.Path(en_core_web_sm.__file__).parent / list(pathlib.Path(en_core_web_sm.__file__).parent.glob('en_core_web_sm-*'))[0].name; shutil.copytree(src, 'models/en_core_web_sm/model-best', dirs_exist_ok=True)"
```

### Option 2: Use Your Own Trained Model

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

2. **Enter Text**:
   - Type or paste text into the input area
   - Or click "Load Sample Text" for a demo

3. **Process Text**:
   - Click "Process Text (NER)" to analyze the text
   - View entities in the results section
   - HTML visualization is automatically saved

4. **View Results**:
   - Click "View Last Output" to open the HTML in your browser
   - Click "Open Output Folder" to see all saved outputs

### Example

Try this sample text:
```
Apple Inc. is an American multinational technology company headquartered 
in Cupertino, California. Tim Cook is the CEO of Apple. The company was 
founded by Steve Jobs, Steve Wozniak, and Ronald Wayne in 1976.
```

The application will:
- Extract entities like "Apple Inc." (ORG), "Tim Cook" (PERSON), "Cupertino" (GPE)
- Show entity labels and positions
- Generate an HTML visualization with highlighted entities
- Save the output to `data/outputs/ner_output_YYYYMMDD_HHMMSS.html`

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

## License

This project is licensed under the MIT License - see the LICENSE file for details.

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
- **TESLA** - Text Embeddings - Serbian Language Applications
- **Language Resources and Technologies Society - Jerteh**

---

**Happy Entity Recognition! 🎯**