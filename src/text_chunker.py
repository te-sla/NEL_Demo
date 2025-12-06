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
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Callable, List, Optional, Tuple

from logging_utils import get_logger
from spacy import displacy


logger = get_logger(__name__)

# Default maximum chunk size (conservative estimate for spaCy)
DEFAULT_MAX_CHUNK_SIZE = 100000  # 100K characters per chunk


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
    
    logger.debug("Split text into %d paragraphs", len(paragraphs))
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

    logger.debug("Chunking text of length %d with max_chunk_size=%d", len(text), max_chunk_size)
    
    if not text or not text.strip():
        logger.info("Received empty or whitespace-only text; returning no chunks")
        return []
    
    # If text is small enough, return as single chunk
    if len(text) <= max_chunk_size:
        logger.debug("Text fits within max_chunk_size; returning single chunk")
        return [text]
    
    # Split into paragraphs
    paragraphs = split_into_paragraphs(text)
    
    chunks: List[str] = []
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
    
    logger.debug("Merging %d HTML chunk(s) into a single document titled '%s'", len(html_chunks), title)

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
            logger.warning("Chunk %d does not match expected HTML pattern and will be skipped", i + 1)
    
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
    
    logger.debug("Merged HTML length: %d characters", len(merged_html))
    return merged_html


def process_text_in_chunks(
    nlp,
    text: str,
    max_chunk_size: int = DEFAULT_MAX_CHUNK_SIZE,
    output_path: Optional[Path] = None,
    progress_callback: Optional[Callable[[int, int], None]] = None,
) -> Tuple[List, str, int]:
    """
    Process text in chunks using spaCy NLP pipeline and merge results.
    
    This is a convenience function that:
    1. Chunks the input text
    2. Processes each chunk with spaCy
    3. Generates HTML visualizations
    4. Merges the HTML outputs
    5. Optionally saves to a file
    
    Args:
        nlp: spaCy language model instance
        text: Input text to process
        max_chunk_size: Maximum chunk size in characters
        output_path: Optional path to save merged HTML output
        progress_callback: Optional callable receiving (completed_chunks, total_chunks)
        
    Returns:
        Tuple of (all_entities, merged_html, num_chunks)
        - all_entities: List of all entities found across all chunks
        - merged_html: Merged HTML visualization
        - num_chunks: Number of chunks created
        
    Raises:
        ValueError: If nlp is None or text is empty
    """
    if nlp is None:
        raise ValueError("nlp model cannot be None")
    
    if not text or not text.strip():
        raise ValueError("text cannot be empty")
    
    # Chunk the text
    chunks = chunk_text(text, max_chunk_size)
    logger.info("Processing %d chunk(s) with max_chunk_size=%d", len(chunks), max_chunk_size)
    
    # Process each chunk
    all_entities = []
    html_outputs = []

    if progress_callback:
        progress_callback(0, len(chunks))

    for index, chunk in enumerate(chunks, start=1):
        # Process with spaCy
        logger.debug("Processing chunk %d with length %d", index, len(chunk))
        doc = nlp(chunk)
        
        # Collect entities
        all_entities.extend(doc.ents)
        
        # Generate HTML for this chunk
        # Use page=True to get the full HTML page (including wrapper)
        html = displacy.render(doc, style="ent", page=True)
        html_outputs.append(html)

        if progress_callback:
            progress_callback(index, len(chunks))
    
    # Merge HTML outputs
    merged_html = merge_html_outputs(html_outputs, title="Chunked NER Output")
    
    # Save if output path provided
    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(merged_html)
        logger.info("Merged HTML written to %s", output_path)
    
    logger.info("Completed processing with %d entity(ies) found across %d chunk(s)", len(all_entities), len(chunks))
    return all_entities, merged_html, len(chunks)
