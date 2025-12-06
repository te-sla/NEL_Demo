#!/usr/bin/env python3
"""Text Chunking Module for spaCy NER Processing.

This module provides functionality to chunk large text documents into smaller
segments to prevent exceeding spaCy's document length limits. It preserves
text structure by chunking on paragraph boundaries when possible, and merges
the resulting HTML visualizations into a single output.

spaCy has practical limits on document length (typically around 1,000,000 characters)
for efficient processing. This module helps handle larger documents by:
1. Splitting text into manageable chunks
2. Processing each chunk separately
3. Merging the HTML outputs into a cohesive visualization
"""

from __future__ import annotations

import re
import warnings
from pathlib import Path
from typing import TYPE_CHECKING, List, Optional, Tuple

if TYPE_CHECKING:
    from spacy.language import Language
    from spacy.tokens import Span

# Try to import spacy's displacy for HTML rendering
# This is optional and only needed for process_text_in_chunks function
try:
    from spacy import displacy

    DISPLACY_AVAILABLE = True
except ImportError:
    DISPLACY_AVAILABLE = False
    displacy = None


# Constants
DEFAULT_MAX_CHUNK_SIZE: int = 100000  # 100K characters per chunk
MIN_CHUNK_SIZE: int = 100
PARAGRAPH_SEPARATOR: str = '\n\n'
SECTION_BREAK_HTML: str = (
    '<div style="margin: 20px 0; padding: 10px; '
    'border-top: 2px solid #ddd; border-bottom: 2px solid #ddd; '
    'text-align: center; color: #666; font-style: italic;">'
    '--- Document Section Break ---</div>'
)

# Public API
__all__ = [
    'split_into_paragraphs',
    'chunk_text',
    'merge_html_outputs',
    'process_text_in_chunks',
    'DEFAULT_MAX_CHUNK_SIZE',
]


def split_into_paragraphs(text: str) -> List[str]:
    """Split text into paragraphs based on double newlines or similar patterns.
    
    This function splits text on double newlines while handling various line
    ending styles (CRLF, LF, etc.) and filtering out empty paragraphs.
    
    Args:
        text: The input text to split into paragraphs.
        
    Returns:
        A list of non-empty paragraph strings with whitespace stripped.
        Returns an empty list if the input text is empty or contains only whitespace.
        
    Example:
        >>> text = "First paragraph.\\n\\nSecond paragraph."
        >>> split_into_paragraphs(text)
        ['First paragraph.', 'Second paragraph.']
    """
    if not text or not text.strip():
        return []
    
    # Split on double newlines, handling various line ending styles
    paragraphs = re.split(r'\n\s*\n+', text)
    
    # Filter out empty paragraphs and strip whitespace
    return [p.strip() for p in paragraphs if p.strip()]


def chunk_text(text: str, max_chunk_size: int = DEFAULT_MAX_CHUNK_SIZE) -> List[str]:
    """Chunk text into smaller segments, preserving paragraph boundaries when possible.
    
    This function attempts to split text on paragraph boundaries to maintain
    logical coherence. If a single paragraph exceeds the max chunk size,
    it will be split on sentence boundaries or character boundaries as a fallback.
    
    Args:
        text: The input text to chunk.
        max_chunk_size: Maximum size of each chunk in characters. Must be at least 100.
        
    Returns:
        A list of text chunks. Returns an empty list if the input text is empty.
        Each chunk will be at most max_chunk_size characters (with small tolerance
        for boundary preservation).
        
    Raises:
        ValueError: If max_chunk_size is less than MIN_CHUNK_SIZE (100 characters).
        
    Example:
        >>> text = "Para 1.\\n\\nPara 2.\\n\\nPara 3."
        >>> chunks = chunk_text(text, max_chunk_size=20)
        >>> len(chunks) >= 3
        True
    """
    if max_chunk_size < MIN_CHUNK_SIZE:
        raise ValueError(f"max_chunk_size must be at least {MIN_CHUNK_SIZE} characters")
    
    if not text or not text.strip():
        return []
    
    # If text is small enough, return as single chunk
    if len(text) <= max_chunk_size:
        return [text]
    
    # Split into paragraphs
    paragraphs = split_into_paragraphs(text)
    
    chunks: List[str] = []
    current_chunk: List[str] = []
    current_size = 0
    
    for paragraph in paragraphs:
        paragraph_size = len(paragraph)
        
        # If single paragraph is too large, we need to split it
        if paragraph_size > max_chunk_size:
            # First, save any accumulated paragraphs
            if current_chunk:
                chunks.append(PARAGRAPH_SEPARATOR.join(current_chunk))
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
                chunks.append(PARAGRAPH_SEPARATOR.join(current_chunk))
            current_chunk = [paragraph]
            current_size = paragraph_size
        else:
            # Add paragraph to current chunk
            current_chunk.append(paragraph)
            current_size += paragraph_size + 2  # +2 for double newline
    
    # Don't forget the last chunk
    if current_chunk:
        chunks.append(PARAGRAPH_SEPARATOR.join(current_chunk))
    
    return chunks


