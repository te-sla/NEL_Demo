#!/usr/bin/env python3
"""
Configuration module for NEL Demo application.

This module centralizes all configuration constants and settings used
throughout the application.
"""

from pathlib import Path

# Version information
VERSION = "1.0.0"
APP_NAME = "NEL Demo - spaCy NER+NEL GUI"

# Attribution
TESLA_URL = "https://tesla.rgf.bg.ac.rs/"
JERTEH_URL = "https://jerteh.rs/"

# Project paths (relative to this file)
PROJECT_ROOT = Path(__file__).parent.parent
MODELS_DIR = PROJECT_ROOT / "models"
INPUTS_DIR = PROJECT_ROOT / "inputs"
DATA_DIR = PROJECT_ROOT / "data"
OUTPUTS_DIR = DATA_DIR / "outputs"

# File loading limits
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB limit for file loading

# Text chunking settings
DEFAULT_MAX_CHUNK_SIZE = 100000  # 100K characters per chunk

# Supported transliteration language codes
SUPPORTED_TRANSLITERATION_CODES = {'sr', 'me', 'mk', 'ru', 'uk', 'kk', 'bg'}

# Sample text file
SAMPLE_TEXT_FILE = INPUTS_DIR / "sample_text.txt"

# GUI Settings
GUI_TITLE = APP_NAME
GUI_WINDOW_SIZE = "1000x700"
GUI_MIN_WIDTH = 800
GUI_MIN_HEIGHT = 600
