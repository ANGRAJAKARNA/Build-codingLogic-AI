# assistant/code_analyzer.py
"""
Code analysis, review, and bug detection for the AI assistant.
"""

import re
from typing import List, Dict, Tuple, Optional


# Common coding mistakes and their fixes
COMMON_MISTAKES: Dict[str, Dict[str, str]] = {
    "print_not_return": {
        "pattern": r"print\s*\([^)]*\)\s*$",
        "message": "Using print() instead of return",
        "fix": "Replace print() with return to return the value"
    },
    "missing_return": {
        "pattern": r"^def \w+\([^)]*\):\s*\n(?:(?!return).*\n)*$",
        "message": "Function doesn't have a return statement",
        "fix": "Add a return statement to return your result"
    },
    "assignment_in_condition": {
        "pattern": r"if\s+\w+\s*=\s*[^=]",
        "message": "Using = instead of == in condition",
        "fix": "Use == for comparison, = is for assignment"
    },
    "mutable_default": {
        "pattern": r"def \w+\([^)]*=\s*\[\]",
        "message": "Mutable default argument (list)",
        "fix": "Use None as default and create list inside function"
    },
    "string_concat_in_loop": {
        "pattern": r"for .+:\s*\n\s*\w+\s*\+=\s*['\"]",
        "message": "String concatenation in loop (inefficient)",
        "fix": "Use list.append() and ''.join() for better performance"
    },
}


def detect_common_mistakes(code: str) -> List[Dict[str, str]]:
    """
    Detect common coding mistakes in user code.
    
    Args:
        code: User's code string
        
    Returns:
        List of detected mistakes with messages and fixes
    """
    mistakes = []
    
    # Check for print instead of return
    lines = code.strip().split('\n')
    has_def = any(line.strip().startswith('def ') for line in lines)
    has_return = any('return ' in line for line in lines)
    has_print = any('print(' in line for line in lines)
    
    if has_def and has_print and not has_return:
        mistakes.append({
            "type": "print_not_return",
            "message": "❌ You're using print() instead of return",
            "fix": "💡 Replace print(...) with return ... to return the value"
        })
    
    # Check for missing return
    if has_def and not has_return and not has_print:
        mistakes.append({
            "type": "missing_return",
            "message": "❌ Your function doesn't return anything",
            "fix": "💡 Add a 'return' statement at the end of your function"
        })
    
    # Check for common typos
    typo_patterns = [
        (r'\bprnit\b', 'print'),
        (r'\bretunr\b', 'return'),
        (r'\bdefnition\b', 'definition'),
        (r'\bteh\b', 'the'),
    ]
    for pattern, correct in typo_patterns:
        if re.search(pattern, code, re.IGNORECASE):
            mistakes.append({
                "type": "typo",
                "message": f"❌ Possible typo detected",
                "fix": f"💡 Did you mean '{correct}'?"
            })
    
    # Check for using = instead of ==
    if_assignment = re.search(r'if\s+\w+\s*=\s*[^=\n]', code)
    if if_assignment:
        mistakes.append({
            "type": "assignment_in_condition",
            "message": "❌ Using = instead of == in condition",
            "fix": "💡 Use == for comparison (= is for assignment)"
        })
    
    # Check for infinite loop potential
    while_match = re.search(r'while\s+True\s*:', code)
    if while_match and 'break' not in code:
        mistakes.append({
            "type": "infinite_loop",
            "message": "⚠️ Potential infinite loop",
            "fix": "💡 while True loops need a break condition"
        })
    
    return mistakes


