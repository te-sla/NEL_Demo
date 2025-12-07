#!/usr/bin/env python3
"""
Tests for text_chunker module

This module provides comprehensive tests for the text chunking functionality,
including paragraph-based chunking, HTML merging, and edge cases.
"""

import pytest
import sys
from pathlib import Path

# Add src directory to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from text_chunker import (
    split_into_paragraphs,
    chunk_text,
    merge_html_outputs,
    process_text_in_chunks,
    DEFAULT_MAX_CHUNK_SIZE
)


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
    
    def test_malformed_html_warning(self, sample_html_chunk):
        """Test that warning is raised for malformed HTML chunks."""
        # Create HTML that doesn't match expected pattern
        # The pattern looks for <div class="entities"...>
        malformed_html = '''<!DOCTYPE html>
<html>
<head>
    <style>
        .entities { line-height: 2.5; }
    </style>
</head>
<body>
    <div class="wrongclass">No entities div here</div>
</body>
</html>'''
        # Use multiple chunks so we don't return early
        chunks = [sample_html_chunk, malformed_html]
        
        # Should raise a warning for malformed chunk
        import warnings
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = merge_html_outputs(chunks)
            
            # Check that a warning was raised
            assert len(w) >= 1
            # Verify the warning message
            warning_found = any("doesn't match expected HTML pattern" in str(warning.message) for warning in w)
            assert warning_found, f"Expected warning not found. Warnings: {[str(warning.message) for warning in w]}"
    
    def test_mixed_valid_and_malformed_html(self, sample_html_chunk):
        """Test merging with mix of valid and malformed HTML."""
        malformed_html = '<html><body>No entities div here</body></html>'
        chunks = [sample_html_chunk, malformed_html]
        
        import warnings
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = merge_html_outputs(chunks)
            
            # Should still produce output
            assert result.startswith("<!DOCTYPE html>")
            # Should have warned about malformed chunk
            assert len(w) > 0


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
    
    def test_displacy_import_error(self):
        """Test that ImportError is raised when displacy is not available."""
        # Mock the DISPLACY_AVAILABLE flag
        import text_chunker
        original_value = text_chunker.DISPLACY_AVAILABLE
        
        try:
            # Temporarily set DISPLACY_AVAILABLE to False
            text_chunker.DISPLACY_AVAILABLE = False
            
            class DummyNLP:
                pass
            
            with pytest.raises(ImportError, match="spacy.displacy is required"):
                process_text_in_chunks(DummyNLP(), "Some text")
        finally:
            # Restore original value
            text_chunker.DISPLACY_AVAILABLE = original_value
    
    def test_with_mock_spacy_model(self):
        """Test processing with a mock spaCy model using real spacy blank model."""
        try:
            import spacy
            # Use a real blank model instead of mocking
            nlp = spacy.blank("en")
            
            text = "This is a test text with some content."
            
            # This should work with the blank model
            entities, html, num_chunks = process_text_in_chunks(nlp, text)
            
            # Blank model won't find entities, but should still process
            assert isinstance(entities, list)
            assert num_chunks == 1
            assert isinstance(html, str)
            assert len(html) > 0
            # Verify HTML structure
            assert "<!DOCTYPE html>" in html
        except ImportError:
            pytest.skip("spacy not available")
    
    def test_with_multiple_chunks_mock(self):
        """Test processing text that needs chunking with blank model."""
        try:
            import spacy
            nlp = spacy.blank("en")
            
            # Create a large text that will be chunked
            text = "\n\n".join(["Paragraph " * 100 for _ in range(20)])
            
            # This should work with the blank model
            entities, html, num_chunks = process_text_in_chunks(nlp, text, max_chunk_size=1000)
            
            assert isinstance(entities, list)
            assert num_chunks > 1
            assert isinstance(html, str)
            assert len(html) > 0
            # Verify section breaks are present
            assert "Document Section Break" in html
        except ImportError:
            pytest.skip("spacy not available")
    
    def test_output_file_generation(self):
        """Test that output file is generated correctly."""
        try:
            import spacy
            import tempfile
            
            nlp = spacy.blank("en")
            text = "This is a test."
            
            with tempfile.TemporaryDirectory() as tmpdir:
                output_path = Path(tmpdir) / "test_output.html"
                
                entities, html, num_chunks = process_text_in_chunks(
                    nlp, text, output_path=output_path
                )
                
                # Verify file was created
                assert output_path.exists()
                
                # Verify file content
                with open(output_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    assert len(content) > 0
                    assert content == html
        except ImportError:
            pytest.skip("spacy not available")


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
