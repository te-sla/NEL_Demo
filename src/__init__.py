"""
NEL Demo - spaCy NER+NEL GUI Application

This package provides a simple GUI application for Named Entity Recognition (NER)
and Named Entity Linking (NEL) using spaCy models.
"""

from .config import VERSION as __version__
from .config import APP_NAME, TESLA_URL, JERTEH_URL

__author__ = "TESLA & Jerteh"

# Re-export VERSION for backward compatibility
VERSION = __version__

from .text_chunker import (
    process_text_in_chunks,
    split_into_paragraphs,
    transliterate_to_latin,
    CYRTRANSLIT_AVAILABLE,
    DEFAULT_MAX_CHUNK_SIZE,
)

__all__ = [
    "process_text_in_chunks",
    "split_into_paragraphs",
    "transliterate_to_latin",
    "CYRTRANSLIT_AVAILABLE",
    "DEFAULT_MAX_CHUNK_SIZE",
    "VERSION",
    "APP_NAME",
    "TESLA_URL",
    "JERTEH_URL",
]