def analyze_code_quality(code: str) -> Dict[str, any]:
    """
    Analyze the quality of user code.
    
    Args:
        code: User's code string
        
    Returns:
        Dict with quality metrics and suggestions
    """
    lines = [l for l in code.split('\n') if l.strip()]
    
    analysis = {
        "line_count": len(lines),
        "has_docstring": '"""' in code or "'''" in code,
        "has_comments": '#' in code,
        "has_type_hints": bool(re.search(r'def \w+\([^)]*:\s*\w+', code)),
        "function_count": len(re.findall(r'^def \w+', code, re.MULTILINE)),
        "class_count": len(re.findall(r'^class \w+', code, re.MULTILINE)),
        "suggestions": []
    }
    
    # Generate suggestions
    if not analysis["has_docstring"]:
        analysis["suggestions"].append("Add a docstring to document your function")
    
    if not analysis["has_comments"] and len(lines) > 10:
        analysis["suggestions"].append("Consider adding comments for complex logic")
    
    # Check line length
    long_lines = [i+1 for i, l in enumerate(code.split('\n')) if len(l) > 80]
    if long_lines:
        analysis["suggestions"].append(f"Lines {long_lines[:3]} exceed 80 characters")
    
    # Check for magic numbers
    magic_numbers = re.findall(r'(?<![0-9\w])(?:[-+]?\d{2,}|[-+]?\d+\.\d+)(?![0-9\w])', code)
    if len(magic_numbers) > 2:
        analysis["suggestions"].append("Consider using named constants instead of magic numbers")
    
    return analysis


def get_code_review(
    code: str,
    problem: str,
    function_name: str,
    execution_time: float
) -> str:
    """
    Generate a code review for successful solutions.
    
    Args:
        code: User's code
        problem: Problem description
        function_name: Function name
        execution_time: Time to solve in seconds
        
    Returns:
        Code review feedback
    """
    analysis = analyze_code_quality(code)
    
    # Determine overall assessment
    if execution_time < 60:
        speed_comment = "⚡ Excellent speed! You solved this quickly."
    elif execution_time < 180:
        speed_comment = "👍 Good timing for this problem."
    else:
        speed_comment = "💪 You persevered and got it done!"
    
    # Build review
    review_parts = [
        f"## 📝 Code Review for `{function_name}`\n",
        f"✅ **Solution accepted!**\n",
        f"{speed_comment}\n"
    ]
    
    # Strengths
    strengths = []
    if analysis["has_docstring"]:
        strengths.append("Good documentation with docstring")
    if analysis["has_comments"]:
        strengths.append("Clear comments explaining logic")
    if analysis["has_type_hints"]:
        strengths.append("Using type hints (great practice!)")
    if analysis["line_count"] < 20:
        strengths.append("Concise solution")
    
    if strengths:
        review_parts.append("\n**Strengths:**")
        for s in strengths:
            review_parts.append(f"• {s}")
    
    # Suggestions
    if analysis["suggestions"]:
        review_parts.append("\n**Suggestions for improvement:**")
        for s in analysis["suggestions"]:
            review_parts.append(f"• {s}")
    
    return '\n'.join(review_parts)


