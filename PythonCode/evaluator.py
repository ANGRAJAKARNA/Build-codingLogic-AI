# evaluator.py
"""
Secure code evaluator with:
- Sandboxed execution (restricted builtins)
- Timeout protection (prevents infinite loops)
- Better error messages with helpful suggestions
"""

import threading
import traceback
import re
from typing import Tuple, List, Any

# Execution timeout in seconds
TIMEOUT_SECONDS = 5

# Safe builtins whitelist - only allow safe operations
SAFE_BUILTINS = {
    # Types
    'bool': bool,
    'int': int,
    'float': float,
    'str': str,
    'list': list,
    'dict': dict,
    'set': set,
    'tuple': tuple,
    'frozenset': frozenset,
    'bytes': bytes,
    'bytearray': bytearray,
    'complex': complex,
    
    # Functions
    'abs': abs,
    'all': all,
    'any': any,
    'bin': bin,
    'chr': chr,
    'divmod': divmod,
    'enumerate': enumerate,
    'filter': filter,
    'format': format,
    'hash': hash,
    'hex': hex,
    'isinstance': isinstance,
    'iter': iter,
    'len': len,
    'map': map,
    'max': max,
    'min': min,
    'next': next,
    'oct': oct,
    'ord': ord,
    'pow': pow,
    'range': range,
    'repr': repr,
    'reversed': reversed,
    'round': round,
    'slice': slice,
    'sorted': sorted,
    'sum': sum,
    'zip': zip,
    
    # Constants
    'True': True,
    'False': False,
    'None': None,
    
    # Class support (needed for defining classes)
    '__build_class__': __builtins__.__build_class__ if hasattr(__builtins__, '__build_class__') else __builtins__['__build_class__'],
    '__name__': '__user_code__',
    
    # Exceptions (needed for try/except in user code)
    'Exception': Exception,
    'ValueError': ValueError,
    'TypeError': TypeError,
    'IndexError': IndexError,
    'KeyError': KeyError,
    'ZeroDivisionError': ZeroDivisionError,
    'StopIteration': StopIteration,
}

# Dangerous patterns to detect
DANGEROUS_PATTERNS = [
    (r'\bimport\s+os\b', "Importing 'os' module is not allowed"),
    (r'\bimport\s+sys\b', "Importing 'sys' module is not allowed"),
    (r'\bimport\s+subprocess\b', "Importing 'subprocess' module is not allowed"),
    (r'\bopen\s*\(', "File operations with 'open()' are not allowed"),
    (r'\beval\s*\(', "Using 'eval()' is not allowed"),
    (r'\bexec\s*\(', "Using 'exec()' is not allowed"),
    (r'\b__import__\s*\(', "Using '__import__()' is not allowed"),
    (r'\bcompile\s*\(', "Using 'compile()' is not allowed"),
    (r'\bglobals\s*\(', "Using 'globals()' is not allowed"),
    (r'\blocals\s*\(', "Using 'locals()' is not allowed"),
    (r'\bgetattr\s*\(', "Using 'getattr()' is not allowed"),
    (r'\bsetattr\s*\(', "Using 'setattr()' is not allowed"),
    (r'\bdelattr\s*\(', "Using 'delattr()' is not allowed"),
    # Allow safe dunder methods (__init__, __str__, __len__, etc.) but block dangerous ones
    (r'\.__class__', "Accessing '__class__' is not allowed"),
    (r'\.__bases__', "Accessing '__bases__' is not allowed"),
    (r'\.__subclasses__', "Accessing '__subclasses__' is not allowed"),
    (r'\.__code__', "Accessing '__code__' is not allowed"),
    (r'\.__globals__', "Accessing '__globals__' is not allowed"),
    (r'\.__builtins__', "Accessing '__builtins__' is not allowed"),
]

# Common mistakes and their suggestions
COMMON_MISTAKES = {
    'print_instead_of_return': {
        'message': "❌ You're using print() instead of return",
        'suggestion': "💡 Replace print(...) with return ... to return the value"
    },
    'no_return': {
        'message': "❌ Your function doesn't return anything",
        'suggestion': "💡 Add a 'return' statement at the end of your function"
    },
    'wrong_function_name': {
        'message': "❌ Function name doesn't match the required name",
        'suggestion': "💡 Make sure your function is named exactly as shown in the template"
    },
    'indentation_error': {
        'message': "❌ Indentation Error",
        'suggestion': "💡 Check that your code uses consistent spaces (4 spaces per indent level)"
    },
    'syntax_error': {
        'message': "❌ Syntax Error",
        'suggestion': "💡 Check for missing colons, parentheses, or quotes"
    },
    'name_error': {
        'message': "❌ Undefined Variable",
        'suggestion': "💡 Make sure all variables are defined before use"
    },
    'type_error': {
        'message': "❌ Type Error",
        'suggestion': "💡 Check that you're using the correct data types for operations"
    },
    'index_error': {
        'message': "❌ Index Out of Range",
        'suggestion': "💡 Check your loop bounds and list indices"
    },
    'timeout': {
        'message': "❌ Time Limit Exceeded",
        'suggestion': "💡 Your code took too long. Check for infinite loops or optimize your solution"
    }
}


class TimeoutException(Exception):
    """Raised when code execution exceeds time limit."""
    pass


class SecurityException(Exception):
    """Raised when code contains dangerous operations."""
    pass


def check_code_security(code: str) -> Tuple[bool, str]:
    """
    Check code for dangerous patterns.
    Returns (is_safe, error_message).
    """
    for pattern, message in DANGEROUS_PATTERNS:
        if re.search(pattern, code):
            return False, f"🔒 Security Error: {message}"
    return True, ""


