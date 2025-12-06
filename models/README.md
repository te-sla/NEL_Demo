# Example Model Setup

This directory contains an example of how to set up a spaCy model for use with the NEL Demo application.

## Quick Start with a Pre-trained Model

The easiest way to get started is to download a pre-trained spaCy model:

### Step 1: Activate Virtual Environment

**Windows:**
```powershell
.\venv\Scripts\Activate.ps1
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### Step 2: Download a Pre-trained Model

```bash
python -m spacy download en_core_web_sm
```

Available models:
- `en_core_web_sm` - Small English model (12 MB)
- `en_core_web_md` - Medium English model (40 MB)
- `en_core_web_lg` - Large English model (560 MB)
- `en_core_web_trf` - Transformer-based model (requires spacy-transformers, 438 MB)

See all available models: https://spacy.io/models

### Step 3: Set Up Model Directory

After downloading, you need to copy the model to the correct location:

**Find the model location:**
```bash
python -c "import en_core_web_sm; import os; print(os.path.dirname(en_core_web_sm.__file__))"
```

**Create the directory structure:**
```bash
mkdir -p models/en_core_web_sm/model-best
```

**Copy the model files:**

**Linux/Mac:**
```bash
cp -r venv/lib/python3.*/site-packages/en_core_web_sm/en_core_web_sm-*/* models/en_core_web_sm/model-best/
```

**Windows (PowerShell):**
```powershell
Copy-Item -Recurse -Path "venv\Lib\site-packages\en_core_web_sm\en_core_web_sm-*\*" -Destination "models\en_core_web_sm\model-best\"
```

### Step 4: Verify the Setup

Your directory structure should look like this:

```
models/
└── en_core_web_sm/
    └── model-best/
        ├── config.cfg
        ├── meta.json
        ├── tokenizer
        ├── vocab/
        ├── ner/
        └── ... (other model files)
```

## Using a Custom Trained Model

If you have trained your own spaCy model:

1. Create a directory for your model:
   ```bash
   mkdir -p models/my_custom_model/model-best
   ```

2. Copy your trained model files to `models/my_custom_model/model-best/`

3. Ensure the directory contains:
   - `config.cfg` - Model configuration
   - `meta.json` - Model metadata
   - Component directories (e.g., `ner/`, `vocab/`, etc.)

## Training Your Own Model

To train a custom NER model with spaCy:

1. **Prepare training data** in spaCy's format (see: https://spacy.io/usage/training#training-data)

2. **Create a config file:**
   ```bash
   python -m spacy init config config.cfg --lang en --pipeline ner
   ```

3. **Train the model:**
   ```bash
   python -m spacy train config.cfg --output ./models/my_model --paths.train ./train.spacy --paths.dev ./dev.spacy
   ```

4. **The trained model** will be in `models/my_model/model-best/`

## Troubleshooting

### "No models found" error
- Make sure the model is in `models/{model_name}/model-best/`
- Check that `config.cfg` and `meta.json` exist in the model-best directory
- Verify the model was copied completely

### Model loading errors
- Ensure the spaCy version matches the model's training version
- Try re-downloading or re-training the model
- Check the model's `meta.json` for compatibility information

## Additional Resources

- [spaCy Models Documentation](https://spacy.io/models)
- [Training spaCy Models](https://spacy.io/usage/training)
- [spaCy 101 Guide](https://spacy.io/usage/spacy-101)
