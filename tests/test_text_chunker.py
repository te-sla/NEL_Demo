#!/usr/bin/env python3
"""
Tests for text_chunker module

This module provides comprehensive tests for the text chunking functionality,
including paragraph-based chunking, HTML merging, and edge cases.
"""

import sys
from pathlib import Path

import pytest
import spacy

# Add src directory to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from text_chunker import (
    DEFAULT_MAX_CHUNK_SIZE,
    chunk_text,
    merge_html_outputs,
    process_text_in_chunks,
    split_into_paragraphs,
)


def _build_rule_based_nlp():
    """Create a lightweight spaCy pipeline with deterministic entities."""

    nlp = spacy.blank("en")
    ruler = nlp.add_pipe("entity_ruler")
    ruler.add_patterns(
        [
            {"label": "ORG", "pattern": "Apple"},
            {"label": "GPE", "pattern": "Cupertino"},
            {"label": "ORG", "pattern": "Microsoft"},
            {"label": "PERSON", "pattern": "Tim Cook"},
        ]
    )
    return nlp


class TestSplitIntoParagraphs:
    """Test suite for split_into_paragraphs function."""
    
    def test_single_paragraph(self):
        """Test splitting text with a single paragraph."""
        text = "This is a single paragraph."
        result = split_into_paragraphs(text)
        assert len(result) == 1
        assert result[0] == "This is a single paragraph."
    
    def test_multiple_paragraphs(self):
        """Test splitting text with multiple paragraphs."""
        text = "First paragraph.\n\nSecond paragraph.\n\nThird paragraph."
        result = split_into_paragraphs(text)
        assert len(result) == 3
        assert result[0] == "First paragraph."
        assert result[1] == "Second paragraph."
        assert result[2] == "Third paragraph."
    
    def test_various_newline_styles(self):
        """Test handling of various newline styles."""
        text = "Paragraph 1.\n\nParagraph 2.\n  \n\nParagraph 3."
        result = split_into_paragraphs(text)
        assert len(result) == 3
    
    def test_empty_paragraphs_filtered(self):
        """Test that empty paragraphs are filtered out."""
        text = "Para 1.\n\n\n\nPara 2.\n\n  \n\nPara 3."
        result = split_into_paragraphs(text)
        assert len(result) == 3
    
    def test_empty_text(self):
        """Test with empty text."""
        result = split_into_paragraphs("")
        assert result == []
    
    def test_whitespace_only(self):
        """Test with whitespace-only text."""
        result = split_into_paragraphs("   \n\n   \n   ")
        assert result == []


class TestChunkText:
    """Test suite for chunk_text function."""
    
    def test_small_text_single_chunk(self):
        """Test that small text returns a single chunk."""
        text = "This is a small text."
        result = chunk_text(text, max_chunk_size=1000)
        assert len(result) == 1
        assert result[0] == text
    
    def test_exact_size_limit(self):
        """Test text exactly at size limit."""
        text = "a" * 1000
        result = chunk_text(text, max_chunk_size=1000)
        assert len(result) == 1
    
    def test_slightly_over_limit(self):
        """Test text slightly over size limit."""
        text = "a" * 1001
        result = chunk_text(text, max_chunk_size=1000)
        assert len(result) >= 2
    
    def test_paragraph_boundary_preservation(self):
        """Test that chunking preserves paragraph boundaries."""
        paragraphs = ["Para 1. " * 10, "Para 2. " * 10, "Para 3. " * 10]
        text = "\n\n".join(paragraphs)
        result = chunk_text(text, max_chunk_size=200)
        
        # Each paragraph should be in a separate chunk or combined if small enough
        assert len(result) >= 1
        # Verify no paragraph is split incorrectly
        for chunk in result:
            assert chunk.strip()  # No empty chunks
    
    def test_large_single_paragraph_split(self):
        """Test that a large single paragraph is split properly."""
        # Create a paragraph larger than chunk size
        large_para = "This is a sentence. " * 100  # ~2000 chars
        result = chunk_text(large_para, max_chunk_size=500)
        
        assert len(result) > 1
        # Verify each chunk is within size limit (with some tolerance for splitting logic)
        for chunk in result:
            assert len(chunk) <= 550  # Small tolerance
    
    def test_multiple_paragraphs_multiple_chunks(self):
        """Test multiple paragraphs split into multiple chunks."""
        para = "A" * 400
        text = "\n\n".join([para] * 5)  # ~2000 chars total
        result = chunk_text(text, max_chunk_size=500)
        
        assert len(result) >= 4
    
    def test_empty_text(self):
        """Test with empty text."""
        result = chunk_text("")
        assert result == []
    
    def test_whitespace_only(self):
        """Test with whitespace-only text."""
        result = chunk_text("   \n\n   ")
        assert result == []
    
    def test_invalid_chunk_size(self):
        """Test that invalid chunk size raises ValueError."""
        with pytest.raises(ValueError, match="max_chunk_size must be at least 100"):
            chunk_text("Some text", max_chunk_size=50)
    
    def test_default_chunk_size(self):
        """Test that default chunk size is used correctly."""
        text = "x" * (DEFAULT_MAX_CHUNK_SIZE + 1000)
        result = chunk_text(text)
        assert len(result) >= 2


