# tests/test_evaluator.py
"""
Unit tests for the code evaluator module.
Tests security, timeout, and code evaluation functionality.
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from evaluator import (
    evaluate_user_code,
    check_code_security,
    format_runtime_error,
    SAFE_BUILTINS,
    TIMEOUT_SECONDS
)


class TestCodeSecurity:
    """Tests for code security validation."""
    
    def test_safe_code_passes(self):
        """Safe code should pass security check."""
        code = "def add(a, b):\n    return a + b"
        is_safe, msg = check_code_security(code)
        assert is_safe == True
        assert msg == ""
    
    def test_import_os_blocked(self):
        """Import os should be blocked."""
        code = "import os\ndef test(): return os.getcwd()"
        is_safe, msg = check_code_security(code)
        assert is_safe == False
        assert "os" in msg.lower()
    
    def test_import_sys_blocked(self):
        """Import sys should be blocked."""
        code = "import sys\ndef test(): return sys.path"
        is_safe, msg = check_code_security(code)
        assert is_safe == False
        assert "sys" in msg.lower()
    
    def test_eval_blocked(self):
        """eval() should be blocked."""
        code = "def test():\n    return eval('1+1')"
        is_safe, msg = check_code_security(code)
        assert is_safe == False
        assert "eval" in msg.lower()
    
    def test_exec_blocked(self):
        """exec() should be blocked."""
        code = "def test():\n    exec('print(1)')"
        is_safe, msg = check_code_security(code)
        assert is_safe == False
        assert "exec" in msg.lower()
    
    def test_open_blocked(self):
        """open() should be blocked."""
        code = "def test():\n    return open('file.txt')"
        is_safe, msg = check_code_security(code)
        assert is_safe == False
        assert "open" in msg.lower()
    
    def test_dunder_globals_blocked(self):
        """__globals__ access should be blocked."""
        code = "def test():\n    return test.__globals__"
        is_safe, msg = check_code_security(code)
        assert is_safe == False
    
    def test_dunder_init_allowed(self):
        """__init__ should be allowed for class definitions."""
        code = '''class MyClass:
    def __init__(self, value):
        self.value = value'''
        is_safe, msg = check_code_security(code)
        assert is_safe == True


class TestCodeEvaluation:
    """Tests for code evaluation functionality."""
    
    def test_simple_addition(self):
        """Test simple addition function."""
        code = "def add(a, b):\n    return a + b"
        test_cases = [((2, 3), 5), ((10, 20), 30)]
        passed, msg = evaluate_user_code(code, "add", test_cases)
        assert passed == True
    
    def test_list_return(self):
        """Test function returning a list."""
        code = "def get_list(n):\n    return list(range(1, n+1))"
        test_cases = [((3,), [1, 2, 3]), ((5,), [1, 2, 3, 4, 5])]
        passed, msg = evaluate_user_code(code, "get_list", test_cases)
        assert passed == True
    
    def test_wrong_result(self):
        """Test that wrong results are caught."""
        code = "def add(a, b):\n    return a - b"  # Wrong operation
        test_cases = [((2, 3), 5)]
        passed, msg = evaluate_user_code(code, "add", test_cases)
        assert passed == False
        assert "Test Case Failed" in msg or "Expected" in msg
    
    def test_wrong_function_name(self):
        """Test wrong function name detection."""
        code = "def addition(a, b):\n    return a + b"
        test_cases = [((2, 3), 5)]
        passed, msg = evaluate_user_code(code, "add", test_cases)
        assert passed == False
        assert "function" in msg.lower()
    
    def test_syntax_error(self):
        """Test syntax error detection."""
        code = "def add(a, b)\n    return a + b"  # Missing colon
        test_cases = [((2, 3), 5)]
        passed, msg = evaluate_user_code(code, "add", test_cases)
        assert passed == False
        assert "syntax" in msg.lower() or "error" in msg.lower()
    
    def test_no_return_statement(self):
        """Test detection of missing return."""
        code = "def add(a, b):\n    result = a + b"
        test_cases = [((2, 3), 5)]
        passed, msg = evaluate_user_code(code, "add", test_cases)
        assert passed == False
    
    def test_print_instead_of_return(self):
        """Test detection of print instead of return."""
        code = "def add(a, b):\n    print(a + b)"
        test_cases = [((2, 3), 5)]
        passed, msg = evaluate_user_code(code, "add", test_cases)
        assert passed == False
        assert "print" in msg.lower() or "return" in msg.lower()


class TestSafeModules:
    """Tests for safe module availability."""
    
    def test_math_module_available(self):
        """Test that math module is available."""
        code = '''def calculate(n):
    import math
    return math.sqrt(n)'''
        test_cases = [((16,), 4.0), ((25,), 5.0)]
        passed, msg = evaluate_user_code(code, "calculate", test_cases)
        assert passed == True
    
    def test_collections_counter_available(self):
        """Test that collections.Counter is available."""
        code = '''def count_items(items):
    from collections import Counter
    return dict(Counter(items))'''
        test_cases = [((['a', 'b', 'a'],), {'a': 2, 'b': 1})]
        passed, msg = evaluate_user_code(code, "count_items", test_cases)
        assert passed == True
    
    def test_heapq_available(self):
        """Test that heapq is available."""
        code = '''def get_smallest(nums, k):
    import heapq
    return heapq.nsmallest(k, nums)'''
        test_cases = [(([3, 1, 4, 1, 5], 2), [1, 1])]
        passed, msg = evaluate_user_code(code, "get_smallest", test_cases)
        assert passed == True
    
    def test_itertools_available(self):
        """Test that itertools is available."""
        code = '''def get_perms(s):
    from itertools import permutations
    return sorted([''.join(p) for p in permutations(s)])'''
        test_cases = [(('ab',), ['ab', 'ba'])]
        passed, msg = evaluate_user_code(code, "get_perms", test_cases)
        assert passed == True


class TestClassDefinitions:
    """Tests for class definition support."""
    
    def test_simple_class(self):
        """Test that simple class definitions work."""
        code = '''class Counter:
    def __init__(self):
        self.count = 0
    
    def increment(self):
        self.count += 1
        return self.count

def count_to(n):
    c = Counter()
    for _ in range(n):
        c.increment()
    return c.count'''
        test_cases = [((3,), 3), ((5,), 5)]
        passed, msg = evaluate_user_code(code, "count_to", test_cases)
        assert passed == True
    
    def test_class_with_str(self):
        """Test class with __str__ method."""
        code = '''class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __str__(self):
        return f"({self.x}, {self.y})"

def create_point(x, y):
    return str(Point(x, y))'''
        test_cases = [((1, 2), "(1, 2)")]
        passed, msg = evaluate_user_code(code, "create_point", test_cases)
        assert passed == True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

