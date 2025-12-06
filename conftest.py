#!/usr/bin/env python3
"""
Shared test fixtures and configuration for pytest.

This module provides common fixtures used across multiple test files,
ensuring consistent test setup and reducing code duplication.
"""

import pytest
import spacy


@pytest.fixture
def rule_based_nlp():
    """Create a lightweight spaCy pipeline with deterministic entities.
    
    This fixture provides a rule-based NLP model that produces consistent,
    deterministic entities for testing without requiring a trained model download.
    The entity ruler recognizes common test entities like "Apple", "Cupertino",
    "Microsoft", and "Tim Cook".
    
    Returns:
        spacy.Language: A spaCy language model with entity ruler configured.
    """
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
