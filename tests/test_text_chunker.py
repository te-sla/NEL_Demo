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
    transliterate_to_latin,
    add_wikidata_links,
    DEFAULT_MAX_CHUNK_SIZE,
    CYRTRANSLIT_AVAILABLE
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
    
    @pytest.mark.skip(reason="Requires actual spaCy model, tested in integration")
    def test_small_text_processing(self):
        """Test processing small text that fits in one chunk."""
        # This test requires an actual spaCy model to work with displaCy
        # It's better tested with integration tests that use real models
        pass
    
    @pytest.mark.skip(reason="Requires actual spaCy model, tested in integration")
    def test_large_text_chunking(self):
        """Test processing large text that requires chunking."""
        # This test requires an actual spaCy model to work with displaCy
        # It's better tested with integration tests that use real models
        pass
    
    @pytest.mark.skipif(not CYRTRANSLIT_AVAILABLE, reason="cyrtranslit not installed")
    def test_transliteration_integration(self):
        """Test that transliterate parameter works in process_text_in_chunks."""
        # This test verifies the integration of transliteration in the chunking workflow
        try:
            import spacy
        except ImportError:
            pytest.skip("spaCy not installed")
        
        # Create a blank Serbian model
        nlp = spacy.blank("sr")
        
        # Cyrillic text
        cyrillic_text = "Београд је главни град Србије."
        
        # Process WITH transliteration
        entities_with, html_with, chunks_with = process_text_in_chunks(
            nlp, 
            cyrillic_text,
            transliterate=True,
            transliterate_lang='sr'
        )
        
        # Process WITHOUT transliteration
        entities_without, html_without, chunks_without = process_text_in_chunks(
            nlp, 
            cyrillic_text,
            transliterate=False
        )
        
        # Both should succeed (blank model won't find entities, but processing should work)
        assert chunks_with == 1
        assert chunks_without == 1
        assert html_with is not None
        assert html_without is not None
        
        # The HTML outputs should be different due to transliteration
        # (one contains Cyrillic, one contains Latin)
        assert html_with != html_without
    
    def test_progress_callback_invoked(self):
        """Test that progress_callback is called correctly for each chunk."""
        try:
            import spacy
        except ImportError:
            pytest.skip("spaCy not installed")
        
        # Create a blank model for testing
        nlp = spacy.blank("en")
        
        # Create text that will be split into multiple chunks
        text = "Test paragraph. " * 1000  # Create text large enough to be chunked
        
        # Track callback invocations
        callback_calls = []
        
        def mock_callback(current, total):
            callback_calls.append((current, total))
        
        # Process with callback
        all_entities, html, num_chunks = process_text_in_chunks(
            nlp,
            text,
            max_chunk_size=1000,  # Force multiple chunks
            progress_callback=mock_callback
        )
        
        # Verify callback was invoked
        assert len(callback_calls) > 0, "Callback should be invoked at least once"
        assert len(callback_calls) == num_chunks, "Callback should be invoked once per chunk"
        
        # Verify callback parameters are correct
        for i, (current, total) in enumerate(callback_calls):
            assert current == i, f"Current should be {i}, got {current}"
            assert total == num_chunks, f"Total should be {num_chunks}, got {total}"
    
    def test_progress_callback_none_works(self):
        """Test that None progress_callback works without errors."""
        try:
            import spacy
        except ImportError:
            pytest.skip("spaCy not installed")
        
        # Create a blank model for testing
        nlp = spacy.blank("en")
        
        # Should work fine with no callback
        all_entities, html, num_chunks = process_text_in_chunks(
            nlp,
            "Test text.",
            progress_callback=None
        )
        
        assert html is not None
        assert num_chunks >= 1


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


