#!/usr/bin/env python3
"""
Integration test demonstrating the complete text chunking workflow.

This script shows how to use the text chunking functionality in a real-world scenario.
It requires a trained spaCy model to be available.
"""

import sys
from pathlib import Path

# Add src directory to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

try:
    import spacy
    from text_chunker import process_text_in_chunks, chunk_text, DEFAULT_MAX_CHUNK_SIZE
except ImportError as e:
    print(f"Error: {e}")
    print("Please ensure spaCy is installed and text_chunker.py is available.")
    sys.exit(1)


def create_large_sample_text():
    """Create a large sample text for testing."""
    base_text = """
Apple Inc. is an American multinational technology company headquartered in Cupertino, California. 
Tim Cook is the CEO of Apple. The company was founded by Steve Jobs, Steve Wozniak, and Ronald Wayne in 1976.
Apple is known for products like the iPhone, iPad, and Mac computers.

Microsoft Corporation, founded by Bill Gates and Paul Allen in 1975, is headquartered in Redmond, Washington.
Satya Nadella currently serves as the CEO. Microsoft is famous for Windows, Office, and Azure cloud services.

Google LLC, founded by Larry Page and Sergey Brin in 1998, is based in Mountain View, California.
Sundar Pichai is the current CEO. Google is known for its search engine, Android, and cloud computing services.

Amazon.com, Inc., founded by Jeff Bezos in 1994, is headquartered in Seattle, Washington.
Andy Jassy became CEO in 2021. Amazon is famous for e-commerce, AWS, and cloud computing services.

Tesla, Inc., founded by Elon Musk and others in 2003, is based in Austin, Texas.
The company specializes in electric vehicles and clean energy products.
"""
    
    # Repeat the text to make it large enough to demonstrate chunking
    # Let's create about 150K characters (enough to trigger chunking at 100K threshold)
    repetitions = 150
    large_text = "\n\n".join([base_text.strip() for _ in range(repetitions)])
    
    return large_text


def test_with_blank_model():
    """Test using spaCy's blank model (no training required)."""
    print("=" * 70)
    print("INTEGRATION TEST: Using Blank spaCy Model")
    print("=" * 70)
    
    # Create a blank English model
    print("\nCreating blank spaCy model...")
    nlp = spacy.blank("en")
    
    # Create sample text
    text = create_large_sample_text()
    print(f"Created sample text: {len(text):,} characters")
    
    # Test chunking
    print(f"\nChunking text (max size: {DEFAULT_MAX_CHUNK_SIZE:,} chars)...")
    chunks = chunk_text(text, max_chunk_size=DEFAULT_MAX_CHUNK_SIZE)
    print(f"Created {len(chunks)} chunks:")
    for i, chunk in enumerate(chunks, 1):
        print(f"  Chunk {i}: {len(chunk):,} characters")
    
    # Test full processing
    print("\nProcessing chunks with spaCy...")
    output_dir = PROJECT_ROOT / "data" / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "integration_test_output.html"
    
    try:
        entities, html = process_text_in_chunks(
            nlp, 
            text, 
            max_chunk_size=DEFAULT_MAX_CHUNK_SIZE,
            output_path=output_file
        )
        
        print(f"✓ Processing complete!")
        print(f"  Total entities found: {len(entities)}")
        print(f"  HTML output saved to: {output_file}")
        print(f"  HTML size: {len(html):,} characters")
        
        # Verify file was created
        if output_file.exists():
            print(f"✓ Output file verified: {output_file}")
        else:
            print(f"✗ Warning: Output file not found at {output_file}")
        
        return True
        
    except Exception as e:
        print(f"\n✗ Error during processing: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_small_text():
    """Test with small text that doesn't need chunking."""
    print("\n" + "=" * 70)
    print("INTEGRATION TEST: Small Text (No Chunking)")
    print("=" * 70)
    
    nlp = spacy.blank("en")
    
    text = """Apple Inc. is headquartered in Cupertino, California. 
Tim Cook is the CEO. The company was founded by Steve Jobs in 1976."""
    
    print(f"\nProcessing small text ({len(text)} chars)...")
    
    try:
        entities, html = process_text_in_chunks(nlp, text)
        print(f"✓ Processing complete!")
        print(f"  Total entities found: {len(entities)}")
        print(f"  HTML size: {len(html):,} characters")
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def main():
    """Run integration tests."""
    print("\n")
    print("*" * 70)
    print("*" + " " * 68 + "*")
    print("*" + "  TEXT CHUNKER INTEGRATION TEST SUITE".center(68) + "*")
    print("*" + " " * 68 + "*")
    print("*" * 70)
    print("\n")
    
    results = []
    
    # Test 1: Small text
    results.append(("Small Text Test", test_small_text()))
    
    # Test 2: Large text with chunking
    results.append(("Large Text Test", test_with_blank_model()))
    
    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    for test_name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{test_name}: {status}")
    
    all_passed = all(result[1] for result in results)
    
    if all_passed:
        print("\n" + "=" * 70)
        print("ALL INTEGRATION TESTS PASSED!")
        print("=" * 70)
        print()
        return 0
    else:
        print("\n" + "=" * 70)
        print("SOME TESTS FAILED!")
        print("=" * 70)
        print()
        return 1


if __name__ == "__main__":
    sys.exit(main())
