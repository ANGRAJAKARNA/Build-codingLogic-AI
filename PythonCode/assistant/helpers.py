# assistant/helpers.py
"""
Helper functions for the AI assistant.
Text processing, topic extraction, and formatting utilities.
"""

import re
from typing import List, Optional, Tuple


def extract_topic(message: str) -> str:
    """
    Extract the main topic from a user message.
    
    Args:
        message: User's input message
        
    Returns:
        Extracted topic string, cleaned and normalized
    """
    message_lower = message.lower().strip()
    
    # Remove common question patterns
    patterns_to_remove = [
        r'^(what|who|when|where|why|how)\s+(is|are|do|does|did|can|could|would|should)\s+',
        r'^(explain|describe|tell me about|show me|give me|help with)\s+',
        r'^(i want to|i need to|can you|could you|please)\s+',
        r'(learn|understand|know)\s+(about|how)\s+',
        r'\?+$',
        r'^the\s+',
        r'^a\s+',
        r'^an\s+',
    ]
    
    topic = message_lower
    for pattern in patterns_to_remove:
        topic = re.sub(pattern, '', topic)
    
    # Clean up whitespace
    topic = ' '.join(topic.split())
    
    return topic


def normalize_topic(topic: str) -> str:
    """
    Normalize a topic string for matching.
    
    Args:
        topic: Topic string to normalize
        
    Returns:
        Normalized topic string
    """
    # Remove special characters
    normalized = re.sub(r'[^\w\s-]', '', topic.lower())
    
    # Replace multiple spaces with single space
    normalized = ' '.join(normalized.split())
    
    # Common normalizations
    normalizations = {
        'classes': 'class',
        'functions': 'function',
        'loops': 'loop',
        'lists': 'list',
        'dicts': 'dictionary',
        'dictionaries': 'dictionary',
        'strings': 'string',
        'tuples': 'tuple',
        'sets': 'set',
        'objects': 'object',
        'methods': 'method',
        'decorators': 'decorator',
        'exceptions': 'exception',
        'generators': 'generator',
        'iterators': 'iterator',
        'modules': 'module',
        'packages': 'package',
        'keywords': 'keyword',
        'data types': 'data type',
        'datatypes': 'data type',
        'regular expressions': 'regex',
        'regexp': 'regex',
        're': 'regex',
        'oop': 'object oriented programming',
        'oops': 'object oriented programming',
    }
    
    for old, new in normalizations.items():
        if normalized == old:
            return new
    
    return normalized


def is_code_block(text: str) -> bool:
    """
    Check if text appears to be a code block.
    
    Args:
        text: Text to check
        
    Returns:
        True if text appears to be code
    """
    code_indicators = [
        r'^\s*def\s+\w+\s*\(',
        r'^\s*class\s+\w+',
        r'^\s*import\s+',
        r'^\s*from\s+\w+\s+import',
        r'^\s*if\s+.*:$',
        r'^\s*for\s+.*:$',
        r'^\s*while\s+.*:$',
        r'^\s*try\s*:',
        r'^\s*except\s*',
        r'^\s*return\s+',
        r'^\s*#.*',  # Comments
        r'^\s*"""',  # Docstrings
        r"^\s*'''",
    ]
    
    lines = text.strip().split('\n')
    for line in lines[:5]:  # Check first 5 lines
        for pattern in code_indicators:
            if re.match(pattern, line):
                return True
    
    return False


def format_code_block(code: str, language: str = "python") -> str:
    """
    Format code with markdown code block syntax.
    
    Args:
        code: Code string to format
        language: Language for syntax highlighting
        
    Returns:
        Formatted code block
    """
    code = code.strip()
    if not code:
        return ""
    
    # Don't double-wrap if already wrapped
    if code.startswith("```"):
        return code
    
    return f"```{language}\n{code}\n```"


def format_bullet_points(items: List[str], prefix: str = "•") -> str:
    """
    Format a list of items as bullet points.
    
    Args:
        items: List of strings to format
        prefix: Bullet character to use
        
    Returns:
        Formatted bullet point string
    """
    if not items:
        return ""
    
    return '\n'.join(f"{prefix} {item}" for item in items)