def get_bug_hint(
    code: str,
    error_message: str,
    problem: str,
    function_name: str
) -> str:
    """
    Generate debugging hints based on error messages.
    
    Args:
        code: User's code
        error_message: The error that occurred
        problem: Problem description
        function_name: Expected function name
        
    Returns:
        Debugging hint
    """
    error_lower = error_message.lower()
    
    # Check for common mistakes first
    mistakes = detect_common_mistakes(code)
    if mistakes:
        first_mistake = mistakes[0]
        return f"{first_mistake['message']}\n\n{first_mistake['fix']}"
    
    # Error-specific hints
    if "syntaxerror" in error_lower or "syntax error" in error_lower:
        return """🔍 **Syntax Error Detected**

Common causes:
• Missing colon `:` after `def`, `if`, `for`, `while`
• Unmatched parentheses `()`, brackets `[]`, or braces `{}`
• Missing quotes around strings
• Incorrect indentation

Check the line number mentioned in the error!"""
    
    if "nameerror" in error_lower:
        # Try to extract the variable name
        match = re.search(r"name '(\w+)'", error_message)
        var_name = match.group(1) if match else "the variable"
        return f"""🔍 **Name Error: {var_name} is not defined**

This means you're using a variable before defining it.

**Check for:**
• Typos in variable names
• Variable defined inside a different scope
• Using a function before defining it
• Missing import statement"""
    
    if "typeerror" in error_lower:
        return """🔍 **Type Error Detected**

You're trying to do an operation with incompatible types.

**Common causes:**
• Adding string + int (use str() or int() to convert)
• Calling a non-callable object
• Wrong number of arguments to a function
• Using None where a value is expected"""
    
    if "indexerror" in error_lower:
        return """🔍 **Index Error: List index out of range**

You're trying to access an index that doesn't exist.

**Check:**
• List might be empty
• Loop might go past list length
• Remember: indices start at 0, last index is len(list)-1
• Use `if i < len(list)` before accessing"""
    
    if "keyerror" in error_lower:
        return """🔍 **Key Error: Dictionary key not found**

**Solutions:**
• Use `dict.get(key, default)` to avoid errors
• Check if key exists: `if key in dict:`
• Initialize with `defaultdict` from collections"""
    
    if "attributeerror" in error_lower:
        return """🔍 **Attribute Error**

You're accessing a method or attribute that doesn't exist.

**Check:**
• Variable might be None
• Typo in method name
• Wrong type (e.g., calling .append() on a string)"""
    
    if "test case failed" in error_lower or "expected" in error_lower:
        return f"""🔍 **Test Case Failed**

Your function returned a different value than expected.

**Debug steps:**
1. Print your intermediate values
2. Check the expected output format
3. Handle edge cases (empty input, single element)
4. Make sure you're using `return`, not `print`"""
    
    # Generic hint
    return f"""🔍 **Debugging `{function_name}`**

Error: {error_message[:100]}...

**General debugging tips:**
1. Read the error message carefully
2. Check the line number mentioned
3. Add print statements to see values
4. Test with simple inputs first
5. Check for common mistakes (indentation, typos)"""


def get_smart_hint(
    code: str,
    problem: str,
    function_name: str,
    available_hints: List[str],
    hint_level: int
) -> str:
    """
    Generate a smart, contextual hint based on user's code and progress.
    
    Args:
        code: User's current code
        problem: Problem description
        function_name: Function to implement
        available_hints: List of predefined hints
        hint_level: Current hint level
        
    Returns:
        Smart hint based on context
    """
    # Analyze code state
    has_function = f"def {function_name}" in code
    has_return = "return" in code
    has_loop = any(kw in code for kw in ["for ", "while "])
    is_empty = code.strip().endswith("pass") or len(code.strip().split('\n')) <= 3
    
    # Generate contextual hint
    if not has_function:
        return f"💡 **First step:** Start by defining your function:\n```python\ndef {function_name}(...):\n    # your code here\n```"
    
    if is_empty:
        if available_hints and hint_level <= len(available_hints):
            return f"💡 **Hint {hint_level}:** {available_hints[hint_level - 1]}"
        return "💡 **Think about:** What's the first thing your function needs to do with the input?"
    
    if not has_return:
        return "💡 **Remember:** Your function needs to `return` the result, not `print` it!"
    
    # Check for common mistakes
    mistakes = detect_common_mistakes(code)
    if mistakes:
        return f"💡 **Tip:** {mistakes[0]['fix']}"
    
    # Use predefined hints based on level
    if available_hints and hint_level <= len(available_hints):
        hint = available_hints[hint_level - 1]
        remaining = len(available_hints) - hint_level
        suffix = f"\n\n*{remaining} more hints available*" if remaining > 0 else "\n\n*Final hint!*"
        return f"💡 **Hint {hint_level}:** {hint}{suffix}"
    
    # Advanced hint
    return f"""💡 **Review your solution:**

1. Does your function handle edge cases?
   - Empty input
   - Single element
   - Negative numbers (if applicable)

2. Is your logic correct for all test cases?

3. Are you returning the correct type?"""

