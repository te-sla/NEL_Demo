#!/usr/bin/env python3
"""
Manual test script for text chunking functionality.

This script demonstrates the text chunking feature without requiring
a trained spaCy model, using spaCy's blank model instead.
"""

import sys
from pathlib import Path

# Add src directory to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from text_chunker import chunk_text, merge_html_outputs, split_into_paragraphs


def test_paragraph_splitting():
    """Test paragraph splitting functionality."""
    print("=" * 70)
    print("TEST 1: Paragraph Splitting")
    print("=" * 70)
    
    text = """This is the first paragraph. It contains multiple sentences. 
Each sentence adds to the content.

This is the second paragraph. It is separated by a double newline.

And here is a third paragraph. The text chunker should preserve these boundaries."""
    
    paragraphs = split_into_paragraphs(text)
    print(f"\nOriginal text has {len(text)} characters")
    print(f"Split into {len(paragraphs)} paragraphs:\n")
    
    for i, para in enumerate(paragraphs, 1):
        print(f"Paragraph {i} ({len(para)} chars):")
        print(f"  {para[:80]}..." if len(para) > 80 else f"  {para}")
        print()


def test_text_chunking():
    """Test text chunking with different sizes."""
    print("=" * 70)
    print("TEST 2: Text Chunking")
    print("=" * 70)
    
    # Create a larger text with multiple paragraphs
    paragraphs = []
    for i in range(10):
        para = f"This is paragraph {i+1}. " * 50  # ~1000 chars per paragraph
        paragraphs.append(para)
    
    text = "\n\n".join(paragraphs)
    
    print(f"\nOriginal text: {len(text):,} characters")
    print(f"Total paragraphs: {len(paragraphs)}")
    
    # Test with different chunk sizes
    for chunk_size in [2000, 5000]:
        chunks = chunk_text(text, max_chunk_size=chunk_size)
        print(f"\nWith max_chunk_size={chunk_size:,}:")
        print(f"  Created {len(chunks)} chunks")
        for i, chunk in enumerate(chunks, 1):
            print(f"  Chunk {i}: {len(chunk):,} characters")


def test_html_merging():
    """Test HTML merging functionality."""
    print("=" * 70)
    print("TEST 3: HTML Merging")
    print("=" * 70)
    
    # Create sample HTML chunks similar to displaCy output
    html_chunks = []
    for i in range(3):
        html = f'''<!DOCTYPE html>
<html>
<head>
    <style>
        .entities {{ line-height: 2.5; }}
        mark.entity {{ background: #ddd; padding: 0.25em; }}
    </style>
</head>
<body>
    <div class="entities" style="line-height: 2.5">
        This is chunk {i+1} with some <mark class="entity" style="background: #ddd;">entity text</mark>.
    </div>
</body>
</html>'''
        html_chunks.append(html)
    
    print(f"\nMerging {len(html_chunks)} HTML chunks...")
    merged = merge_html_outputs(html_chunks, title="Test Merge")
    
    print(f"Merged HTML size: {len(merged):,} characters")
    print(f"Contains 'Document Section Break': {('Document Section Break' in merged)}")
    print(f"Number of entity markers: {merged.count('mark.entity')}")
    
    # Save to temp file for inspection
    temp_file = PROJECT_ROOT / "temp_test_output.html"
    with open(temp_file, "w", encoding="utf-8") as f:
        f.write(merged)
    print(f"\nMerged HTML saved to: {temp_file}")
    print("You can open this file in a browser to see the merged output.")


def test_edge_cases():
    """Test edge cases."""
    print("=" * 70)
    print("TEST 4: Edge Cases")
    print("=" * 70)
    
    # Test with Unicode
    unicode_text = "Hello 世界\n\nBonjour le monde\n\nΓεια σου κόσμε"
    paragraphs = split_into_paragraphs(unicode_text)
    print(f"\nUnicode text split into {len(paragraphs)} paragraphs")
    for i, para in enumerate(paragraphs, 1):
        print(f"  Paragraph {i}: {para}")
    
    # Test with very long sentence (no paragraph breaks)
    long_sentence = "word " * 1000  # ~5000 chars
    chunks = chunk_text(long_sentence, max_chunk_size=1000)
    print(f"\nLong sentence ({len(long_sentence):,} chars) split into {len(chunks)} chunks")
    print(f"  Chunk sizes: {[len(c) for c in chunks]}")
    
    # Test with empty text
    empty_chunks = chunk_text("")
    print(f"\nEmpty text produces {len(empty_chunks)} chunks")
    
    # Test with single character repeated
    single_char = "a" * 10000
    chunks = chunk_text(single_char, max_chunk_size=1000)
    print(f"\nSingle character repeated ({len(single_char):,} chars) split into {len(chunks)} chunks")


def main():
    """Run all manual tests."""
    print("\n")
    print("*" * 70)
    print("*" + " " * 68 + "*")
    print("*" + "  TEXT CHUNKER MANUAL TEST SUITE".center(68) + "*")
    print("*" + " " * 68 + "*")
    print("*" * 70)
    print("\n")
    
    try:
        test_paragraph_splitting()
        print("\n")
        
        test_text_chunking()
        print("\n")
        
        test_html_merging()
        print("\n")
        
        test_edge_cases()
        print("\n")
        
        print("=" * 70)
        print("ALL MANUAL TESTS COMPLETED SUCCESSFULLY!")
        print("=" * 70)
        print()
        
    except Exception as e:
        print(f"\n\nERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
