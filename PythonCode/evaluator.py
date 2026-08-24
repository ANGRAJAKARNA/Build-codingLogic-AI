# evaluator.py
"""
Secure code evaluator with:
- Sandboxed execution (restricted builtins)
- Timeout protection (prevents infinite loops)
- Better error messages with helpful suggestions
"""

import ast
import threading
import multiprocessing
import traceback
from typing import Tuple, List, Any

# Execution timeout in seconds
TIMEOUT_SECONDS = 5

# Reject absurdly long submissions before even spawning a sandbox process
MAX_CODE_LENGTH = 10000

# How many sandboxed submissions may run at once, app-wide. Streamlit Cloud
# runs one shared process for every visitor, so this caps how many forked
# child processes can exist simultaneously — excess submissions simply wait
# their turn rather than letting the container fork unboundedly.
MAX_CONCURRENT_SANDBOXES = 4
_SANDBOX_SEMAPHORE = threading.Semaphore(MAX_CONCURRENT_SANDBOXES)

# Import safe modules that users might need
import math
import collections
import heapq
import itertools
import functools
import string
import operator
import bisect
import re

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
    'object': object,
    
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
    'id': id,
    'isinstance': isinstance,
    'issubclass': issubclass,
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
    'callable': callable,
    'ascii': ascii,
    'input': lambda *args: "",  # Safe no-op input
    
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
    'RuntimeError': RuntimeError,
    'AttributeError': AttributeError,
    'RecursionError': RecursionError,
    'OverflowError': OverflowError,
    'AssertionError': AssertionError,
    
    # Safe modules - commonly needed for algorithm problems
    'math': math,
    'collections': collections,
    'heapq': heapq,
    'itertools': itertools,
    'functools': functools,
    'string': string,
    'operator': operator,
    'bisect': bisect,
    're': re,
    
    # Commonly used from collections
    'Counter': collections.Counter,
    'defaultdict': collections.defaultdict,
    'deque': collections.deque,
    'OrderedDict': collections.OrderedDict,
    'namedtuple': collections.namedtuple,
    
    # Commonly used from functools
    'reduce': functools.reduce,
    'lru_cache': functools.lru_cache,
    'cache': getattr(functools, 'cache', functools.lru_cache(maxsize=None)),
    
    # Commonly used from itertools
    'permutations': itertools.permutations,
    'combinations': itertools.combinations,
    'product': itertools.product,
    'chain': itertools.chain,
    'groupby': itertools.groupby,
    
    # Commonly used from heapq
    'heappush': heapq.heappush,
    'heappop': heapq.heappop,
    'heapify': heapq.heapify,
    'nlargest': heapq.nlargest,
    'nsmallest': heapq.nsmallest,
}

# The modules user code is allowed to `import`/`from ... import ...`.
# This is the single source of truth for both the AST-based security check
# (which validates import statements before execution) and the restricted
# __import__ shim below (which actually serves them at runtime) — kept as
# one dict so the two can't drift out of sync with each other.
SAFE_MODULES = {
    'math': math, 'collections': collections, 'heapq': heapq,
    'itertools': itertools, 'functools': functools, 'string': string,
    'operator': operator, 'bisect': bisect, 're': re,
}


def _safe_import(name, globals=None, locals=None, fromlist=(), level=0):
    """
    Restricted __import__ used inside the sandbox. Only ever returns one of
    the pre-imported SAFE_MODULES objects — never touches the real
    importlib/filesystem — so `import math` / `from collections import
    Counter` work as statements without opening a real import path.
    """
    root = name.split('.')[0]
    if root not in SAFE_MODULES:
        raise ImportError(f"Import of '{name}' is not allowed in this sandbox")
    return SAFE_MODULES[root]


SAFE_BUILTINS['__import__'] = _safe_import