def format_syntax_error(error: SyntaxError, code: str) -> str:
    """Format syntax error with line highlighting."""
    lines = code.split('\n')
    line_no = error.lineno if error.lineno else 1
    
    # Get context lines
    start = max(0, line_no - 2)
    end = min(len(lines), line_no + 1)
    
    result = [COMMON_MISTAKES['syntax_error']['message']]
    result.append(f"\n📍 Error at line {line_no}: {error.msg}")
    result.append("\n```")
    
    for i in range(start, end):
        prefix = "→ " if i == line_no - 1 else "  "
        result.append(f"{prefix}{i + 1}: {lines[i]}")
    
    result.append("```")
    result.append(f"\n{COMMON_MISTAKES['syntax_error']['suggestion']}")
    
    return '\n'.join(result)


def format_runtime_error(error: Exception, error_type: str) -> str:
    """Format runtime error with helpful message."""
    mistake_info = COMMON_MISTAKES.get(error_type, {
        'message': f"❌ {type(error).__name__}",
        'suggestion': "💡 Check your code logic and try again"
    })
    
    return f"{mistake_info['message']}: {str(error)}\n\n{mistake_info['suggestion']}"


def format_test_failure(inputs: tuple, expected: Any, actual: Any) -> str:
    """Format test case failure with diff."""
    result = ["❌ Test Case Failed\n"]
    result.append(f"📥 **Input:** `{inputs}`")
    result.append(f"✅ **Expected:** `{expected}`")
    result.append(f"❌ **Got:** `{actual}`")
    
    # Add type info if types differ
    if type(expected) != type(actual):
        result.append(f"\n⚠️ **Type mismatch:** Expected `{type(expected).__name__}`, got `{type(actual).__name__}`")
        result.append("💡 Make sure you're returning the correct data type")
    
    return '\n'.join(result)


def run_with_timeout(func, args, timeout: int) -> Tuple[Any, bool, str]:
    """
    Run a function with timeout.
    Returns (result, success, error_message).
    """
    result = [None]
    error = [None]
    completed = [False]
    
    def target():
        try:
            result[0] = func(*args)
            completed[0] = True
        except Exception as e:
            error[0] = e
    
    thread = threading.Thread(target=target)
    thread.daemon = True
    thread.start()
    thread.join(timeout)
    
    if thread.is_alive():
        return None, False, format_runtime_error(
            TimeoutException(f"Execution exceeded {timeout} seconds"),
            'timeout'
        )
    
    if error[0]:
        return None, False, str(error[0])
    
    return result[0], completed[0], ""


def evaluate_user_code(code: str, function_name: str, test_cases: List[Tuple]) -> Tuple[bool, str]:
    """
    Evaluate user code against test cases.
    
    Args:
        code: User's Python code as string
        function_name: Expected function name to call
        test_cases: List of (inputs, expected_output) tuples
    
    Returns:
        (passed, message) tuple
    """
    printed_output = []
    
    # Security check first
    is_safe, security_error = check_code_security(code)
    if not is_safe:
        return False, security_error
    
    # Create restricted environment
    safe_env = {'__builtins__': SAFE_BUILTINS.copy()}
    
    # Add print capture
    def capture_print(*args, **kwargs):
        printed_output.append(' '.join(map(str, args)))
    
    safe_env['print'] = capture_print
    
    # Try to compile and execute code
    try:
        # Compile first to catch syntax errors with good messages
        compiled = compile(code, '<user_code>', 'exec')
        exec(compiled, safe_env, safe_env)
    
    except SyntaxError as e:
        return False, format_syntax_error(e, code)
    
    except IndentationError as e:
        return False, f"{COMMON_MISTAKES['indentation_error']['message']}: {e}\n\n{COMMON_MISTAKES['indentation_error']['suggestion']}"

    except Exception as e:
        return False, f"❌ Error while defining your code:\n\n`{type(e).__name__}: {e}`\n\n💡 Check your function definition for errors"
    
    # Check if function exists
    if function_name not in safe_env:
        # Try to find similar function names
        user_functions = [k for k in safe_env.keys() if callable(safe_env.get(k)) and not k.startswith('_')]
        
        msg = f"{COMMON_MISTAKES['wrong_function_name']['message']}\n\n"
        msg += f"❌ Expected function: `{function_name}`\n"
        
        if user_functions:
            msg += f"📝 Found: `{', '.join(user_functions)}`\n"
        
        msg += f"\n{COMMON_MISTAKES['wrong_function_name']['suggestion']}"
        return False, msg
    
    func = safe_env[function_name]
    
    # Run test cases
    for i, (inputs, expected) in enumerate(test_cases):
        printed_output.clear()
        
        # Run with timeout
        result, success, error_msg = run_with_timeout(func, inputs, TIMEOUT_SECONDS)
        
        if not success:
            if "exceeded" in error_msg.lower():
                return False, error_msg
            
            # Determine error type
            error_type = 'runtime'
            if 'NameError' in error_msg:
                error_type = 'name_error'
            elif 'TypeError' in error_msg:
                error_type = 'type_error'
            elif 'IndexError' in error_msg:
                error_type = 'index_error'
            
            return False, format_runtime_error(Exception(error_msg), error_type)
        
        # Check for print-only solution
        if result is None and printed_output:
            return False, f"{COMMON_MISTAKES['print_instead_of_return']['message']}\n\n{COMMON_MISTAKES['print_instead_of_return']['suggestion']}"
        
        # Check for no return
        if result is None and not printed_output:
            return False, f"{COMMON_MISTAKES['no_return']['message']}\n\n{COMMON_MISTAKES['no_return']['suggestion']}"
        
        # Compare result
        if result != expected:
            return False, format_test_failure(inputs, expected, result)
    
    # All tests passed!
    passed_count = len(test_cases)
    return True, f"✅ All {passed_count} test cases passed!"
