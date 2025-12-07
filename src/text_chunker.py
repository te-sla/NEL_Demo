#!/usr/bin/env python3
"""
Text Chunking Module for spaCy NER Processing

This module provides functionality to chunk large text documents into smaller
segments to prevent exceeding spaCy's document length limits. It preserves
text structure by chunking on paragraph boundaries when possible, and merges
the resulting HTML visualizations into a single output.

spaCy has practical limits on document length (typically around 1,000,000 characters)
for efficient processing. This module helps handle larger documents by:
1. Splitting text into manageable chunks
2. Processing each chunk separately
3. Merging the HTML outputs into a cohesive visualization

Additionally, this module provides Cyrillic to Latin transliteration for texts
primarily written in Cyrillic script, which is useful when the NER model was
trained on Latin script.
"""

from typing import List, Optional, Tuple, Callable
import re
import warnings
from pathlib import Path

# Try to import config module for constants
try:
    from .config import DEFAULT_MAX_CHUNK_SIZE, SUPPORTED_TRANSLITERATION_CODES
except ImportError:
    # Fallback defaults if config not available
    DEFAULT_MAX_CHUNK_SIZE = 100000  # 100K characters per chunk
    SUPPORTED_TRANSLITERATION_CODES = {'sr', 'me', 'mk', 'ru', 'uk', 'kk', 'bg'}

# Try to import spacy's displacy for HTML rendering
# This is optional and only needed for process_text_in_chunks function
try:
    from spacy import displacy
    DISPLACY_AVAILABLE = True
except ImportError:
    DISPLACY_AVAILABLE = False
    displacy = None

# Try to import cyrtranslit for Cyrillic-to-Latin transliteration
try:
    import cyrtranslit
    CYRTRANSLIT_AVAILABLE = True
except ImportError:
    CYRTRANSLIT_AVAILABLE = False
    cyrtranslit = None


def transliterate_to_latin(text: str, lang_code: str = 'sr') -> str:
    """
    Transliterate Cyrillic text to Latin script.
    
    This function uses the cyrtranslit library to convert Cyrillic characters
    to their Latin equivalents. This is useful when the NER model was trained
    on Latin script but the input text is in Cyrillic.
    
    Args:
        text: The input text (may contain Cyrillic, Latin, or mixed)
        lang_code: Language code for transliteration (default: 'sr' for Serbian)
                   Supported codes: 'sr' (Serbian), 'me' (Montenegrin), 'mk' (Macedonian), 
                   'ru' (Russian), 'uk' (Ukrainian), 'kk' (Kazakh), 'bg' (Bulgarian)
        
    Returns:
        Text with Cyrillic characters converted to Latin
        
    Raises:
        ImportError: If cyrtranslit is not installed
        ValueError: If an unsupported language code is provided
        
    Note:
        - If cyrtranslit is not available, this function will raise ImportError
        - Text already in Latin script will be preserved
        - Mixed Cyrillic/Latin text is supported
    """
    if not CYRTRANSLIT_AVAILABLE:
        raise ImportError(
            "cyrtranslit is required for transliteration. "
            "Install it with: pip install cyrtranslit"
        )
    
    if lang_code not in SUPPORTED_TRANSLITERATION_CODES:
        raise ValueError(
            f"Unsupported language code '{lang_code}'. "
            f"Supported codes: {', '.join(sorted(SUPPORTED_TRANSLITERATION_CODES))}"
        )
    
    return cyrtranslit.to_latin(text, lang_code)


def split_into_paragraphs(text: str) -> List[str]:
    """
    Split text into paragraphs based on double newlines or similar patterns.
    
    Args:
        text: The input text to split
        
    Returns:
        List of paragraph strings
    """
    # Split on double newlines, handling various line ending styles
    paragraphs = re.split(r'\n\s*\n+', text)
    
    # Filter out empty paragraphs and strip whitespace
    paragraphs = [p.strip() for p in paragraphs if p.strip()]
    
    return paragraphs


