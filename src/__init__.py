"""NEL Demo - spaCy NER+NEL GUI Application.

This package provides tools for Named Entity Recognition (NER) and
Named Entity Linking (NEL) demonstration using spaCy models.

Modules:
    gui: Main GUI application for NER+NEL demonstration.
    text_chunker: Text chunking utilities for processing large documents.
"""

__version__ = "0.1.0"

from text_chunker import (
    DEFAULT_MAX_CHUNK_SIZE,
    chunk_text,
    merge_html_outputs,
    process_text_in_chunks,
    split_into_paragraphs,
)

__all__ = [
    "DEFAULT_MAX_CHUNK_SIZE",
    "chunk_text",
    "merge_html_outputs",
    "process_text_in_chunks",
    "split_into_paragraphs",
]