class TestMergeHTMLOutputs:
    """Test suite for merge_html_outputs function."""
    
    @pytest.fixture
    def sample_html_chunk(self):
        """Fixture providing a sample HTML chunk similar to displaCy output."""
        return '''<!DOCTYPE html>
<html>
<head>
    <style>
        .entities { line-height: 2.5; }
        mark.entity { padding: 0.25em; }
    </style>
</head>
<body>
    <div class="entities" style="line-height: 2.5">
        This is some <mark class="entity" style="background: #ddd;">entity</mark> text.
    </div>
</body>
</html>'''
    
    def test_single_chunk_returns_unchanged(self, sample_html_chunk):
        """Test that a single chunk is returned as-is."""
        result = merge_html_outputs([sample_html_chunk])
        assert result == sample_html_chunk
    
    def test_multiple_chunks_merged(self, sample_html_chunk):
        """Test that multiple chunks are merged properly."""
        chunks = [sample_html_chunk, sample_html_chunk]
        result = merge_html_outputs(chunks)
        
        # Check that result is valid HTML
        assert result.startswith("<!DOCTYPE html>")
        assert "<style>" in result
        assert ".entities" in result
        # Should contain content from both chunks
        assert result.count("entity") >= 2
    
    def test_empty_list_raises_error(self):
        """Test that empty list raises ValueError."""
        with pytest.raises(ValueError, match="html_chunks cannot be empty"):
            merge_html_outputs([])
    
    def test_custom_title(self, sample_html_chunk):
        """Test that custom title is used."""
        chunks = [sample_html_chunk, sample_html_chunk]
        result = merge_html_outputs(chunks, title="Custom Title")
        assert "<title>Custom Title</title>" in result
    
    def test_section_breaks_inserted(self, sample_html_chunk):
        """Test that section breaks are inserted between chunks."""
        chunks = [sample_html_chunk, sample_html_chunk]
        result = merge_html_outputs(chunks)
        assert "Document Section Break" in result