class TestTransliteration:
    """Test suite for Cyrillic to Latin transliteration functionality."""
    
    @pytest.mark.skipif(not CYRTRANSLIT_AVAILABLE, reason="cyrtranslit not installed")
    def test_cyrillic_to_latin(self):
        """Test basic Cyrillic to Latin transliteration."""
        cyrillic_text = "Београд"
        result = transliterate_to_latin(cyrillic_text, 'sr')
        assert result == "Beograd"
    
    @pytest.mark.skipif(not CYRTRANSLIT_AVAILABLE, reason="cyrtranslit not installed")
    def test_already_latin_unchanged(self):
        """Test that Latin text remains unchanged."""
        latin_text = "Beograd"
        result = transliterate_to_latin(latin_text, 'sr')
        assert result == "Beograd"
    
    @pytest.mark.skipif(not CYRTRANSLIT_AVAILABLE, reason="cyrtranslit not installed")
    def test_mixed_cyrillic_latin(self):
        """Test mixed Cyrillic and Latin text."""
        mixed_text = "Novak Ђоковић"
        result = transliterate_to_latin(mixed_text, 'sr')
        # Latin part should remain, Cyrillic should be transliterated
        assert "Novak" in result
        assert "Đoković" in result
    
    @pytest.mark.skipif(not CYRTRANSLIT_AVAILABLE, reason="cyrtranslit not installed")
    def test_serbian_sentence(self):
        """Test full Serbian sentence transliteration."""
        cyrillic_text = "Народна банка Србије је централна банка."
        result = transliterate_to_latin(cyrillic_text, 'sr')
        expected = "Narodna banka Srbije je centralna banka."
        assert result == expected
    
    @pytest.mark.skipif(not CYRTRANSLIT_AVAILABLE, reason="cyrtranslit not installed")
    def test_other_language_codes(self):
        """Test transliteration with other supported language codes."""
        # Test Russian
        russian_text = "Москва"
        russian_result = transliterate_to_latin(russian_text, 'ru')
        assert russian_result  # Should not raise an error
        
        # Test Macedonian
        macedonian_text = "Скопје"
        macedonian_result = transliterate_to_latin(macedonian_text, 'mk')
        assert macedonian_result  # Should not raise an error
        
        # Test Bulgarian
        bulgarian_text = "София"
        bulgarian_result = transliterate_to_latin(bulgarian_text, 'bg')
        assert bulgarian_result  # Should not raise an error
    
    @pytest.mark.skipif(not CYRTRANSLIT_AVAILABLE, reason="cyrtranslit not installed")
    def test_special_serbian_characters(self):
        """Test special Serbian Cyrillic characters."""
        # Test characters unique to Serbian Cyrillic
        cyrillic_text = "Ђ, ђ, Ж, ж, Љ, љ, Њ, њ, Ћ, ћ, Џ, џ, Ш, ш, Ч, ч"
        result = transliterate_to_latin(cyrillic_text, 'sr')
        # Check that special characters are properly transliterated
        assert "Đ" in result or "Dj" in result
        assert "ž" in result or "zh" in result
    
    @pytest.mark.skipif(not CYRTRANSLIT_AVAILABLE, reason="cyrtranslit not installed")
    def test_empty_text(self):
        """Test transliteration with empty text."""
        result = transliterate_to_latin("", 'sr')
        assert result == ""
    
    @pytest.mark.skipif(not CYRTRANSLIT_AVAILABLE, reason="cyrtranslit not installed")
    def test_numbers_and_punctuation_unchanged(self):
        """Test that numbers and punctuation remain unchanged."""
        text = "Број 123, датум: 2024."
        result = transliterate_to_latin(text, 'sr')
        # Numbers should be preserved
        assert "123" in result
        assert "2024" in result
    
    @pytest.mark.skipif(not CYRTRANSLIT_AVAILABLE, reason="cyrtranslit not installed")
    def test_unsupported_language_code_raises_error(self):
        """Test that unsupported language codes raise ValueError."""
        with pytest.raises(ValueError, match="Unsupported language code"):
            transliterate_to_latin("test", 'unsupported')
    
    def test_transliterate_without_module_raises_error(self):
        """Test that transliteration raises error when module not available."""
        if CYRTRANSLIT_AVAILABLE:
            pytest.skip("cyrtranslit is installed, can't test error case")
        
        with pytest.raises(ImportError, match="cyrtranslit is required"):
            transliterate_to_latin("test", 'sr')


