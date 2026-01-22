# assistant/__init__.py
"""
PyCode AI Assistant Package

A modular AI assistant system for Python learning, providing:
- Python concept explanations
- Code review and bug detection
- Interview preparation
- Automation testing concepts (Selenium, Robot Framework, pytest)

This package splits the functionality from builtin_assistant.py for better
maintainability and performance.

For backward compatibility, import from builtin_assistant.py which re-exports
all functions from this package.
"""

from .python_concepts import CONCEPTS, get_concept_explanation
from .helpers import (
    extract_topic,
    normalize_topic,
    is_code_block,
    format_code_block,
    format_bullet_points,
    clean_response_text
)
from .response_generator import (
    generate_response,
    generate_hint_response,
    generate_default_response,
    generate_greeting
)
from .code_analyzer import (
    get_code_review,
    get_bug_hint,
    get_smart_hint,
    analyze_code_quality,
    detect_common_mistakes
)

__all__ = [
    # Concepts
    'CONCEPTS',
    'get_concept_explanation',
    
    # Helpers
    'extract_topic',
    'normalize_topic',
    'is_code_block',
    'format_code_block',
    'format_bullet_points',
    'clean_response_text',
    
    # Response generation
    'generate_response',
    'generate_hint_response',
    'generate_default_response',
    'generate_greeting',
    
    # Code analysis
    'get_code_review',
    'get_bug_hint',
    'get_smart_hint',
    'analyze_code_quality',
    'detect_common_mistakes',
]

