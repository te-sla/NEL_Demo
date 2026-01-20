#!/usr/bin/env python3
"""
PyInstaller runtime hook for spaCy optimization.
This hook optimizes spaCy loading in the bundled executable.
"""

from PyInstaller.utils.hooks import collect_all

# Collect all spaCy data
datas, binaries, hiddenimports = collect_all('spacy')

# Collect specific spaCy language data
hiddenimports += [
    'spacy.lang.sr',
    'spacy.lang.en',
    'spacy.lang.xx',
    'thinc.backends',
    'thinc.backends.numpy_ops',
    'thinc.api',
    'cymem.cymem',
    'preshed.maps',
    'murmurhash.mrmr',
    'blis',
    'catalogue',
    'confection',
    'pydantic',
    'srsly',
    'wasabi',
    'typer',
]

# Exclude unnecessary spaCy components to reduce size
excludedimports = [
    'spacy.cli.download',
    'spacy.cli.init',
    'spacy.cli.project',
    'spacy.cli.train',
    'spacy.tests',
]
