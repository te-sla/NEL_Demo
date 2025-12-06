#!/usr/bin/env python3
"""
Integration test demonstrating the complete text chunking workflow.

This script shows how to use the text chunking functionality in a real-world scenario.
It requires a trained spaCy model to be available.
"""

import sys
from pathlib import Path

import pytest

# Add src directory to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from text_chunker import DEFAULT_MAX_CHUNK_SIZE, chunk_text, process_text_in_chunks


def create_large_sample_text(repetitions: int = 30) -> str:
    """Create a large sample text for testing that still runs quickly."""

    base_text = """
Apple Inc. is an American multinational technology company headquartered in Cupertino, California.
Tim Cook is the CEO of Apple. The company was founded by Steve Jobs, Steve Wozniak, and Ronald Wayne in 1976.
Apple is known for products like the iPhone, iPad, and Mac computers.

Microsoft Corporation, founded by Bill Gates and Paul Allen in 1975, is headquartered in Redmond, Washington.
Satya Nadella currently serves as the CEO. Microsoft is famous for Windows, Office, and Azure cloud services.
"""

    large_text = "\n\n".join([base_text.strip() for _ in range(repetitions)])
    return large_text


def test_with_rule_based_model(rule_based_nlp, tmp_path):
    """Test using a rule-based spaCy pipeline to avoid external model downloads."""

    nlp = rule_based_nlp
    text = create_large_sample_text()
    chunk_size = 5000

    chunks = chunk_text(text, max_chunk_size=chunk_size)
    assert len(chunks) > 1

    output_file = tmp_path / "integration_test_output.html"
    entities, html, num_chunks = process_text_in_chunks(
        nlp, text, max_chunk_size=chunk_size, output_path=output_file
    )

    assert num_chunks == len(chunks)
    assert len(entities) >= num_chunks
    assert output_file.exists()
    assert "Document Section Break" in html


def test_small_text(rule_based_nlp, tmp_path):
    """Test with small text that doesn't need chunking."""

    nlp = rule_based_nlp
    text = """Apple Inc. is headquartered in Cupertino, California.
Tim Cook is the CEO."""

    output_file = tmp_path / "small_text_output.html"
    entities, html, num_chunks = process_text_in_chunks(
        nlp, text, output_path=output_file
    )

    assert num_chunks == 1
    assert len(entities) >= 2
    assert "Apple" in html and "Cupertino" in html
    assert output_file.exists()


def main():
    """Allow running the integration tests directly."""

    return pytest.main([__file__])


if __name__ == "__main__":
    sys.exit(main())