class TestAddWikidataLinks:
    """Test suite for add_wikidata_links function."""
    
    def test_adds_wikidata_links_for_qids(self):
        """Test that Wikidata links are added for Q-IDs in placeholder links."""
        # Create mock HTML with placeholder links
        html = '''<div class="entities">
<mark class="entity">
    National Bank of Serbia
    <span>ORG
 <a style="text-decoration: none; color: inherit; font-weight: normal" href="#">Q1194664</a>
</span>
</mark>
</div>'''
        
        # Create a mock doc with entities
        try:
            import spacy
            nlp = spacy.blank("en")
            doc = nlp("National Bank of Serbia")
        except ImportError:
            pytest.skip("spaCy not installed")
        
        # Call the function
        result = add_wikidata_links(html, doc)
        
        # Check that the link was replaced
        assert 'href="https://www.wikidata.org/wiki/Q1194664"' in result
        assert 'target="_blank"' in result
        assert 'href="#">Q1194664</a>' not in result
    
    def test_handles_multiple_qids(self):
        """Test handling multiple Q-IDs in the same HTML."""
        html = '''<div class="entities">
<mark class="entity">
    <span>ORG <a href="#">Q1194664</a></span>
</mark>
 is in 
<mark class="entity">
    <span>LOC <a href="#">Q3711</a></span>
</mark>
 in 
<mark class="entity">
    <span>LOC <a href="#">Q403</a></span>
</mark>
</div>'''
        
        try:
            import spacy
            nlp = spacy.blank("en")
            doc = nlp("Test")
        except ImportError:
            pytest.skip("spaCy not installed")
        
        result = add_wikidata_links(html, doc)
        
        # Check all links were replaced
        assert 'href="https://www.wikidata.org/wiki/Q1194664"' in result
        assert 'href="https://www.wikidata.org/wiki/Q3711"' in result
        assert 'href="https://www.wikidata.org/wiki/Q403"' in result
        assert 'href="#">Q' not in result
    
    def test_preserves_nil_entries(self):
        """Test that NIL entries are preserved unchanged."""
        html = '''<div class="entities">
<mark class="entity">
    <span>PER <a href="#">NIL</a></span>
</mark>
</div>'''
        
        try:
            import spacy
            nlp = spacy.blank("en")
            doc = nlp("Test")
        except ImportError:
            pytest.skip("spaCy not installed")
        
        result = add_wikidata_links(html, doc)
        
        # NIL should remain unchanged
        assert '<a href="#">NIL</a>' in result
        assert 'wikidata.org' not in result
    
    def test_empty_entities_returns_unchanged(self):
        """Test that HTML without entities is returned unchanged."""
        html = '<div class="entities">Plain text without entities</div>'
        
        try:
            import spacy
            nlp = spacy.blank("en")
            doc = nlp("Text")
        except ImportError:
            pytest.skip("spaCy not installed")
        
        result = add_wikidata_links(html, doc)
        assert result == html
    
    def test_handles_different_qid_formats(self):
        """Test handling Q-IDs with different number lengths."""
        html = '''<div class="entities">
<a href="#">Q1</a>
<a href="#">Q123</a>
<a href="#">Q123456</a>
<a href="#">Q123456789</a>
</div>'''
        
        try:
            import spacy
            nlp = spacy.blank("en")
            doc = nlp("Test")
        except ImportError:
            pytest.skip("spaCy not installed")
        
        result = add_wikidata_links(html, doc)
        
        # All Q-IDs should be replaced
        assert 'href="https://www.wikidata.org/wiki/Q1"' in result
        assert 'href="https://www.wikidata.org/wiki/Q123"' in result
        assert 'href="https://www.wikidata.org/wiki/Q123456"' in result
        assert 'href="https://www.wikidata.org/wiki/Q123456789"' in result
        assert result.count('target="_blank"') == 4
    
    def test_does_not_affect_other_links(self):
        """Test that other links in the HTML are not affected."""
        html = '''<div class="entities">
<a href="https://example.com">External Link</a>
<a href="#section">Anchor Link</a>
<a href="#">Q1194664</a>
</div>'''
        
        try:
            import spacy
            nlp = spacy.blank("en")
            doc = nlp("Test")
        except ImportError:
            pytest.skip("spaCy not installed")
        
        result = add_wikidata_links(html, doc)
        
        # Other links should remain unchanged
        assert 'href="https://example.com">External Link</a>' in result
        assert 'href="#section">Anchor Link</a>' in result
        # Only Q-ID link should be changed
        assert 'href="https://www.wikidata.org/wiki/Q1194664"' in result
    
    def test_integration_with_displacy_output(self):
        """Test with actual displaCy HTML output structure."""
        try:
            import spacy
            from spacy import displacy
            from spacy.tokens import Span
        except ImportError:
            pytest.skip("spaCy not installed")
        
        # Create a doc with an entity that has a Q-ID
        nlp = spacy.blank("en")
        doc = nlp("The National Bank of Serbia is in Belgrade.")
        
        # Create entities with Q-IDs
        ent1 = Span(doc, 1, 5, label="ORG")  # "National Bank of Serbia"
        ent1.kb_id_ = "Q1194664"
        ent2 = Span(doc, 7, 8, label="LOC")  # "Belgrade"
        ent2.kb_id_ = "Q3711"
        doc.ents = [ent1, ent2]
        
        # Generate HTML
        html = displacy.render(doc, style="ent", page=False)
        
        # Apply the function
        result = add_wikidata_links(html, doc)
        
        # Verify the links are correct
        assert 'href="https://www.wikidata.org/wiki/Q1194664"' in result
        assert 'href="https://www.wikidata.org/wiki/Q3711"' in result
        assert 'target="_blank"' in result
        # Make sure placeholder links are gone
        assert 'href="#">Q1194664</a>' not in result
        assert 'href="#">Q3711</a>' not in result


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