def clean_response_text(text: str) -> str:
    """
    Clean and normalize response text.
    
    Args:
        text: Text to clean
        
    Returns:
        Cleaned text
    """
    if not text:
        return ""
    
    # Fix common OCR/PDF extraction errors
    fixes = {
        ' yo ': ' you ',
        'yocan': 'you can',
        'yocreate': 'you create',
        'yowrite': 'you write',
        'yodefine': 'you define',
        'manreal': 'many real',
        'automaticall': 'automatically',
        'categorof': 'category of',
        'modifthe': 'modify the',
        '  ': ' ',  # Double spaces
    }
    
    result = text
    for old, new in fixes.items():
        result = result.replace(old, new)
    
    # Clean up multiple newlines
    result = re.sub(r'\n{3,}', '\n\n', result)
    
    # Clean up trailing whitespace
    result = '\n'.join(line.rstrip() for line in result.split('\n'))
    
    return result.strip()


def detect_question_type(message: str) -> str:
    """
    Detect the type of question being asked.
    
    Args:
        message: User's message
        
    Returns:
        Question type: 'definition', 'how_to', 'why', 'comparison', 'example', 'other'
    """
    message_lower = message.lower()
    
    if any(p in message_lower for p in ['what is', 'what are', 'define', 'meaning of']):
        return 'definition'
    
    if any(p in message_lower for p in ['how to', 'how do', 'how can', 'how does']):
        return 'how_to'
    
    if any(p in message_lower for p in ['why', 'reason', 'purpose']):
        return 'why'
    
    if any(p in message_lower for p in ['difference', 'compare', 'vs', 'versus', 'better']):
        return 'comparison'
    
    if any(p in message_lower for p in ['example', 'show', 'demonstrate', 'sample']):
        return 'example'
    
    return 'other'


def split_multiple_topics(message: str) -> List[str]:
    """
    Split a message containing multiple topics.
    
    Args:
        message: User's message potentially containing multiple topics
        
    Returns:
        List of individual topics
    """
    # Common separators
    separators = [',', ' and ', '; ', ' & ']
    
    # Check if message looks like multiple topics
    has_separator = any(sep in message.lower() for sep in separators)
    
    if not has_separator:
        return [message]
    
    # Split on separators
    topics = [message]
    for sep in separators:
        new_topics = []
        for topic in topics:
            parts = topic.split(sep)
            new_topics.extend([p.strip() for p in parts if p.strip()])
        topics = new_topics
    
    # Remove common prefixes like "explain", "what is"
    cleaned_topics = []
    for topic in topics:
        cleaned = extract_topic(topic)
        if cleaned:
            cleaned_topics.append(cleaned)
    
    return cleaned_topics if cleaned_topics else [message]


def truncate_text(text: str, max_length: int = 500, suffix: str = "...") -> str:
    """
    Truncate text to maximum length while preserving word boundaries.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated
        
    Returns:
        Truncated text
    """
    if not text or len(text) <= max_length:
        return text
    
    # Find the last space before max_length
    truncated = text[:max_length]
    last_space = truncated.rfind(' ')
    
    if last_space > max_length * 0.7:  # Don't truncate too much
        truncated = truncated[:last_space]
    
    return truncated.rstrip() + suffix


def highlight_code_in_text(text: str) -> str:
    """
    Find and highlight inline code in text using backticks.
    
    Args:
        text: Text that may contain code references
        
    Returns:
        Text with code highlighted in backticks
    """
    # Pattern for common code elements
    code_patterns = [
        r'\b(def\s+\w+)',  # Function definitions
        r'\b(class\s+\w+)',  # Class definitions
        r'\b([A-Z][a-zA-Z]*Error)\b',  # Exception names
        r'\b(__\w+__)\b',  # Dunder methods
        r'\b(\w+\.(?:append|pop|insert|remove|sort|reverse|get|keys|values|items)\(\))',  # Method calls
    ]
    
    for pattern in code_patterns:
        text = re.sub(pattern, r'`\1`', text)
    
    return text