def chunk_text(text: str, max_chunk_size: int = DEFAULT_MAX_CHUNK_SIZE) -> List[str]:
    """
    Chunk text into smaller segments, preserving paragraph boundaries when possible.
    
    This function attempts to split text on paragraph boundaries to maintain
    logical coherence. If a single paragraph exceeds the max chunk size,
    it will be split on sentence boundaries or character boundaries as a fallback.
    
    Args:
        text: The input text to chunk
        max_chunk_size: Maximum size of each chunk in characters
        
    Returns:
        List of text chunks
        
    Raises:
        ValueError: If max_chunk_size is less than 100 characters
    """
    if max_chunk_size < 100:
        raise ValueError("max_chunk_size must be at least 100 characters")
    
    if not text or not text.strip():
        return []
    
    # If text is small enough, return as single chunk
    if len(text) <= max_chunk_size:
        return [text]
    
    # Split into paragraphs
    paragraphs = split_into_paragraphs(text)
    
    chunks = []
    current_chunk = []
    current_size = 0
    
    for paragraph in paragraphs:
        paragraph_size = len(paragraph)
        
        # If single paragraph is too large, we need to split it
        if paragraph_size > max_chunk_size:
            # First, save any accumulated paragraphs
            if current_chunk:
                chunks.append('\n\n'.join(current_chunk))
                current_chunk = []
                current_size = 0
            
            # Split large paragraph on sentence boundaries
            sentences = re.split(r'(?<=[.!?])\s+', paragraph)
            
            for sentence in sentences:
                sentence_size = len(sentence)
                
                # If a single sentence is too large, split by characters
                if sentence_size > max_chunk_size:
                    # Split into character chunks
                    for i in range(0, sentence_size, max_chunk_size):
                        chunk_part = sentence[i:i + max_chunk_size]
                        chunks.append(chunk_part)
                elif current_size + sentence_size + 1 > max_chunk_size:
                    # Start new chunk
                    if current_chunk:
                        chunks.append(' '.join(current_chunk))
                    current_chunk = [sentence]
                    current_size = sentence_size
                else:
                    # Add to current chunk
                    current_chunk.append(sentence)
                    current_size += sentence_size + 1  # +1 for space
            
            # Save any remaining sentences
            if current_chunk:
                chunks.append(' '.join(current_chunk))
                current_chunk = []
                current_size = 0
                
        elif current_size + paragraph_size + 2 > max_chunk_size:
            # +2 for double newline separator
            # Save current chunk and start new one
            if current_chunk:
                chunks.append('\n\n'.join(current_chunk))
            current_chunk = [paragraph]
            current_size = paragraph_size
        else:
            # Add paragraph to current chunk
            current_chunk.append(paragraph)
            current_size += paragraph_size + 2  # +2 for double newline
    
    # Don't forget the last chunk
    if current_chunk:
        chunks.append('\n\n'.join(current_chunk))
    
    return chunks


def merge_html_outputs(html_chunks: List[str], title: str = "NER Output") -> str:
    """
    Merge multiple displaCy HTML outputs into a single HTML document.
    
    This function takes multiple HTML outputs from spaCy's displaCy renderer
    and combines them into a single coherent HTML document while preserving
    entity highlighting and styling.
    
    Args:
        html_chunks: List of HTML strings to merge
        title: Title for the merged HTML document
        
    Returns:
        Merged HTML string
        
    Raises:
        ValueError: If html_chunks is empty
    """
    if not html_chunks:
        raise ValueError("html_chunks cannot be empty")
    
    # If only one chunk, return it as-is
    if len(html_chunks) == 1:
        return html_chunks[0]
    
    # Extract the CSS and content from the first chunk
    # displaCy HTML has a standard structure with <style> and <div> tags
    
    # Pattern to extract style section
    style_pattern = r'<style[^>]*>(.*?)</style>'
    # Pattern to extract the marked-up content
    content_pattern = r'<div class="entities"[^>]*>(.*?)</div>'
    
    # Get the style from the first chunk (all chunks should have same style)
    style_match = re.search(style_pattern, html_chunks[0], re.DOTALL)
    style_content = style_match.group(1) if style_match else ""
    
    # Extract content from all chunks
    all_content = []
    for i, html_chunk in enumerate(html_chunks):
        content_match = re.search(content_pattern, html_chunk, re.DOTALL)
        if content_match:
            content = content_match.group(1)
            all_content.append(content)
            # Add a visual separator between chunks if not the last one
            if i < len(html_chunks) - 1:
                all_content.append('<div style="margin: 20px 0; padding: 10px; '
                                 'border-top: 2px solid #ddd; border-bottom: 2px solid #ddd; '
                                 'text-align: center; color: #666; font-style: italic;">'
                                 '--- Document Section Break ---</div>')
        else:
            # Log warning if chunk doesn't match expected pattern
            warnings.warn(f"Chunk {i+1} doesn't match expected HTML pattern and will be skipped")
    
    # Build the merged HTML
    merged_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>{title}</title>
    <style>{style_content}</style>
</head>
<body>
    <div class="entities" style="line-height: 2.5; direction: ltr">
        {''.join(all_content)}
    </div>
