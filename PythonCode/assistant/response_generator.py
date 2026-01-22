# assistant/response_generator.py
"""
Response generation for the AI assistant.
Handles creating formatted responses for various query types.
"""

import random
from typing import Optional, List, Tuple

from .python_concepts import get_concept_explanation, CONCEPTS
from .helpers import (
    extract_topic,
    normalize_topic,
    detect_question_type,
    split_multiple_topics,
    clean_response_text
)


def generate_greeting() -> str:
    """Generate a friendly greeting message."""
    greetings = [
        "👋 Hello! I'm your Python tutor. How can I help you today?",
        "🐍 Hi there! Ready to learn some Python? What would you like to explore?",
        "👋 Welcome! I'm here to help with Python concepts, coding problems, and more!",
        "🎓 Hello! Ask me anything about Python programming!",
    ]
    return random.choice(greetings)


def generate_default_response(topic: str = "") -> str:
    """
    Generate a helpful default response when no specific answer is found.
    
    Args:
        topic: The topic that wasn't found (optional)
        
    Returns:
        A helpful message with suggestions
    """
    if topic:
        return f"""I don't have specific information about "{topic}" in my knowledge base.

**Try asking about:**
• Basic concepts: class, object, function, loop, list, dictionary
• OOP concepts: inheritance, polymorphism, encapsulation, abstraction
• Data types: strings, lists, tuples, sets, dictionaries
• Advanced: decorators, generators, context managers, regex

Or try rephrasing your question!"""
    
    return """## 🤖 Python Tutor

I'm here to help! Here's what I can do:

**💬 Ask Me About:**

**Problem Help:**
- "Give me a hint" - progressive hints
- "Explain the problem" - understand what's needed
- "How to approach this" - strategy guidance

**Debugging:**
- "Help with error" - analyze your code
- "Why isn't this working" - find bugs

**Learning:**
- "What is [concept]" - detailed explanations
- "Explain recursion" - algorithm concepts
- "How does [X] work" - Python features

**📚 Available Topics:**
`class`, `object`, `function`, `list`, `dictionary`, `loop`, 
`decorator`, `exception`, `recursion`, `data type`, `oop`, `regex`"""


def generate_hint_response(
    problem: str,
    function_name: str,
    user_code: str,
    hints: List[str],
    hint_level: int
) -> str:
    """
    Generate a progressive hint based on the hint level.
    
    Args:
        problem: The problem description
        function_name: The function to implement
        user_code: User's current code
        hints: List of available hints
        hint_level: Current hint level (1-indexed)
        
    Returns:
        Appropriate hint for the level
    """
    if not hints:
        # Generate generic hints
        if hint_level == 1:
            return f"💡 **Think about the problem:** What does `{function_name}` need to do? What input does it receive?"
        elif hint_level == 2:
            return f"💡 **Consider the approach:** What's the simplest way to solve this? What data structures might help?"
        elif hint_level == 3:
            return f"💡 **Implementation hint:** Try breaking the problem into smaller steps. What's the first thing you need to do?"
        else:
            return f"💡 **Almost there!** Make sure your function returns the correct type and handles edge cases."
    
    # Use provided hints
    if hint_level <= len(hints):
        return f"💡 **Hint {hint_level}:** {hints[hint_level - 1]}"
    
    # Beyond available hints
    return f"💡 **Final hint:** Review the first {len(hints)} hints and think about how they connect."


def generate_response(
    message: str,
    question: str = "",
    function_name: str = "",
    user_code: str = "",
    interview_mode: bool = False
) -> str:
    """
    Generate a response to a user message.
    
    Args:
        message: User's message
        question: Current problem description (if any)
        function_name: Current function to implement (if any)
        user_code: User's current code (if any)
        interview_mode: Whether in interview mode
        
    Returns:
        Generated response string
    """
    message_lower = message.lower().strip()
    
    # Check for greeting
    greeting_patterns = ['hi', 'hello', 'hey', 'good morning', 'good evening']
    if any(message_lower == p or message_lower.startswith(p + ' ') for p in greeting_patterns):
        return generate_greeting()
    
    # Check for help request
    if message_lower in ['help', '?', 'what can you do']:
        return generate_default_response()
    
    # Check for multiple topics
    topics = split_multiple_topics(message)
    if len(topics) > 1:
        responses = []
        for topic in topics:
            response = _generate_single_response(topic, question, function_name, user_code)
            if response and "don't have" not in response.lower():
                responses.append(response)
        
        if responses:
            return "\n\n---\n\n".join(responses)
    
    # Single topic response
    return _generate_single_response(message, question, function_name, user_code)


def _generate_single_response(
    message: str,
    question: str = "",
    function_name: str = "",
    user_code: str = ""
) -> str:
    """Generate response for a single topic."""
    topic = extract_topic(message)
    normalized = normalize_topic(topic)
    question_type = detect_question_type(message)
    
    # Check for concept explanation
    explanation = get_concept_explanation(normalized)
    if explanation:
        return explanation
    
    # Try original topic
    explanation = get_concept_explanation(topic)
    if explanation:
        return explanation
    
    # Check for problem-related queries
    if question and function_name:
        return _generate_problem_response(message, question, function_name, user_code)
    
    # Default response
    return generate_default_response(topic)


def _generate_problem_response(
    message: str,
    question: str,
    function_name: str,
    user_code: str
) -> str:
    """Generate response for problem-related queries."""
    message_lower = message.lower()
    
    # Hint request
    if any(p in message_lower for p in ['hint', 'help', 'stuck', 'clue']):
        return f"""💡 **Hint for `{function_name}`:**

Think about:
1. What input does the function receive?
2. What output should it return?
3. What's the simplest approach that would work?

Try breaking it down step by step!"""
    
    # Explain problem
    if any(p in message_lower for p in ['explain', 'what does', 'understand']):
        return f"""📝 **Problem Explanation:**

**Task:** {question}

**Function to implement:** `{function_name}`

**What you need to do:**
1. Read and understand the problem
2. Think about the input and expected output
3. Plan your approach before coding
4. Implement the solution
5. Test with the provided examples"""
    
    # Approach guidance
    if any(p in message_lower for p in ['approach', 'how to', 'strategy']):
        return f"""🎯 **Approach for `{function_name}`:**

**Steps to solve:**
1. **Understand** - What are the inputs? What should you return?
2. **Plan** - Think of the simplest working solution first
3. **Code** - Write clean, readable code
4. **Test** - Try edge cases (empty input, single element, etc.)

**Tip:** Start simple, then optimize if needed!"""
    
    # Default problem-related response
    return f"""🤖 **About `{function_name}`:**

I see you're working on: {question}

**Quick tips:**
- Make sure to use `return`, not `print`
- Check your function name matches exactly
- Handle edge cases

What specific aspect do you need help with?"""


def format_response_with_context(
    response: str,
    context: Optional[str] = None,
    include_footer: bool = True
) -> str:
    """
    Format a response with optional context and footer.
    
    Args:
        response: Main response content
        context: Optional context to prepend
        include_footer: Whether to include helpful footer
        
    Returns:
        Formatted response
    """
    parts = []
    
    if context:
        parts.append(f"*{context}*\n")
    
    parts.append(response)
    
    if include_footer:
        parts.append("\n\n---\n*Ask me anything else about Python!*")
    
    return clean_response_text('\n'.join(parts))