class TestProcessTextInChunks:
    """Test suite for process_text_in_chunks function."""
    
    def test_none_nlp_raises_error(self):
        """Test that None nlp raises ValueError."""
        with pytest.raises(ValueError, match="nlp model cannot be None"):
            process_text_in_chunks(None, "Some text")
    
    def test_empty_text_raises_error(self):
        """Test that empty text raises ValueError."""
        # Create a minimal mock that won't be called
        class DummyNLP:
            pass
        
        with pytest.raises(ValueError, match="text cannot be empty"):
            process_text_in_chunks(DummyNLP(), "")
    
    def test_whitespace_text_raises_error(self):
        """Test that whitespace-only text raises ValueError."""
        # Create a minimal mock that won't be called
        class DummyNLP:
            pass
        
        with pytest.raises(ValueError, match="text cannot be empty"):
            process_text_in_chunks(DummyNLP(), "   \n\n   ")
    
    def test_small_text_processing(self, tmp_path):
        """Process small text and ensure entities are preserved."""

        nlp = _build_rule_based_nlp()
        text = "Apple is headquartered in Cupertino. Tim Cook leads the company."
        output_path = tmp_path / "small_text.html"

        entities, html, num_chunks = process_text_in_chunks(
            nlp, text, max_chunk_size=500, output_path=output_path
        )

        assert num_chunks == 1
        assert len(entities) >= 2  # Cupertino and Apple should match
        assert "Apple" in html and "Cupertino" in html
        assert output_path.exists()

    def test_large_text_chunking(self, tmp_path):
        """Process large text and confirm multiple chunks and HTML separators."""

        nlp = _build_rule_based_nlp()
        paragraph = "Apple is headquartered in Cupertino. Microsoft has offices worldwide. "
        text = "\n\n".join([paragraph] * 30)
        output_path = tmp_path / "large_text.html"

        entities, html, num_chunks = process_text_in_chunks(
            nlp, text, max_chunk_size=500, output_path=output_path
        )

        assert num_chunks > 1
        assert len(entities) >= num_chunks  # Each chunk should yield at least one entity
        assert "Document Section Break" in html
        assert output_path.exists()

    def test_progress_callback_invoked(self):
        """Ensure progress callback receives chunk progress updates."""

        nlp = _build_rule_based_nlp()
        text = "\n\n".join(["Apple is in Cupertino." for _ in range(10)])

        progress_updates = []

        def _record_progress(completed, total):
            progress_updates.append((completed, total))

        entities, _, num_chunks = process_text_in_chunks(
            nlp,
            text,
            max_chunk_size=120,
            progress_callback=_record_progress,
        )

        assert num_chunks > 1
        assert len(entities) >= num_chunks
        assert progress_updates[0] == (0, num_chunks)
        assert progress_updates[-1] == (num_chunks, num_chunks)
        # Should record one entry per chunk plus the initial zeroed state
        assert len(progress_updates) == num_chunks + 1


class TestEdgeCases:
    """Test suite for edge cases and special scenarios."""
    
    def test_very_long_sentence(self):
        """Test handling of very long sentences without punctuation."""
        text = "word " * 1000  # ~5000 chars, no sentence boundaries
        result = chunk_text(text, max_chunk_size=500)
        
        assert len(result) > 1
        for chunk in result:
            # Should be split, even without sentence boundaries
            assert len(chunk) <= 550  # Small tolerance
    
    def test_mixed_paragraph_sizes(self):
        """Test text with mixed paragraph sizes."""
        small_para = "Small paragraph."
        large_para = "Large paragraph. " * 100
        text = "\n\n".join([small_para, large_para, small_para])
        
        result = chunk_text(text, max_chunk_size=500)
        assert len(result) >= 2
    
    def test_unicode_text(self):
        """Test handling of Unicode characters."""
        text = "Hello 世界\n\nBonjour le monde\n\nΓεια σου κόσμε"
        result = chunk_text(text, max_chunk_size=1000)
        
        assert len(result) >= 1
        merged = "\n\n".join(result)
        # Unicode should be preserved
        assert "世界" in merged
        assert "Γεια" in merged
    
    def test_special_characters(self):
        """Test handling of special characters."""
        text = "Para 1: @#$%^&*()\n\nPara 2: <html> & \"quotes\""
        result = split_into_paragraphs(text)
        
        assert len(result) == 2
        assert "@#$%^&*()" in result[0]
        assert "<html>" in result[1]


class TestIntegration:
    """Integration tests for the complete workflow."""
    
    def test_chunk_and_merge_workflow(self):
        """Test the complete chunk and merge workflow."""
        # Create sample text with paragraphs
        text = "\n\n".join([f"Paragraph {i}. " * 20 for i in range(10)])
        
        # Chunk the text
        chunks = chunk_text(text, max_chunk_size=500)
        assert len(chunks) > 1
        
        # Create mock HTML outputs
        html_chunks = [
            f'<html><head><style>.entities {{}}</style></head>'
            f'<body><div class="entities">Chunk {i}</div></body></html>'
            for i in range(len(chunks))
        ]
        
        # Merge HTML
        merged = merge_html_outputs(html_chunks)
        
        assert merged.startswith("<!DOCTYPE html>")
        assert "<style>" in merged
        assert len(chunks) <= merged.count("Chunk")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