def merge_html_outputs(html_chunks: List[str], title: str = "NER Output") -> str:
    """Merge multiple displaCy HTML outputs into a single HTML document.
    
    This function takes multiple HTML outputs from spaCy's displaCy renderer
    and combines them into a single coherent HTML document while preserving
    entity highlighting and styling.
    
    Args:
        html_chunks: List of HTML strings to merge. Must not be empty.
        title: Title for the merged HTML document. Defaults to "NER Output".
        
    Returns:
        A merged HTML string containing all chunks with section breaks between them.
        If only one chunk is provided, it's returned as-is.
        
    Raises:
        ValueError: If html_chunks is empty.
        
    Example:
        >>> html1 = '<html><head><style>.entities {}</style></head><body><div class="entities">Text 1</div></body></html>'
        >>> html2 = '<html><head><style>.entities {}</style></head><body><div class="entities">Text 2</div></body></html>'
        >>> merged = merge_html_outputs([html1, html2])
        >>> 'Text 1' in merged and 'Text 2' in merged
        True
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
    all_content: List[str] = []
    for i, html_chunk in enumerate(html_chunks):
        content_match = re.search(content_pattern, html_chunk, re.DOTALL)
        if content_match:
            content = content_match.group(1)
            all_content.append(content)
            # Add a visual separator between chunks if not the last one
            if i < len(html_chunks) - 1:
                all_content.append(SECTION_BREAK_HTML)
        else:
            # Log warning if chunk doesn't match expected pattern
            warnings.warn(
                f"Chunk {i+1} doesn't match expected HTML pattern and will be skipped",
                UserWarning,
                stacklevel=2
            )
    
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


def process_text_in_chunks(
    nlp: "Language",
    text: str,
    max_chunk_size: int = DEFAULT_MAX_CHUNK_SIZE,
    output_path: Optional[Path] = None
) -> Tuple[List["Span"], str, int]:
    """Process text in chunks using spaCy NLP pipeline and merge results.
    
    This is a convenience function that:
    1. Chunks the input text
    2. Processes each chunk with spaCy
    3. Generates HTML visualizations
    4. Merges the HTML outputs
    5. Optionally saves to a file
    
    Args:
        nlp: spaCy language model instance. Must not be None.
        text: Input text to process. Must not be empty or whitespace-only.
        max_chunk_size: Maximum chunk size in characters. Defaults to DEFAULT_MAX_CHUNK_SIZE.
        output_path: Optional path to save merged HTML output. Parent directories will be
                     created if they don't exist.
        
    Returns:
        A tuple containing:
        - all_entities: List of all entities found across all chunks
        - merged_html: Merged HTML visualization string
        - num_chunks: Number of chunks created
        
    Raises:
        ValueError: If nlp is None or text is empty/whitespace-only.
        ImportError: If spacy.displacy is not available.
        
    Example:
        >>> import spacy
        >>> nlp = spacy.blank("en")
        >>> text = "Some text to process."
        >>> entities, html, n_chunks = process_text_in_chunks(nlp, text)
        >>> n_chunks >= 1
        True
    """
    if nlp is None:
        raise ValueError("nlp model cannot be None")
    
    if not text or not text.strip():
        raise ValueError("text cannot be empty")
    
    if not DISPLACY_AVAILABLE:
        raise ImportError("spacy.displacy is required for process_text_in_chunks. Please install spacy.")
    
    # Chunk the text
    chunks = chunk_text(text, max_chunk_size)
    
    # Process each chunk
    all_entities: List["Span"] = []
    html_outputs: List[str] = []
    
    for chunk in chunks:
        # Process with spaCy
        doc = nlp(chunk)
        
        # Collect entities
        all_entities.extend(doc.ents)
        
        # Generate HTML for this chunk
        # Use page=True to get the full HTML page (including wrapper)
        html = displacy.render(doc, style="ent", page=True)
        html_outputs.append(html)
    
    # Merge HTML outputs
    merged_html = merge_html_outputs(html_outputs, title="Chunked NER Output")
    
    # Save if output path provided
    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(merged_html)
    
    return all_entities, merged_html, len(chunks)
