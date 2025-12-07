#!/usr/bin/env python3
"""
Integration tests for the complete NEL Demo workflow

This module provides end-to-end integration tests that verify the complete
functionality of the application, from text input to HTML output generation.
"""

import pytest
import sys
from pathlib import Path
import tempfile

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


class TestEndToEndWorkflow:
    """End-to-end integration tests."""
    
    def test_complete_chunking_workflow(self):
        """Test the complete workflow from text to merged HTML."""
        # Create a realistic multi-paragraph text
        paragraphs = [
            "The first paragraph contains information about entities. It has multiple sentences. "
            "Each sentence contributes to the overall meaning.",
            
            "The second paragraph discusses different topics. It introduces new concepts. "
            "The content is varied and interesting.",
            
            "The third paragraph wraps up the discussion. It provides conclusions. "
            "The final thoughts are presented here."
        ]
        
        text = "\n\n".join(paragraphs)
        
        # Step 1: Split into paragraphs
        split_paras = split_into_paragraphs(text)
        assert len(split_paras) == 3
        
        # Step 2: Chunk the text (using small chunk size to force chunking)
        chunks = chunk_text(text, max_chunk_size=200)
        assert len(chunks) >= 1
        
        # Step 3: Verify chunks maintain content
        merged_chunks = "\n\n".join(chunks)
        # Content should be preserved (allowing for whitespace normalization)
        for para in paragraphs:
            assert para.strip() in merged_chunks or any(word in merged_chunks for word in para.split())
    
    def test_large_document_processing(self):
        """Test processing of a large document that requires chunking."""
        # Create a large document
        base_paragraph = "This is a test paragraph. " * 100  # ~2400 chars
        paragraphs = [f"{base_paragraph} Section {i}." for i in range(50)]
        text = "\n\n".join(paragraphs)
        
        # Chunk the text
        chunks = chunk_text(text, max_chunk_size=5000)
        
        # Verify chunking occurred
        assert len(chunks) > 1
        
        # Verify all chunks are within size limit (with tolerance)
        for chunk in chunks:
            assert len(chunk) <= 5500  # 10% tolerance
        
        # Verify content preservation
        total_chars = sum(len(chunk) for chunk in chunks)
        # Should be close to original length (allowing for separator differences)
        assert total_chars >= len(text) * 0.9
    
    def test_html_generation_workflow(self):
        """Test HTML generation and merging workflow."""
        # Create sample HTML chunks similar to displaCy output
        html_template = '''<!DOCTYPE html>
<html>
<head>
    <style>
        .entities {{ line-height: 2.5; }}
        mark.entity {{ background: #ddd; padding: 0.25em; }}
    </style>
</head>
<body>
    <div class="entities" style="line-height: 2.5">
        Chunk {num}: This is <mark class="entity" style="background: #ddd;">Entity {num}</mark> text.
    </div>
</body>
</html>'''
        
        # Create multiple chunks
        html_chunks = [html_template.format(num=i) for i in range(1, 4)]
        
        # Merge HTML
        merged = merge_html_outputs(html_chunks, title="Test Document")
        
        # Verify merged HTML structure
        assert merged.startswith("<!DOCTYPE html>")
        assert "<title>Test Document</title>" in merged
        assert ".entities" in merged
        
        # Verify all chunks are included
        for i in range(1, 4):
            assert f"Entity {i}" in merged
        
        # Verify section breaks
        assert "Document Section Break" in merged
    
    def test_spacy_integration_with_blank_model(self):
        """Test integration with spaCy using a blank model."""
        try:
            import spacy
            
            # Create a blank model
            nlp = spacy.blank("en")
            
            # Create test text
            text = "This is a test document.\n\nIt has multiple paragraphs.\n\nEach paragraph contains text."
            
            # Process with chunking
            with tempfile.TemporaryDirectory() as tmpdir:
                output_path = Path(tmpdir) / "test_output.html"
                
                entities, html, num_chunks = process_text_in_chunks(
                    nlp, text, output_path=output_path
                )
                
                # Verify results
                assert isinstance(entities, list)
                assert isinstance(html, str)
                assert num_chunks >= 1
                
                # Verify output file
                assert output_path.exists()
                
                with open(output_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    assert content == html
                    assert "<!DOCTYPE html>" in content
                    
        except ImportError:
            pytest.skip("spacy not available")
    
    def test_unicode_document_processing(self):
        """Test processing documents with Unicode characters."""
        # Create text with various Unicode characters
        text = """Hello World!

Bonjour le monde! Les accents français: é è ê ë.

Привет мир! Кириллица здесь.

你好世界！中文在这里。

مرحبا بالعالم! العربية هنا.

Γεια σου κόσμε! Ελληνικά εδώ."""
        
        # Split into paragraphs
        paragraphs = split_into_paragraphs(text)
        assert len(paragraphs) == 6
        
        # Verify Unicode preservation
        assert "français" in paragraphs[1]
        assert "Кириллица" in paragraphs[2]
        assert "中文" in paragraphs[3]
        assert "العربية" in paragraphs[4]
        assert "Ελληνικά" in paragraphs[5]
        
        # Chunk and verify Unicode preservation
        chunks = chunk_text(text, max_chunk_size=500)
        merged = "\n\n".join(chunks)
        
        # All Unicode should be preserved
        assert "français" in merged
        assert "Кириллица" in merged
        assert "中文" in merged


class TestErrorRecovery:
    """Test error handling and recovery scenarios."""
    
    def test_recovery_from_malformed_chunks(self):
        """Test that processing continues even with malformed HTML chunks."""
        valid_html = '''<!DOCTYPE html>
<html>
<head>
    <style>.entities { line-height: 2.5; }</style>
</head>
<body>
    <div class="entities" style="line-height: 2.5">
        Valid content here.
    </div>
</body>
</html>'''
        
        malformed_html = '<html><body>Malformed without entities div</body></html>'
        
        # Mix valid and malformed chunks
        chunks = [valid_html, malformed_html, valid_html]
        
        import warnings
        with warnings.catch_warnings(record=True):
            result = merge_html_outputs(chunks)
            
            # Should still produce output
            assert result.startswith("<!DOCTYPE html>")
            # Valid content should be included
            assert "Valid content here" in result
    
    def test_empty_paragraph_handling(self):
        """Test handling of text with many empty paragraphs."""
        text = "Para 1\n\n\n\n\n\n\nPara 2\n\n\n\nPara 3"
        
        paragraphs = split_into_paragraphs(text)
        
        # Should filter out empty paragraphs
        assert len(paragraphs) == 3
        assert all(p.strip() for p in paragraphs)
    
    def test_very_large_single_paragraph(self):
        """Test handling of a single paragraph that exceeds chunk size."""
        # Create a huge paragraph with no natural break points
        huge_paragraph = "word" * 50000  # 200K characters
        
        chunks = chunk_text(huge_paragraph, max_chunk_size=10000)
        
        # Should be split despite being single paragraph
        assert len(chunks) > 1
        
        # All chunks should be within or close to size limit
        for chunk in chunks:
            assert len(chunk) <= 11000  # 10% tolerance


class TestPerformanceScenarios:
    """Test performance-related scenarios."""
    
    def test_optimal_chunk_sizes(self):
        """Test that chunk sizes are optimized for typical use cases."""
        # Create text at various sizes
        small_text = "Small text. " * 100  # ~1200 chars
        medium_text = "Medium text. " * 1000  # ~12K chars
        large_text = "Large text. " * 10000  # ~120K chars
        
        # Small text should not be chunked
        small_chunks = chunk_text(small_text, max_chunk_size=DEFAULT_MAX_CHUNK_SIZE)
        assert len(small_chunks) == 1
        
        # Medium text should not be chunked with default size
        medium_chunks = chunk_text(medium_text, max_chunk_size=DEFAULT_MAX_CHUNK_SIZE)
        assert len(medium_chunks) == 1
        
        # Large text should be chunked
        large_chunks = chunk_text(large_text, max_chunk_size=DEFAULT_MAX_CHUNK_SIZE)
        assert len(large_chunks) >= 2
    
    def test_paragraph_boundary_preservation(self):
        """Test that paragraph boundaries are preserved when possible."""
        # Create text with clear paragraph boundaries
        paragraphs = [f"Paragraph {i}. " * 50 for i in range(10)]
        text = "\n\n".join(paragraphs)
        
        # Chunk with size that should keep some paragraphs together
        chunks = chunk_text(text, max_chunk_size=1000)
        
        # Verify chunks maintain paragraph structure
        for chunk in chunks:
            # Each chunk should contain complete paragraphs when possible
            # Check for paragraph markers
            if "\n\n" in chunk:
                parts = chunk.split("\n\n")
                # Each part should be a complete paragraph (not cut mid-sentence)
                for part in parts:
                    if part.strip():
                        # Should end with proper punctuation
                        assert part.strip()[-1] in '.!?'


class TestBoundaryConditions:
    """Test boundary conditions and edge cases."""
    
    def test_minimum_chunk_size(self):
        """Test with minimum allowed chunk size."""
        text = "This is a test. " * 20
        
        # Test minimum size (100)
        chunks = chunk_text(text, max_chunk_size=100)
        assert len(chunks) >= 1
        
        # Test below minimum should raise error
        with pytest.raises(ValueError, match="max_chunk_size must be at least 100"):
            chunk_text(text, max_chunk_size=50)
    
    def test_exact_boundary_sizes(self):
        """Test text that is exactly at chunk boundaries."""
        # Create text exactly 1000 characters
        text = "a" * 1000
        
        chunks = chunk_text(text, max_chunk_size=1000)
        assert len(chunks) == 1
        assert len(chunks[0]) == 1000
        
        # Create text exactly 1001 characters
        text = "a" * 1001
        
        chunks = chunk_text(text, max_chunk_size=1000)
        assert len(chunks) >= 2
    
    def test_single_character_text(self):
        """Test with single character."""
        text = "a"
        
        chunks = chunk_text(text, max_chunk_size=1000)
        assert len(chunks) == 1
        assert chunks[0] == "a"
    
    def test_text_with_only_whitespace_paragraphs(self):
        """Test text with paragraphs containing only whitespace."""
        text = "Para 1\n\n   \t   \n\nPara 2"
        
        paragraphs = split_into_paragraphs(text)
        
        # Whitespace-only paragraphs should be filtered
        assert len(paragraphs) == 2
        assert "Para 1" in paragraphs[0]
        assert "Para 2" in paragraphs[1]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