</body>
</html>
"""
    
    return merged_html


def add_wikidata_links(html: str, doc) -> str:
    """
    Enhance HTML output with Wikidata links for entities with Q-IDs.
    
    This function processes the displaCy HTML output and adds clickable links
    to Wikidata for entities that have been linked to Wikidata Q-IDs through
    the entity linking component.
    
    Args:
        html: The HTML string generated by displaCy
        doc: The spaCy Doc object containing entities with kb_id attributes
        
    Returns:
        Enhanced HTML string with Wikidata links
    """
    if not doc.ents:
        return html
    
    # Build a mapping of entity text to Q-IDs
    entity_qids = {}
    for ent in doc.ents:
        # Check if entity has a kb_id that looks like a Wikidata Q-ID
        if hasattr(ent, 'kb_id_') and ent.kb_id_:
            qid = ent.kb_id_
            # Check if it's a Wikidata Q-ID (starts with Q followed by digits)
            if qid.startswith('Q') and qid[1:].isdigit():
                entity_qids[ent.text] = qid
    
    # If no Q-IDs found, return original HTML
    if not entity_qids:
        return html
    
    # Add Wikidata links to the HTML
    # We'll wrap entity marks with links where Q-IDs exist
    for entity_text, qid in entity_qids.items():
        wikidata_url = f"https://www.wikidata.org/wiki/{qid}"
        # Escape special regex characters in entity text
        escaped_text = re.escape(entity_text)
        
        # Pattern to find the entity mark without a link
        # This looks for <mark> tags that contain the entity text and don't already have a link
        pattern = f'(<mark[^>]*>)({escaped_text})(</mark>)'
        
        # Replace with linked version
        replacement = f'\\1<a href="{wikidata_url}" target="_blank" style="color: inherit; text-decoration: underline dotted;">\\2</a> <sup style="font-size: 0.7em;"><a href="{wikidata_url}" target="_blank" title="View on Wikidata">[{qid}]</a></sup>\\3'
        
        html = re.sub(pattern, replacement, html)
    
    return html


def process_text_in_chunks(
    nlp,
    text: str,
    max_chunk_size: int = DEFAULT_MAX_CHUNK_SIZE,
    output_path: Optional[Path] = None,
    progress_callback: Optional[Callable[[int, int], None]] = None,
    transliterate: bool = False,
    transliterate_lang: str = 'sr'
) -> Tuple[List, str, int]:
    """
    Process text in chunks using spaCy NLP pipeline and merge results.
    
    This is a convenience function that:
    1. Optionally transliterates Cyrillic text to Latin
    2. Chunks the input text
    3. Processes each chunk with spaCy
    4. Generates HTML visualizations
    5. Merges the HTML outputs
    6. Optionally saves to a file
    
    Args:
        nlp: spaCy language model instance
        text: Input text to process
        max_chunk_size: Maximum chunk size in characters
        output_path: Optional path to save merged HTML output
        progress_callback: Optional callback function(current_chunk, total_chunks) 
                          called before processing each chunk
        transliterate: If True, transliterate Cyrillic to Latin before processing
        transliterate_lang: Language code for transliteration (default: 'sr')
        
    Returns:
        Tuple of (all_entities, merged_html, num_chunks)
        - all_entities: List of all entities found across all chunks
        - merged_html: Merged HTML visualization
        - num_chunks: Number of chunks created
        
    Raises:
        ValueError: If nlp is None or text is empty
        ImportError: If transliterate=True but cyrtranslit is not installed
    """
    if nlp is None:
        raise ValueError("nlp model cannot be None")
    
    if not text or not text.strip():
        raise ValueError("text cannot be empty")
    
    if not DISPLACY_AVAILABLE:
        raise ImportError("spacy.displacy is required for process_text_in_chunks. Please install spacy.")
    
    # Transliterate if requested
    if transliterate:
        text = transliterate_to_latin(text, transliterate_lang)
    
    # Chunk the text
    chunks = chunk_text(text, max_chunk_size)
    
    # Process each chunk
    all_entities = []
    html_outputs = []
    
    for i, chunk in enumerate(chunks):
        # Call progress callback if provided
        if progress_callback:
            progress_callback(i, len(chunks))
        
        # Process with spaCy
        doc = nlp(chunk)
        
        # Collect entities
        all_entities.extend(doc.ents)
        
        # Generate HTML for this chunk
        # Use page=True to get the full HTML page (including wrapper)
        html = displacy.render(doc, style="ent", page=True)
        
        # Add Wikidata links for entities with Q-IDs
        html = add_wikidata_links(html, doc)
        
        html_outputs.append(html)
    
    # Merge HTML outputs
    merged_html = merge_html_outputs(html_outputs, title="Chunked NER Output")
    
    # Save if output path provided
    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(merged_html)
    
    return all_entities, merged_html, len(chunks)