# Dunder attribute names user code is allowed to access (e.g. `super().__init__()`,
# defining `__str__`, comparing with `__eq__`). Everything else starting and
# ending with `__` is blocked. This is deliberately an allowlist rather than
# a denylist — a denylist has to enumerate every dangerous dunder in advance
# and reliably misses some (e.g. `__mro__` was never blocked by the old
# regex-based check); an allowlist can't leak what it doesn't name.
SAFE_DUNDER_ATTRS = {
    '__init__', '__str__', '__repr__', '__len__', '__eq__', '__ne__',
    '__lt__', '__le__', '__gt__', '__ge__', '__hash__', '__iter__', '__next__',
    '__contains__', '__getitem__', '__setitem__', '__delitem__',
    '__add__', '__sub__', '__mul__', '__truediv__', '__floordiv__', '__mod__',
    '__pow__', '__neg__', '__pos__', '__abs__', '__bool__', '__call__',
    '__enter__', '__exit__', '__name__', '__doc__',
}

# Bare-name calls that are never allowed, even though most of these names
# aren't in SAFE_BUILTINS anyway (so calling them would already NameError) —
# blocking them at the security-check stage gives a clear, specific message
# instead of a confusing NameError. Deliberately excludes 'input' — that one
# IS in SAFE_BUILTINS on purpose, as a safe no-op (see above).
DENYLISTED_CALLS = {
    'eval', 'exec', 'compile', 'globals', 'locals', 'getattr', 'setattr',
    'delattr', 'vars', '__import__', 'open',
}

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
    },
    'recursion_error': {
        'message': "❌ Maximum Recursion Depth Exceeded",
        'suggestion': "💡 Your recursion doesn't have a proper base case or recurses too deeply. Add a base case!"
    },
    'attribute_error': {
        'message': "❌ Attribute Error",
        'suggestion': "💡 You're accessing a method or property that doesn't exist on this object"
    },
    'key_error': {
        'message': "❌ Key Error",
        'suggestion': "💡 The key you're trying to access doesn't exist in the dictionary. Use .get() or check with 'in'"
    },
    'zero_division': {
        'message': "❌ Division by Zero",
        'suggestion': "💡 You're dividing by zero. Add a check to prevent this"
    },
    'overflow_error': {
        'message': "❌ Overflow Error",
        'suggestion': "💡 The number is too large to handle. Consider using a different approach"
    },
    'assertion_error': {
        'message': "❌ Assertion Failed",
        'suggestion': "💡 An assertion in your code failed. Check your logic"
    },
    'value_error': {
        'message': "❌ Value Error",
        'suggestion': "💡 A function received an argument with the right type but inappropriate value"
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
    Check code for dangerous operations by walking its parsed AST, rather
    than pattern-matching the raw text. This closes gaps a regex prefilter
    has by construction: `from os import getcwd` and `importlib.import_module(...)`
    both defeated the old `\\bimport\\s+os\\b`-style patterns purely on word
    order, and a regex can also false-positive on the same text appearing
    inside a comment or string literal. Operating on the parsed tree avoids
    both problems.

    Returns (is_safe, error_message). If the code doesn't even parse, this
    reports safe — the real SyntaxError with a nicely formatted message is
    produced downstream by compile(), which is a better place for it.
    """
    try:
        tree = ast.parse(code, mode='exec')
    except (SyntaxError, ValueError):
        return True, ""

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                root = alias.name.split('.')[0]
                if root not in SAFE_MODULES:
                    return False, f"🔒 Security Error: Importing '{alias.name}' is not allowed"

        elif isinstance(node, ast.ImportFrom):
            root = (node.module or '').split('.')[0]
            if node.level or root not in SAFE_MODULES:
                what = node.module or '(relative import)'
                return False, f"🔒 Security Error: Importing '{what}' is not allowed"

        elif isinstance(node, ast.Attribute):
            attr = node.attr
            if attr.startswith('__') and attr.endswith('__') and attr not in SAFE_DUNDER_ATTRS:
                return False, f"🔒 Security Error: Accessing '{attr}' is not allowed"

        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id in DENYLISTED_CALLS:
                return False, f"🔒 Security Error: Using '{node.func.id}()' is not allowed"

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


def _get_mp_context():
    """
    Prefer 'fork' — cheap copy-on-write with no re-pickling of the parent's
    state, and the production target (Streamlit Community Cloud) is Linux.
    Falls back to 'spawn', the only option on Windows, for local dev.
    """
    try:
        return multiprocessing.get_context('fork')
    except ValueError:
        return multiprocessing.get_context('spawn')


def _classify_exception(error: Exception) -> str:
    """Map a caught exception to a COMMON_MISTAKES key by its real type
    (instead of substring-matching str(error), which only ever recognized
    NameError/TypeError/IndexError and left several already-written
    COMMON_MISTAKES entries permanently unreachable)."""
    return {
        'NameError': 'name_error', 'TypeError': 'type_error',
        'IndexError': 'index_error', 'KeyError': 'key_error',
        'AttributeError': 'attribute_error', 'ZeroDivisionError': 'zero_division',
        'OverflowError': 'overflow_error', 'AssertionError': 'assertion_error',
        'ValueError': 'value_error', 'RecursionError': 'recursion_error',
    }.get(type(error).__name__, 'runtime')


def _sandboxed_worker(code, function_name, test_cases, stop_on_first_failure, conn):
    """
    Runs inside the forked/spawned child process — this is the actual
    untrusted-code execution boundary. Sends exactly one (status, payload)
    message back over `conn` before exiting. Never lets an unexpected
    failure crash the process silently; it's always turned into a normal
    result message instead.
    """
    try:
        try:
            import resource  # POSIX only; no-op on Windows dev machines
            resource.setrlimit(resource.RLIMIT_CPU, (TIMEOUT_SECONDS, TIMEOUT_SECONDS + 1))
            resource.setrlimit(resource.RLIMIT_AS, (256 * 1024 * 1024, 256 * 1024 * 1024))
        except Exception:
            pass

        printed_output = []
        safe_env = {'__builtins__': SAFE_BUILTINS.copy()}

        def capture_print(*args, **kwargs):
            printed_output.append(' '.join(map(str, args)))

        safe_env['print'] = capture_print

        try:
            compiled = compile(code, '<user_code>', 'exec')
            exec(compiled, safe_env, safe_env)
        except IndentationError as e:
            conn.send(('indentation_error', f"{COMMON_MISTAKES['indentation_error']['message']}: {e}\n\n{COMMON_MISTAKES['indentation_error']['suggestion']}"))
            return
        except SyntaxError as e:
            conn.send(('syntax_error', format_syntax_error(e, code)))
            return
        except Exception as e:
            conn.send(('define_error', f"❌ Error while defining your code:\n\n`{type(e).__name__}: {e}`\n\n💡 Check your function definition for errors"))
            return

        if function_name not in safe_env:
            candidates = [k for k in safe_env.keys()
                          if callable(safe_env.get(k)) and not k.startswith('_') and k != 'print']
            conn.send(('function_not_found', candidates))
            return

        func = safe_env[function_name]
        results = []

        for inputs, expected in test_cases:
            printed_output.clear()
            try:
                actual = func(*inputs)
                # Only treat a None return as suspicious ("forgot to return" /
                # "printed instead of returning") when None ISN'T actually the
                # correct answer — otherwise a problem whose valid answer is
                # None (e.g. "return None when there's no second-largest
                # element") would always be misreported as buggy even when
                # it's exactly correct.
                if expected is not None and actual is None and printed_output:
                    case_status = "print_instead_of_return"
                elif expected is not None and actual is None and not printed_output:
                    case_status = "no_return"
                elif actual != expected:
                    case_status = "wrong_value"
                else:
                    case_status = "passed"
                results.append({
                    "inputs": inputs, "expected": expected, "actual": actual,
                    "passed": case_status == "passed", "printed": list(printed_output),
                    "case_status": case_status, "error_type": None, "error_str": None,
                })
            except Exception as e:
                results.append({
                    "inputs": inputs, "expected": expected, "actual": None, "passed": False,
                    "printed": list(printed_output), "case_status": "error",
                    "error_type": _classify_exception(e), "error_str": str(e),
                })

            if results[-1]["case_status"] != "passed" and stop_on_first_failure:
                break

        conn.send(('ok', results))

    except Exception as e:
        try:
            conn.send(('define_error', f"❌ Unexpected sandbox error: {type(e).__name__}: {e}"))
        except Exception:
            pass
    finally:
        try:
            conn.close()
        except Exception:
            pass


def run_test_cases(code: str, function_name: str, test_cases: List[Tuple],
                    stop_on_first_failure: bool = True) -> Tuple[str, Any]:
    """
    Compile and execute user code, then run it against test_cases.

    This is the single shared sandbox entry point — the canonical place
    all callers (Practice mode's Run/Submit, the test-results table, and
    the AI-chat code runner) should go through instead of each hand-rolling
    their own exec() with a slightly different builtins whitelist.

    Args:
        stop_on_first_failure: True (default) matches evaluate_user_code()'s
            existing pass/fail semantics — stop at the first non-passing case.
            False runs every test case regardless of earlier failures, for
            UIs that want to display a full per-case results table.

    Returns (status, payload):
      'security_error'    -> payload: str (message)
      'syntax_error'       -> payload: str (formatted message)
      'indentation_error'  -> payload: str (formatted message)
      'define_error'       -> payload: str (formatted message)
      'timeout'             -> payload: str (formatted message) — the sandbox
                              process was killed for exceeding TIMEOUT_SECONDS
                              (applies to the whole submission: compiling plus
                              every test case run, not per test case)
      'function_not_found' -> payload: List[str] (candidate function names found)
      'ok'                 -> payload: List[dict], one per test case run:
          {inputs, expected, actual, passed, printed, case_status, error_type, error_str}
          case_status is one of: 'passed', 'print_instead_of_return', 'no_return',
                                  'wrong_value', 'error'
    """
    is_safe, security_error = check_code_security(code)
    if not is_safe:
        return 'security_error', security_error

    if len(code) > MAX_CODE_LENGTH:
        return 'define_error', f"❌ Code too long (max {MAX_CODE_LENGTH:,} characters)"

    if not isinstance(test_cases, list) or not all(
        isinstance(tc, (tuple, list)) and len(tc) == 2 for tc in test_cases
    ):
        return 'define_error', "❌ Internal error: malformed test cases"

    ctx = _get_mp_context()
    parent_conn, child_conn = ctx.Pipe(duplex=False)
    proc = ctx.Process(
        target=_sandboxed_worker,
        args=(code, function_name, test_cases, stop_on_first_failure, child_conn),
        daemon=True,
    )

    status, payload = None, None
    with _SANDBOX_SEMAPHORE:
        try:
            proc.start()
            child_conn.close()  # only the child should hold the writable end
            if parent_conn.poll(TIMEOUT_SECONDS):
                try:
                    status, payload = parent_conn.recv()
                except (EOFError, OSError):
                    status, payload = None, None
        finally:
            # Guaranteed reclaim: unlike a Thread, a Process can actually be
            # killed, so a runaway submission no longer burns CPU forever
            # after we've already told the user it timed out.
            if proc.is_alive():
                proc.terminate()
                proc.join(1)
            if proc.is_alive():
                proc.kill()
                proc.join(1)
            parent_conn.close()

    if status is None:
        return 'timeout', format_runtime_error(
            TimeoutException(f"Execution exceeded {TIMEOUT_SECONDS} seconds"), 'timeout'
        )

    return status, payload


def evaluate_user_code(code: str, function_name: str, test_cases: List[Tuple]) -> Tuple[bool, str]:
    """
    Evaluate user code against test cases.

    Args:
        code: User's Python code as string
        function_name: Expected function name to call
        test_cases: List of (inputs, expected_output) tuples

    Returns:
        (passed, message) tuple

    Thin wrapper around run_test_cases() that reduces the structured
    per-test-case results to the (bool, str) contract existing callers expect.
    """
    status, payload = run_test_cases(code, function_name, test_cases)

    if status in ('security_error', 'syntax_error', 'indentation_error', 'define_error', 'timeout'):
        return False, payload

    if status == 'function_not_found':
        candidates = payload
        msg = f"{COMMON_MISTAKES['wrong_function_name']['message']}\n\n"
        msg += f"❌ Expected function: `{function_name}`\n"
        if candidates:
            msg += f"📝 Found: `{', '.join(candidates)}`\n"
        msg += f"\n{COMMON_MISTAKES['wrong_function_name']['suggestion']}"
        return False, msg

    # status == 'ok'
    results = payload
    last = results[-1]

    if last["case_status"] == "error":
        if last["error_type"] == "timeout":
            return False, last["error_str"]
        return False, format_runtime_error(Exception(last["error_str"]), last["error_type"])

    if last["case_status"] == "print_instead_of_return":
        return False, f"{COMMON_MISTAKES['print_instead_of_return']['message']}\n\n{COMMON_MISTAKES['print_instead_of_return']['suggestion']}"

    if last["case_status"] == "no_return":
        return False, f"{COMMON_MISTAKES['no_return']['message']}\n\n{COMMON_MISTAKES['no_return']['suggestion']}"

    if last["case_status"] == "wrong_value":
        return False, format_test_failure(last["inputs"], last["expected"], last["actual"])

    return True, f"✅ All {len(results)} test cases passed!"


def _snippet_worker(code, conn):
    """Child-process body for run_snippet() — same timeout/kill guarantees
    as _sandboxed_worker, just without the function-name/test-case machinery."""
    try:
        try:
            import resource
            resource.setrlimit(resource.RLIMIT_CPU, (TIMEOUT_SECONDS, TIMEOUT_SECONDS + 1))
            resource.setrlimit(resource.RLIMIT_AS, (256 * 1024 * 1024, 256 * 1024 * 1024))
        except Exception:
            pass

        printed_output = []
        safe_env = {'__builtins__': SAFE_BUILTINS.copy()}

        def capture_print(*args, **kwargs):
            printed_output.append(' '.join(str(a) for a in args))

        safe_env['print'] = capture_print

        try:
            compiled = compile(code, '<user_code>', 'exec')
            exec(compiled, safe_env, safe_env)
            conn.send({'output': '\n'.join(printed_output), 'error': '', 'success': True})
        except Exception as e:
            conn.send({'output': '\n'.join(printed_output), 'error': f"{type(e).__name__}: {e}", 'success': False})
    except Exception as e:
        try:
            conn.send({'output': '', 'error': f"{type(e).__name__}: {e}", 'success': False})
        except Exception:
            pass
    finally:
        try:
            conn.close()
        except Exception:
            pass


def run_snippet(code: str) -> dict:
    """
    Execute an arbitrary code snippet (no expected function/test cases) —
    used for running standalone code blocks (e.g. from AI chat responses).

    Reuses the same security check, builtins whitelist, and killable-process
    timeout as run_test_cases(), unlike the ad-hoc, unvetted, untimed exec()
    blocks this replaces.

    Returns dict with 'output', 'error', and 'success' keys.
    """
    is_safe, security_error = check_code_security(code)
    if not is_safe:
        return {'output': '', 'error': security_error, 'success': False}

    if len(code) > MAX_CODE_LENGTH:
        return {'output': '', 'error': f"Code too long (max {MAX_CODE_LENGTH:,} characters)", 'success': False}

    ctx = _get_mp_context()
    parent_conn, child_conn = ctx.Pipe(duplex=False)
    proc = ctx.Process(target=_snippet_worker, args=(code, child_conn), daemon=True)

    result = None
    with _SANDBOX_SEMAPHORE:
        try:
            proc.start()
            child_conn.close()
            if parent_conn.poll(TIMEOUT_SECONDS):
                try:
                    result = parent_conn.recv()
                except (EOFError, OSError):
                    result = None
        finally:
            if proc.is_alive():
                proc.terminate()
                proc.join(1)
            if proc.is_alive():
                proc.kill()
                proc.join(1)
            parent_conn.close()

    if result is None:
        return {'output': '', 'error': f"Execution exceeded {TIMEOUT_SECONDS} seconds", 'success': False}

    return result
