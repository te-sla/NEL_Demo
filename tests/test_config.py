#!/usr/bin/env python3
"""
Tests for the config module.

This test verifies that all expected configuration constants are defined
and have the correct types.
"""

import pytest
from pathlib import Path


def test_config_constants_defined():
    """Test that all required configuration constants are defined."""
    from src.config import (
        VERSION,
        APP_NAME,
        TESLA_URL,
        JERTEH_URL,
        PROJECT_ROOT,
        MODELS_DIR,
        INPUTS_DIR,
        DATA_DIR,
        OUTPUTS_DIR,
        MAX_FILE_SIZE,
        DEFAULT_MAX_CHUNK_SIZE,
        SUPPORTED_TRANSLITERATION_CODES,
    )
    
    # Test string constants
    assert isinstance(VERSION, str)
    assert len(VERSION) > 0
    assert isinstance(APP_NAME, str)
    assert len(APP_NAME) > 0
    
    # Test URLs
    assert isinstance(TESLA_URL, str)
    assert TESLA_URL.startswith("http")
    assert isinstance(JERTEH_URL, str)
    assert JERTEH_URL.startswith("http")
    
    # Test paths
    assert isinstance(PROJECT_ROOT, Path)
    assert isinstance(MODELS_DIR, Path)
    assert isinstance(INPUTS_DIR, Path)
    assert isinstance(DATA_DIR, Path)
    assert isinstance(OUTPUTS_DIR, Path)
    
    # Test numeric constants
    assert isinstance(MAX_FILE_SIZE, int)
    assert MAX_FILE_SIZE > 0
    assert isinstance(DEFAULT_MAX_CHUNK_SIZE, int)
    assert DEFAULT_MAX_CHUNK_SIZE > 0
    
    # Test transliteration codes
    assert isinstance(SUPPORTED_TRANSLITERATION_CODES, set)
    assert len(SUPPORTED_TRANSLITERATION_CODES) > 0
    assert all(isinstance(code, str) for code in SUPPORTED_TRANSLITERATION_CODES)


def test_config_version_format():
    """Test that VERSION follows semantic versioning."""
    from src.config import VERSION
    
    parts = VERSION.split('.')
    assert len(parts) == 3, "VERSION should follow semantic versioning (major.minor.patch)"
    assert all(part.isdigit() for part in parts), "VERSION parts should be numeric"


def test_config_paths_relative_to_project_root():
    """Test that all directory paths are relative to PROJECT_ROOT."""
    from src.config import PROJECT_ROOT, MODELS_DIR, INPUTS_DIR, DATA_DIR
    
    # Check that paths are under PROJECT_ROOT
    assert str(MODELS_DIR).startswith(str(PROJECT_ROOT))
    assert str(INPUTS_DIR).startswith(str(PROJECT_ROOT))
    assert str(DATA_DIR).startswith(str(PROJECT_ROOT))
