# builtin_assistant.py
"""
Advanced Built-in AI Assistant - Works Without API, Enhanced With API
Comprehensive Python tutor with pattern matching, code analysis,
learning recommendations, interview preparation, and PDF knowledge base.

When GROQ_API_KEY is set, uses Groq AI for enhanced responses.
When no API key, uses local pattern matching and PDF knowledge base.
"""

import os
import re
import random
from typing import Dict, List, Optional, Tuple, Any

# =============================================================================
# SELF-LEARNING MODULE INTEGRATION
# =============================================================================

LEARNING_AVAILABLE = False
_smart_matcher = None

# Per-visitor learning-module caches. Streamlit Cloud runs one shared
# process for every visitor, so — like learning_memory.py's own instance
# cache — these are keyed by visitor_id instead of being single globals,
# otherwise every visitor's chat memory and feedback would bleed into
# everyone else's. _smart_matcher/LEARNING_AVAILABLE stay plain globals:
# they're just a class reference and an availability flag, not per-visitor
# state, so they're safe to share.
_learning_memory_by_visitor: Dict[str, Any] = {}
_feedback_learner_by_visitor: Dict[str, Any] = {}

def _init_learning_modules(visitor_id: str):
    """Initialize (or fetch the already-cached) learning modules for this visitor."""
    global LEARNING_AVAILABLE, _smart_matcher
    if visitor_id in _learning_memory_by_visitor:
        return True
    try:
        from learning_memory import get_memory, get_feedback_learner, detect_topic, SmartMatcher
        _learning_memory_by_visitor[visitor_id] = get_memory(visitor_id)
        _feedback_learner_by_visitor[visitor_id] = get_feedback_learner(visitor_id)
        _smart_matcher = SmartMatcher
        LEARNING_AVAILABLE = True
        return True
    except ImportError:
        LEARNING_AVAILABLE = False
        return False

def get_smart_matcher(visitor_id: str):
    """Get the SmartMatcher class for spell correction."""
    _init_learning_modules(visitor_id)
    return _smart_matcher

def get_learning_memory(visitor_id: str):
    """Get this visitor's conversation memory instance."""
    _init_learning_modules(visitor_id)
    return _learning_memory_by_visitor.get(visitor_id)

def get_feedback_learner_instance(visitor_id: str):
    """Get this visitor's feedback learner instance."""
    _init_learning_modules(visitor_id)
    return _feedback_learner_by_visitor.get(visitor_id)

def store_qa_interaction(visitor_id: str, question: str, answer: str, topic: str = None):
    """Store a Q&A interaction for learning, scoped to this visitor."""
    if not _init_learning_modules(visitor_id):
        return
    try:
        from learning_memory import detect_topic
        topic = topic or detect_topic(question)
        _learning_memory_by_visitor[visitor_id].store_qa(question, answer, topic)
    except Exception:
        pass

def record_feedback(visitor_id: str, question: str, answer: str, is_positive: bool, correction: str = None):
    """Record user feedback on a response with advanced learning, scoped to this visitor."""
    if not _init_learning_modules(visitor_id):
        return
    try:
        from learning_memory import update_learning_from_feedback
        # Use the advanced feedback function that also updates user profile
        update_learning_from_feedback(visitor_id, question, answer, is_positive, correction)
    except ImportError:
        # Fallback to basic feedback recording
        try:
            from learning_memory import detect_topic
            topic = detect_topic(question)
            _feedback_learner_by_visitor[visitor_id].record_feedback(topic, question, answer, is_positive, correction)
        except Exception:
            pass
    except Exception:
        pass

def _check_learned_response(visitor_id: str, user_message: str) -> Optional[Dict]:
    """
    Check if we have a learned response for this question, from this
    visitor's own learned corrections/ratings. Uses advanced matching
    including corrections.

    Returns:
        Dict with 'answer', 'confidence', 'source' or None
    """
    if not _init_learning_modules(visitor_id):
        return None

    try:
        from learning_memory import get_smart_response, detect_topic

        # Use the new smart response system
        learned = get_smart_response(visitor_id, user_message)

        if learned:
            return learned

        # Fallback to simple check for older data format
        topic = detect_topic(user_message)
        if topic:
            similar = _feedback_learner_by_visitor[visitor_id].find_similar_question(user_message, topic)
            if similar and similar.get("score", 0) >= 3:
                return {
                    "answer": similar.get("a"),
                    "confidence": similar.get("_confidence", {"score": 0.7, "icon": "🟢", "level": "high"}),
                    "source": "learned"
                }

    except Exception:
        pass

    return None


def _format_learned_response(learned: Dict) -> str:
    """Format a learned response with confidence indicator."""
    answer = learned.get("answer", "")
    confidence = learned.get("confidence", {})
    source = learned.get("source", "learned")
    
    # Get confidence icon
    icon = confidence.get("icon", "🟢")
    level = confidence.get("level", "high")
    score = confidence.get("score", 0.7)
    
    # Add a subtle indicator for learned responses
    if source == "correction":
        header = f"📝 *From your correction* {icon}\n\n"
    elif score >= 0.8:
        header = f"⭐ *Learned response* {icon}\n\n"
    else:
        header = ""
    
    return header + answer


def get_response_with_learning(visitor_id: str, user_message: str, *args, **kwargs) -> Tuple[str, Optional[Dict]]:
    """
    Get a response, checking learned responses first.

    Returns:
        Tuple of (response_text, learning_info)
        learning_info is None if response was generated, or Dict with confidence if learned
    """
    # Check for learned response first
    learned = _check_learned_response(visitor_id, user_message)

    if learned and learned.get("answer"):
        formatted = _format_learned_response(learned)
        return (formatted, learned)

    # No learned response, generate normally
    # (The generate_response function will be called separately)
    return (None, None)

def get_learning_stats(visitor_id: str) -> Dict:
    """Get combined learning statistics for this visitor."""
    if not _init_learning_modules(visitor_id):
        return {"available": False}

    try:
        mem_stats = _learning_memory_by_visitor[visitor_id].get_stats()
        fb_stats = _feedback_learner_by_visitor[visitor_id].get_stats()
        user_profile = mem_stats.get("user_profile", {})
        
        # Check if semantic search is available
        semantic_available = False
        try:
            from learning_memory import SmartMatcher
            semantic_available = SmartMatcher.is_semantic_available()
        except Exception:
            pass
        
        return {
            "available": True,
            "total_interactions": mem_stats.get("total_qa", 0),
            "feedback_count": fb_stats.get("total_feedback", 0),
            "satisfaction_rate": fb_stats.get("satisfaction_rate", 0),
            "top_topics": mem_stats.get("top_topics", []),
            "corrections_count": fb_stats.get("corrections_count", 0),
            "skill_level": user_profile.get("skill_level", "unknown"),
            "interests": user_profile.get("interests", []),
            "topics_mastered": user_profile.get("topics_mastered", []),
            "semantic_search": semantic_available
        }
    except Exception:
        return {"available": False}

# =============================================================================
# GROQ API INTEGRATION (Optional - Enhances responses when available)
# =============================================================================

GROQ_AVAILABLE = False
_groq_client = None

def _get_groq_client():
    """Get or create Groq client if API key is available."""
    global _groq_client, GROQ_AVAILABLE
    
    if _groq_client is not None:
        return _groq_client
    
    api_key = os.environ.get("GROQ_API_KEY")
    if api_key:
        try:
            from groq import Groq
            _groq_client = Groq(api_key=api_key)
            GROQ_AVAILABLE = True
            return _groq_client
        except ImportError:
            pass
    return None


def _query_groq(prompt: str, system_prompt: str = None, max_tokens: int = 512) -> Optional[str]:
    """
    Query Groq API for enhanced responses.
    
    Args:
        prompt: User's question
        system_prompt: System instructions
        max_tokens: Maximum response length
        
    Returns:
        AI response or None if API not available
    """
    client = _get_groq_client()
    if not client:
        return None
    
    try:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",  # Fast model for quick responses (llama-3.1-8b-instant was retired 2026-08-16)
            messages=messages,
            temperature=0.7,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content
    except Exception:
        return None  # Fall back to local response


def _try_groq_for_complex_query(
    user_message: str,
    question: str = "",
    function_name: str = "",
    user_code: str = ""
) -> Optional[str]:
    """
    Try to get a Groq AI response for complex queries.
    Used as enhancement when local pattern matching doesn't find a good answer.
    
    Returns:
        AI response or None if API not available/fails
    """
    client = _get_groq_client()
    if not client:
        return None
    
    # Build context-aware system prompt
    system_prompt = """You are PyCode Assistant, a helpful Python programming tutor.
Keep responses concise (under 200 words), educational, and encouraging.

Guidelines:
- Explain concepts clearly with examples when helpful
- For coding problems, guide rather than give direct answers
- Use code blocks with ```python for code examples
- Be friendly and supportive"""
    
    # Add problem context if available
    if question and function_name:
        system_prompt += f"""

Current Problem Context:
- Problem: {question}
- Function to write: {function_name}"""
        
        if user_code and user_code.strip() != f"def {function_name}():\\n    # Your code here\\n    pass":
            system_prompt += f"""
- User's current code:
```python
{user_code}
```"""
    
    try:
        return _query_groq(user_message, system_prompt, max_tokens=400)
    except Exception:
        return None


# =============================================================================
# PDF KNOWLEDGE BASE INTEGRATION
# =============================================================================

# PDF Knowledge Base - Lazy Loading to avoid slow startup
# The sentence_transformers/torch import is very slow, so we only load when needed
PDF_KB_AVAILABLE = False
_pdf_kb_initialized = False
_pdf_kb_module = None

def _get_pdf_kb_module():
    """Lazy import of PDF knowledge base module to avoid slow startup."""
    global _pdf_kb_module, PDF_KB_AVAILABLE
    if _pdf_kb_module is None:
        try:
            import pdf_knowledge_base as kb
            _pdf_kb_module = kb
            PDF_KB_AVAILABLE = True
        except ImportError:
            PDF_KB_AVAILABLE = False
    return _pdf_kb_module

def _ensure_pdf_kb_initialized():
    """Lazy initialization of PDF knowledge base."""
    global _pdf_kb_initialized, PDF_KB_AVAILABLE
    kb = _get_pdf_kb_module()
    if kb and not _pdf_kb_initialized:
        try:
            kb.initialize_knowledge_base()
            _pdf_kb_initialized = True
        except Exception:
            pass  # Silently fail - will use fallback

def query_knowledge(query: str) -> str:
    """Query the PDF knowledge base if available."""
    kb = _get_pdf_kb_module()
    if kb and _pdf_kb_initialized:
        try:
            return kb.query_knowledge(query)
        except Exception:
            pass
    return ""

def is_knowledge_base_ready() -> bool:
    """Check if knowledge base is ready."""
    kb = _get_pdf_kb_module()
    return kb is not None and _pdf_kb_initialized


# =============================================================================
# AUTOMATION CONCEPTS INTEGRATION (Selenium, Robot Framework, pytest)
# =============================================================================

AUTOMATION_CONCEPTS_AVAILABLE = False

try:
    from automation_concepts import (
        SELENIUM_CONCEPTS,
        ROBOT_FRAMEWORK_CONCEPTS,
        RELATED_TOOLS_CONCEPTS,
        ALL_AUTOMATION_CONCEPTS,
        AUTOMATION_TAGS
    )
    AUTOMATION_CONCEPTS_AVAILABLE = True
except ImportError:
    SELENIUM_CONCEPTS = {}
    ROBOT_FRAMEWORK_CONCEPTS = {}
    RELATED_TOOLS_CONCEPTS = {}
    ALL_AUTOMATION_CONCEPTS = {}
    AUTOMATION_TAGS = []


# =============================================================================
# ADVANCED CONCEPTS INTEGRATION (Modern Python 3.7+ Features)
# =============================================================================

ADVANCED_CONCEPTS_AVAILABLE = False

try:
    from advanced_concepts import (
        ADVANCED_CONCEPTS,
        ADVANCED_TAGS
    )
    ADVANCED_CONCEPTS_AVAILABLE = True
except ImportError:
    ADVANCED_CONCEPTS = {}
    ADVANCED_TAGS = []


# =============================================================================
# INFRASTRUCTURE CONCEPTS INTEGRATION (Networking, Servers, Storage)
# =============================================================================

INFRASTRUCTURE_CONCEPTS_AVAILABLE = False

try:
    from infrastructure_concepts import (
        INFRASTRUCTURE_CONCEPTS,
        INFRASTRUCTURE_TAGS
    )
    INFRASTRUCTURE_CONCEPTS_AVAILABLE = True
except ImportError:
    INFRASTRUCTURE_CONCEPTS = {}
    INFRASTRUCTURE_TAGS = []


# =============================================================================
# LINUX CONCEPTS INTEGRATION
# =============================================================================

LINUX_CONCEPTS_AVAILABLE = False

try:
    from linux_concepts import (
        LINUX_CONCEPTS,
        LINUX_TAGS
    )
    LINUX_CONCEPTS_AVAILABLE = True
except ImportError:
    LINUX_CONCEPTS = {}
    LINUX_TAGS = []


def _match_automation_concept(topic: str, topic_words: List[str]) -> Optional[str]:
    """
    Match user query against automation concepts (Selenium, Robot Framework, etc.)
    
    Args:
        topic: Cleaned topic string from user query
        topic_words: List of words from the topic
        
    Returns:
        Matching concept explanation or None
    """
    if not AUTOMATION_CONCEPTS_AVAILABLE:
        return None
    
    topic_lower = topic.lower()
    topic_words_lower = [w.lower() for w in topic_words]
    full_query = ' '.join(topic_words_lower)
    
    # Map of related terms to help matching (term in query -> implied concept prefix)
    term_to_concept_prefix = {
        'xpath': 'selenium',
        'css': 'selenium',
        'webdriver': 'selenium',
        'browser': 'selenium',
        'element': 'selenium',
        'click': 'selenium',
        'wait': 'selenium',
        'alert': 'selenium',
        'frame': 'selenium',
        'iframe': 'selenium',
        'pabot': 'robot',
        'resource': 'robot',
        'keyword': 'robot',
    }
    
    # Expand query with implied terms
    expanded_words = list(topic_words_lower)
    for query_term, implied_prefix in term_to_concept_prefix.items():
        if query_term in topic_words_lower and implied_prefix not in topic_words_lower:
            expanded_words.append(implied_prefix)
    
    expanded_query = ' '.join(expanded_words)
    
    # Specific topic terms that should be prioritized in matching
    specific_terms = ['keywords', 'variables', 'waits', 'locators', 'actions', 
                     'alerts', 'frames', 'cookies', 'screenshots', 'fixtures',
                     'seleniumlibrary', 'control', 'flow', 'resource', 'files', 'tags',
                     'listeners', 'pabot', 'grid', 'page', 'object', 'structure',
                     'reporting', 'implicit', 'explicit', 'fluent', 'xpath', 'css',
                     'attributes', 'handling', 'custom', 'library']
    
    # Find which specific term the user is asking about
    query_specific_term = None
    for term in specific_terms:
        if term in expanded_words:
            query_specific_term = term
            break
    
    # Search for best matching concept
    best_match = None
    best_score = 0
    
    for concept_key in ALL_AUTOMATION_CONCEPTS.keys():
        score = 0
        concept_lower = concept_key.lower()
        concept_words = concept_lower.split()
        
        # Exact match (highest priority)
        if concept_lower == full_query or concept_lower == expanded_query:
            score = 200
        
        # If user asks about a specific topic (e.g., "keywords"), prioritize concepts containing that term
        elif query_specific_term and query_specific_term in concept_lower:
            # Check if the prefix matches (using expanded words)
            prefix_matches = any(cw in expanded_words for cw in concept_words if cw != query_specific_term)
            if prefix_matches:
                score = 150 + len(concept_key)  # High priority for specific matches
            else:
                score = 100 + len(concept_key)
        
        # All concept words present in expanded query
        elif all(cw in expanded_words for cw in concept_words):
            score = 90 + len(concept_key)
        
        # Concept key as substring in expanded query
        elif concept_lower in expanded_query:
            score = 80 + len(concept_key)
        
        # Partial match - some concept words present
        elif any(cw in expanded_words for cw in concept_words):
            matching_count = sum(1 for cw in concept_words if cw in expanded_words)
            score = 50 + (matching_count * 10)
        
        if score > best_score:
            best_score = score
            best_match = concept_key
    
    if best_match and best_score >= 50:
        return ALL_AUTOMATION_CONCEPTS[best_match]
    
    return None


def get_automation_concept(concept_name: str) -> Optional[str]:
    """
    Get a specific automation concept by name.
    
    Args:
        concept_name: Name of the concept to retrieve
        
    Returns:
        Concept explanation or None if not found
    """
    if not AUTOMATION_CONCEPTS_AVAILABLE:
        return None
    
    # Try exact match first
    if concept_name in ALL_AUTOMATION_CONCEPTS:
        return ALL_AUTOMATION_CONCEPTS[concept_name]
    
    # Try case-insensitive match
    concept_lower = concept_name.lower()
    for key in ALL_AUTOMATION_CONCEPTS:
        if key.lower() == concept_lower:
            return ALL_AUTOMATION_CONCEPTS[key]
    
    return None


def query_pdf_knowledge(question: str) -> Optional[str]:
    """
    Query the PDF knowledge base for an answer.
    
    Args:
        question: User's question about Python
        
    Returns:
        Formatted answer from PDF, or None if not available
    """
    if not PDF_KB_AVAILABLE:
        return None
    
    _ensure_pdf_kb_initialized()
    
    if not is_knowledge_base_ready():
        return None
    
    try:
        answer = query_knowledge(question)
        # Check if we got a meaningful answer (None means no good match)
        if answer is not None:
            return answer
    except Exception:
        pass
    
    return None


def get_enhanced_concept_response(topic: str) -> Optional[str]:
    """
    Get a comprehensive concept explanation combining structured data and PDF.
    
    Args:
        topic: The topic to explain (e.g., "class", "list", "loop")
        
    Returns:
        Well-formatted explanation or None
    """
    topic_lower = topic.lower().strip()
    
    # First check if we have a manual concept (these are well-structured)
    for key, explanation in CONCEPTS.items():
        if key in topic_lower:
            # We have a good structured response - optionally enhance with PDF
            return explanation
    
    # No manual concept - try PDF
    if PDF_KB_AVAILABLE:
        pdf_answer = query_pdf_knowledge(f"What is {topic} in Python? Explain {topic}.")
        if pdf_answer:
            return pdf_answer
    
    return None

# =============================================================================
# PYTHON CONCEPT LIBRARY - Comprehensive explanations
# =============================================================================

CONCEPTS = {
    # Data Structures
    "set": """## 🎯 Sets in Python

**Definition:** Unordered collection of unique elements.

### Creating Sets
```python
empty = set()  # NOT {} (that's a dict)
numbers = {1, 2, 3, 4, 5}
from_list = set([1, 2, 2, 3])  # {1, 2, 3}
comprehension = {x**2 for x in range(5)}
```

### Operations
```python
s = {1, 2, 3}

# Add/Remove
s.add(4)         # {1, 2, 3, 4}
s.remove(2)      # {1, 3, 4} - KeyError if missing
s.discard(5)     # No error if missing
s.pop()          # Remove arbitrary element

# Check
2 in s           # True/False

# Set Operations
a = {1, 2, 3}
b = {2, 3, 4}
a | b            # Union: {1, 2, 3, 4}
a & b            # Intersection: {2, 3}
a - b            # Difference: {1}
a ^ b            # Symmetric diff: {1, 4}
```

### Use Cases
- Remove duplicates: `list(set(items))`
- Membership testing (O(1))
- Finding common elements
- Tracking visited items

### Time Complexity
- Add/Remove/Check: O(1) average
- Union/Intersection: O(len(a) + len(b))""",

    "tuple": """## 📦 Tuples in Python

**Definition:** Immutable, ordered collection.

### Creating Tuples
```python
empty = ()
single = (1,)         # Note the comma!
point = (3, 4)
mixed = (1, "hello", 3.14)
from_list = tuple([1, 2, 3])
```

### Operations
```python
t = (1, 2, 3, 2, 1)

# Access
t[0]              # 1
t[-1]             # 1
t[1:3]            # (2, 3)

# Methods
t.count(2)        # 2
t.index(3)        # 2

# Unpacking
x, y, z = (1, 2, 3)
first, *rest = (1, 2, 3, 4)  # first=1, rest=[2,3,4]
```

### Why Use Tuples?
- **Immutable** - can be dict keys
- **Faster** than lists
- **Intent** - signal data shouldn't change
- **Memory efficient**

### Named Tuples
```python
from collections import namedtuple
Point = namedtuple('Point', ['x', 'y'])
p = Point(3, 4)
print(p.x, p.y)  # 3 4
```""",

    # Algorithms & Patterns
    "recursion": """## 🔁 Recursion in Python

**Definition:** A function that calls itself to solve smaller subproblems.

### Structure
```python
def recursive_function(input):
    # 1. Base case - when to stop
    if base_condition:
        return base_value
    
    # 2. Recursive case - break down problem
    return combine(recursive_function(smaller_input))
```

### Classic Examples

**Factorial**
```python
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)
# factorial(5) = 5 * 4 * 3 * 2 * 1 = 120
```

**Fibonacci**
```python
def fib(n):
    if n <= 1:
        return n
    return fib(n-1) + fib(n-2)

# With memoization (much faster!)
from functools import lru_cache

@lru_cache(maxsize=None)
def fib_memo(n):
    if n <= 1:
        return n
    return fib_memo(n-1) + fib_memo(n-2)
```

**Binary Search**
```python
def binary_search(arr, target, left, right):
    if left > right:
        return -1
    
    mid = (left + right) // 2
    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return binary_search(arr, target, mid + 1, right)
    else:
        return binary_search(arr, target, left, mid - 1)
```

### Recursion vs Iteration
| Recursion | Iteration |
|-----------|-----------|
| More elegant for trees/graphs | More memory efficient |
| Risk of stack overflow | No stack limit |
| Natural for divide & conquer | Better for simple loops |

### Tips
- Always define base case first
- Ensure progress toward base case
- Consider memoization for overlapping subproblems
- Watch for stack overflow (Python limit ~1000)""",

    "two pointers": """## 👆👆 Two Pointers Technique

**When to Use:** Sorted arrays, finding pairs, palindromes, linked lists.

### Pattern 1: Opposite Ends
```python
def two_sum_sorted(arr, target):
    left, right = 0, len(arr) - 1
    
    while left < right:
        current_sum = arr[left] + arr[right]
        if current_sum == target:
            return [left, right]
        elif current_sum < target:
            left += 1
        else:
            right -= 1
    
    return []
```

### Pattern 2: Same Direction (Fast/Slow)
```python
# Remove duplicates in-place
def remove_duplicates(arr):
    if not arr:
        return 0
    
    slow = 0
    for fast in range(1, len(arr)):
        if arr[fast] != arr[slow]:
            slow += 1
            arr[slow] = arr[fast]
    
    return slow + 1
```

### Pattern 3: Palindrome Check
```python
def is_palindrome(s):
    left, right = 0, len(s) - 1
    
    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1
    
    return True
```

### Common Problems
- Two Sum (sorted array)
- Three Sum
- Container With Most Water
- Valid Palindrome
- Remove Duplicates
- Linked List Cycle Detection

### Time Complexity
Usually O(n) - single pass with two pointers.""",

    "sliding window": """## 🪟 Sliding Window Technique

**When to Use:** Contiguous subarrays/substrings, max/min in range.

### Fixed Window
```python
def max_sum_subarray(arr, k):
    \"\"\"Find max sum of k consecutive elements.\"\"\"
    if len(arr) < k:
        return 0
    
    # Calculate first window
    window_sum = sum(arr[:k])
    max_sum = window_sum
    
    # Slide the window
    for i in range(k, len(arr)):
        window_sum += arr[i] - arr[i - k]
        max_sum = max(max_sum, window_sum)
    
    return max_sum
```

### Variable Window
```python
def min_subarray_len(target, arr):
    \"\"\"Find minimum length subarray with sum >= target.\"\"\"
    left = 0
    current_sum = 0
    min_len = float('inf')
    
    for right in range(len(arr)):
        current_sum += arr[right]
        
        while current_sum >= target:
            min_len = min(min_len, right - left + 1)
            current_sum -= arr[left]
            left += 1
    
    return min_len if min_len != float('inf') else 0
```

### String Pattern
```python
def longest_substring_k_distinct(s, k):
    \"\"\"Longest substring with at most k distinct characters.\"\"\"
    from collections import defaultdict
    
    char_count = defaultdict(int)
    left = 0
    max_len = 0
    
    for right in range(len(s)):
        char_count[s[right]] += 1
        
        while len(char_count) > k:
            char_count[s[left]] -= 1
            if char_count[s[left]] == 0:
                del char_count[s[left]]
            left += 1
        
        max_len = max(max_len, right - left + 1)
    
    return max_len
```

### Common Problems
- Maximum Sum Subarray of Size K
- Longest Substring Without Repeating Characters
- Minimum Window Substring
- Find All Anagrams in String

### Time Complexity
Usually O(n) - each element visited at most twice.""",

    "binary search": """## 🔍 Binary Search

**When to Use:** Sorted array, finding position, search space problems.

### Basic Binary Search
```python
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = left + (right - left) // 2  # Avoid overflow
        
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1  # Not found
```

### Find Insert Position
```python
def search_insert(arr, target):
    \"\"\"Find index where target should be inserted.\"\"\"
    left, right = 0, len(arr)
    
    while left < right:
        mid = (left + right) // 2
        if arr[mid] < target:
            left = mid + 1
        else:
            right = mid
    
    return left
```

### Find First/Last Occurrence
```python
def find_first(arr, target):
    left, right = 0, len(arr) - 1
    result = -1
    
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            result = mid
            right = mid - 1  # Keep searching left
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return result
```

### Search on Answer Space
```python
def min_eating_speed(piles, h):
    \"\"\"Koko eating bananas - find minimum speed.\"\"\"
    def can_finish(speed):
        return sum((p + speed - 1) // speed for p in piles) <= h
    
    left, right = 1, max(piles)
    
    while left < right:
        mid = (left + right) // 2
        if can_finish(mid):
            right = mid
        else:
            left = mid + 1
    
    return left
```

### Time Complexity: O(log n)""",

    "hash": """## #️⃣ Hash Tables & Hashing

**Python Implementation:** `dict` and `set`

### Counting Pattern
```python
def count_elements(arr):
    counts = {}
    for item in arr:
        counts[item] = counts.get(item, 0) + 1
    return counts

# Using Counter
from collections import Counter
counts = Counter(arr)
most_common = counts.most_common(3)  # Top 3
```

### Two Sum with Hash Map
```python
def two_sum(nums, target):
    seen = {}  # value -> index
    
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    
    return []
```

### Group Anagrams
```python
def group_anagrams(strs):
    from collections import defaultdict
    
    groups = defaultdict(list)
    for s in strs:
        key = tuple(sorted(s))  # or use character count
        groups[key].append(s)
    
    return list(groups.values())
```

### Check Duplicates
```python
def has_duplicates(arr):
    return len(arr) != len(set(arr))

def find_duplicate(arr):
    seen = set()
    for num in arr:
        if num in seen:
            return num
        seen.add(num)
    return None
```

### Common Problems
- Two Sum
- Contains Duplicate
- Group Anagrams
- Valid Anagram
- First Unique Character
- Intersection of Arrays

### Time Complexity
- Insert/Delete/Lookup: O(1) average, O(n) worst case""",

    "stack": """## 📚 Stack Data Structure

**Definition:** LIFO (Last In, First Out)

### Implementation with List
```python
stack = []

# Push
stack.append(1)
stack.append(2)
stack.append(3)

# Peek
top = stack[-1] if stack else None

# Pop
if stack:
    item = stack.pop()

# Check empty
is_empty = len(stack) == 0
```

### Valid Parentheses
```python
def is_valid(s):
    stack = []
    pairs = {')': '(', '}': '{', ']': '['}
    
    for char in s:
        if char in '({[':
            stack.append(char)
        elif char in ')}]':
            if not stack or stack[-1] != pairs[char]:
                return False
            stack.pop()
    
    return len(stack) == 0
```

### Monotonic Stack
```python
def next_greater_element(arr):
    \"\"\"Find next greater element for each position.\"\"\"
    result = [-1] * len(arr)
    stack = []  # Store indices
    
    for i in range(len(arr)):
        while stack and arr[stack[-1]] < arr[i]:
            idx = stack.pop()
            result[idx] = arr[i]
        stack.append(i)
    
    return result
```

### Evaluate Reverse Polish Notation
```python
def eval_rpn(tokens):
    stack = []
    ops = {
        '+': lambda a, b: a + b,
        '-': lambda a, b: a - b,
        '*': lambda a, b: a * b,
        '/': lambda a, b: int(a / b)
    }
    
    for token in tokens:
        if token in ops:
            b, a = stack.pop(), stack.pop()
            stack.append(ops[token](a, b))
        else:
            stack.append(int(token))
    
    return stack[0]
```

### Common Problems
- Valid Parentheses
- Min Stack
- Daily Temperatures
- Largest Rectangle in Histogram""",

    "queue": """## 📬 Queue Data Structure

**Definition:** FIFO (First In, First Out)

### Implementation with deque
```python
from collections import deque

queue = deque()

# Enqueue
queue.append(1)
queue.append(2)

# Dequeue
if queue:
    item = queue.popleft()  # O(1)

# Peek
front = queue[0] if queue else None

# Size
size = len(queue)
```

### BFS with Queue
```python
def bfs(graph, start):
    visited = {start}
    queue = deque([start])
    result = []
    
    while queue:
        node = queue.popleft()
        result.append(node)
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    
    return result
```

### Level Order Traversal
```python
def level_order(root):
    if not root:
        return []
    
    result = []
    queue = deque([root])
    
    while queue:
        level = []
        level_size = len(queue)
        
        for _ in range(level_size):
            node = queue.popleft()
            level.append(node.val)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        result.append(level)
    
    return result
```

### Common Problems
- BFS Traversal
- Level Order Traversal
- Rotting Oranges
- Sliding Window Maximum (with deque)""",

    "dynamic programming": """## 🧩 Dynamic Programming

**Definition:** Breaking problems into overlapping subproblems and storing results.

### Two Approaches

**Top-Down (Memoization)**
```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n):
    if n <= 1:
        return n
    return fib(n-1) + fib(n-2)
```

**Bottom-Up (Tabulation)**
```python
def fib(n):
    if n <= 1:
        return n
    
    dp = [0] * (n + 1)
    dp[1] = 1
    
    for i in range(2, n + 1):
        dp[i] = dp[i-1] + dp[i-2]
    
    return dp[n]
```

### Classic Problems

**Climbing Stairs**
```python
def climb_stairs(n):
    if n <= 2:
        return n
    
    prev2, prev1 = 1, 2
    for _ in range(3, n + 1):
        prev2, prev1 = prev1, prev2 + prev1
    
    return prev1
```

**Coin Change**
```python
def coin_change(coins, amount):
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    
    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i:
                dp[i] = min(dp[i], dp[i - coin] + 1)
    
    return dp[amount] if dp[amount] != float('inf') else -1
```

**Longest Common Subsequence**
```python
def lcs(text1, text2):
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i-1] == text2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    
    return dp[m][n]
```

### DP Steps
1. Define state (what changes?)
2. Define transition (how states relate?)
3. Define base case
4. Define final answer""",

    "sorting": """## 📊 Sorting Algorithms

### Built-in Sorting
```python
# Sort in-place
nums.sort()                    # Ascending
nums.sort(reverse=True)        # Descending
nums.sort(key=lambda x: x[1])  # By second element

# Return new list
sorted_nums = sorted(nums)
sorted_strs = sorted(strings, key=len)  # By length
sorted_dicts = sorted(dicts, key=lambda x: x['age'])
```

### Common Algorithms

**Bubble Sort - O(n²)**
```python
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
```

**Selection Sort - O(n²)**
```python
def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
```

**Merge Sort - O(n log n)**
```python
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result
```

**Quick Sort - O(n log n) average**
```python
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    return quick_sort(left) + middle + quick_sort(right)
```

### Comparison
| Algorithm | Best | Average | Worst | Space |
|-----------|------|---------|-------|-------|
| Bubble | O(n) | O(n²) | O(n²) | O(1) |
| Selection | O(n²) | O(n²) | O(n²) | O(1) |
| Insertion | O(n) | O(n²) | O(n²) | O(1) |
| Merge | O(n log n) | O(n log n) | O(n log n) | O(n) |
| Quick | O(n log n) | O(n log n) | O(n²) | O(log n) |
| Python sort | O(n) | O(n log n) | O(n log n) | O(n) |""",

    "graph": """## 🕸️ Graph Algorithms

### Graph Representation
```python
# Adjacency List (most common)
graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E']
}

# From edges
from collections import defaultdict
def build_graph(edges):
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)  # undirected
    return graph
```

### DFS (Depth-First Search)
```python
def dfs(graph, start, visited=None):
    if visited is None:
        visited = set()
    
    visited.add(start)
    print(start)
    
    for neighbor in graph[start]:
        if neighbor not in visited:
            dfs(graph, neighbor, visited)
    
    return visited
```

### BFS (Breadth-First Search)
```python
from collections import deque

def bfs(graph, start):
    visited = {start}
    queue = deque([start])
    
    while queue:
        node = queue.popleft()
        print(node)
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
```

### Shortest Path (BFS)
```python
def shortest_path(graph, start, end):
    if start == end:
        return [start]
    
    visited = {start}
    queue = deque([(start, [start])])
    
    while queue:
        node, path = queue.popleft()
        
        for neighbor in graph[node]:
            if neighbor == end:
                return path + [neighbor]
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
    
    return []
```

### Cycle Detection
```python
def has_cycle(graph):
    visited = set()
    
    def dfs(node, parent):
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                if dfs(neighbor, node):
                    return True
            elif neighbor != parent:
                return True
        return False
    
    for node in graph:
        if node not in visited:
            if dfs(node, None):
                return True
    return False
```""",

    "class": """## 🏗️ Classes in Python

**Definition:** A class is a blueprint for creating objects. Objects have attributes (data) and methods (functions).

### Basic Class Structure
```python
class Dog:
    \"\"\"A simple class representing a dog.\"\"\"
    
    def __init__(self, name, age):
        \"\"\"Initialize name and age attributes.\"\"\"
        self.name = name
        self.age = age
    
    def sit(self):
        \"\"\"Simulate a dog sitting.\"\"\"
        print(f"{self.name} is now sitting.")
    
    def roll_over(self):
        \"\"\"Simulate rolling over.\"\"\"
        print(f"{self.name} rolled over!")
```

### Creating Instances
```python
# Create an instance (object)
my_dog = Dog('Willie', 6)

# Access attributes
print(my_dog.name)  # 'Willie'
print(my_dog.age)   # 6

# Call methods
my_dog.sit()        # Willie is now sitting.
my_dog.roll_over()  # Willie rolled over!
```

### Key Concepts
| Concept | Description |
|---------|-------------|
| `class` | Keyword to define a class |
| `__init__` | Constructor method, runs when creating instance |
| `self` | Reference to the current instance |
| Attribute | Variable belonging to an object |
| Method | Function belonging to a class |

### Inheritance
```python
class ElectricCar(Car):
    \"\"\"A child class that inherits from Car.\"\"\"
    
    def __init__(self, make, model, year):
        \"\"\"Initialize parent class attributes.\"\"\"
        super().__init__(make, model, year)
        self.battery_size = 75
    
    def describe_battery(self):
        print(f"Battery: {self.battery_size} kWh")
```

### Why Use Classes?
- **Organization** - Group related data and functions
- **Reusability** - Create multiple objects from one class
- **Inheritance** - Build on existing classes
- **Encapsulation** - Hide internal details

### Common Patterns
```python
# Multiple instances
dog1 = Dog('Willie', 6)
dog2 = Dog('Lucy', 3)

# Modifying attributes
dog1.age = 7  # Direct modification

# Default values
class Cat:
    def __init__(self, name):
        self.name = name
        self.lives = 9  # Default value
```""",

    "function": """## ⚡ Functions in Python

**Definition:** A named block of reusable code that performs a specific task.

### Basic Function
```python
def greet_user(username):
    \"\"\"Display a simple greeting.\"\"\"
    print(f"Hello, {username}!")

# Call the function
greet_user("Alice")  # Hello, Alice!
```

### Parameters & Arguments
```python
# Positional arguments
def describe_pet(animal, name):
    print(f"I have a {animal} named {name}.")

describe_pet("dog", "Willie")

# Keyword arguments
describe_pet(name="Harry", animal="hamster")

# Default values
def describe_pet(name, animal="dog"):
    print(f"I have a {animal} named {name}.")

describe_pet("Willie")  # Uses default animal="dog"
```

### Return Values
```python
def get_formatted_name(first, last):
    \"\"\"Return a neatly formatted full name.\"\"\"
    full_name = f"{first} {last}"
    return full_name.title()

name = get_formatted_name("jimi", "hendrix")
print(name)  # Jimi Hendrix

# Returning multiple values
def get_stats(numbers):
    return min(numbers), max(numbers), sum(numbers)

low, high, total = get_stats([1, 2, 3, 4, 5])
```

### *args and **kwargs
```python
# Variable positional arguments
def make_pizza(*toppings):
    print(f"Making pizza with: {toppings}")

make_pizza("pepperoni", "mushrooms", "cheese")

# Variable keyword arguments
def build_profile(**user_info):
    return user_info

profile = build_profile(name="Albert", field="physics")
```

### Lambda Functions
```python
# Short anonymous functions
square = lambda x: x ** 2
print(square(5))  # 25

# Often used with map, filter, sorted
numbers = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x**2, numbers))
```""",

    "decorator": """## 🎀 Decorators in Python

**Definition:** A decorator is a function that modifies the behavior of another function without changing its code.

### Basic Decorator
```python
def my_decorator(func):
    def wrapper():
        print("Before the function call")
        func()
        print("After the function call")
    return wrapper

@my_decorator
def say_hello():
    print("Hello!")

say_hello()
# Output:
# Before the function call
# Hello!
# After the function call
```

### Decorator with Arguments
```python
def repeat(times):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(3)
def greet(name):
    print(f"Hello, {name}!")

greet("Alice")  # Prints greeting 3 times
```

### Common Built-in Decorators
```python
class MyClass:
    @staticmethod
    def static_method():
        print("No self needed")
    
    @classmethod
    def class_method(cls):
        print(f"Called on {cls}")
    
    @property
    def name(self):
        return self._name
```

### Use Cases
- **Logging** - Track function calls
- **Timing** - Measure execution time
- **Authentication** - Check user permissions
- **Caching** - Store results (see `@functools.lru_cache`)""",

    "exception": """## ⚠️ Exceptions in Python

**Definition:** Exceptions are errors detected during execution. Python uses try/except blocks to handle them gracefully.

### Basic Exception Handling
```python
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero!")
```

### Multiple Exceptions
```python
try:
    value = int(input("Enter a number: "))
    result = 10 / value
except ValueError:
    print("That's not a valid number!")
except ZeroDivisionError:
    print("Cannot divide by zero!")
except Exception as e:
    print(f"Unexpected error: {e}")
```

### try/except/else/finally
```python
try:
    file = open("data.txt")
    data = file.read()
except FileNotFoundError:
    print("File not found!")
else:
    print("File read successfully")  # Runs if no exception
finally:
    print("Cleanup code here")  # Always runs
```

### Common Exceptions
| Exception | Cause |
|-----------|-------|
| `ValueError` | Wrong type of value |
| `TypeError` | Wrong type |
| `IndexError` | Index out of range |
| `KeyError` | Key not in dictionary |
| `FileNotFoundError` | File doesn't exist |
| `ZeroDivisionError` | Division by zero |

### Raising Exceptions
```python
def validate_age(age):
    if age < 0:
        raise ValueError("Age cannot be negative")
    return age
```""",

    "file": """## 📁 File Handling in Python

**Definition:** Python can read from and write to files using the built-in `open()` function.

### Reading Files
```python
# Method 1: Using with statement (recommended)
with open('example.txt', 'r') as file:
    content = file.read()
    print(content)

# Method 2: Read line by line
with open('example.txt', 'r') as file:
    for line in file:
        print(line.strip())

# Method 3: Read all lines into a list
with open('example.txt', 'r') as file:
    lines = file.readlines()
```

### Writing Files
```python
# Write (overwrites existing content)
with open('output.txt', 'w') as file:
    file.write("Hello, World!\\n")
    file.write("Second line")

# Append (adds to existing content)
with open('output.txt', 'a') as file:
    file.write("\\nAppended line")
```

### File Modes
| Mode | Description |
|------|-------------|
| `'r'` | Read (default) |
| `'w'` | Write (overwrites) |
| `'a'` | Append |
| `'r+'` | Read and write |
| `'b'` | Binary mode (e.g., `'rb'`) |

### Working with Paths
```python
from pathlib import Path

# Create path object
path = Path('data/files/example.txt')

# Check if exists
if path.exists():
    content = path.read_text()

# Write to file
path.write_text("New content")

# List files in directory
for file in Path('.').glob('*.txt'):
    print(file.name)
```""",

    "module": """## 📦 Modules in Python

**Definition:** A module is a file containing Python code (functions, classes, variables) that can be imported and reused.

### Importing Modules
```python
# Import entire module
import math
print(math.sqrt(16))  # 4.0

# Import specific items
from math import sqrt, pi
print(sqrt(16))  # 4.0
print(pi)        # 3.14159...

# Import with alias
import numpy as np
import pandas as pd

# Import all (not recommended)
from math import *
```

### Creating Your Own Module
```python
# my_module.py
def greet(name):
    return f"Hello, {name}!"

PI = 3.14159

class Calculator:
    def add(self, a, b):
        return a + b
```

```python
# main.py
import my_module

print(my_module.greet("Alice"))
print(my_module.PI)
calc = my_module.Calculator()
```

### Common Standard Library Modules
| Module | Purpose |
|--------|---------|
| `os` | Operating system interface |
| `sys` | System-specific parameters |
| `json` | JSON encoding/decoding |
| `datetime` | Date and time |
| `random` | Random number generation |
| `re` | Regular expressions |
| `collections` | Specialized containers |

### if __name__ == "__main__"
```python
# my_module.py
def main():
    print("Running as main program")

if __name__ == "__main__":
    main()  # Only runs when executed directly
```""",

    "object": """## 🎯 Objects in Python

**Definition:** An object is an instance of a class. Everything in Python is an object - integers, strings, lists, functions, and even classes themselves.

### Creating Objects
```python
# Define a class
class Dog:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def bark(self):
        print(f"{self.name} says Woof!")

# Create objects (instances)
my_dog = Dog("Willie", 6)
your_dog = Dog("Lucy", 3)

# Each object has its own data
print(my_dog.name)   # Willie
print(your_dog.name) # Lucy
```

### Objects Have:
| Component | Description | Example |
|-----------|-------------|---------|
| **Attributes** | Data stored in the object | `my_dog.name` |
| **Methods** | Functions that belong to object | `my_dog.bark()` |
| **Identity** | Unique ID in memory | `id(my_dog)` |
| **Type** | The class it was created from | `type(my_dog)` |

### Everything is an Object
```python
# Even basic types are objects
x = 5
print(type(x))        # <class 'int'>
print(x.bit_length()) # 3 (method on int object)

s = "hello"
print(type(s))        # <class 'str'>
print(s.upper())      # HELLO (method on str object)

nums = [1, 2, 3]
print(type(nums))     # <class 'list'>
nums.append(4)        # Method on list object
```

### Object vs Class
```python
# Class = Blueprint (template)
class Car:
    def __init__(self, brand):
        self.brand = brand

# Object = Instance (actual thing created from blueprint)
tesla = Car("Tesla")   # tesla is an object
bmw = Car("BMW")       # bmw is another object
```

### Key Concepts
- **Instantiation**: Creating an object from a class
- **self**: Reference to the current object instance
- **Attributes**: Variables that belong to an object
- **Methods**: Functions that belong to an object""",

    "variable": """## 📝 Variables in Python

**Definition:** A variable is a name that refers to a value stored in memory. Python variables are dynamically typed.

### Creating Variables
```python
# No type declaration needed
message = "Hello, World!"
number = 42
pi = 3.14159
is_valid = True

# Multiple assignment
x, y, z = 1, 2, 3
a = b = c = 0
```

### Variable Naming Rules
```python
# Valid names
my_variable = 1
_private = 2
camelCase = 3
CONSTANT = 4
name2 = 5

# Invalid names (will cause errors)
# 2name = 1      # Can't start with number
# my-var = 2     # No hyphens
# class = 3      # Can't use reserved words
```

### Data Types
```python
# Python infers the type automatically
integer = 42           # int
floating = 3.14        # float
string = "Hello"       # str
boolean = True         # bool
nothing = None         # NoneType
items = [1, 2, 3]      # list
mapping = {"a": 1}     # dict

# Check type
print(type(integer))   # <class 'int'>
```

### Type Conversion
```python
# Convert between types
str(42)        # "42"
int("42")      # 42
float("3.14")  # 3.14
list("abc")    # ['a', 'b', 'c']
bool(0)        # False
bool(1)        # True
```

### Variable Scope
```python
global_var = "I'm global"

def my_function():
    local_var = "I'm local"
    print(global_var)   # Can access global
    print(local_var)    # Can access local

my_function()
# print(local_var)  # Error! Not accessible outside
```""",

    "method": """## 🔧 Methods in Python

**Definition:** A method is a function that belongs to an object or class. It can access and modify the object's data.

### Instance Methods
```python
class Dog:
    def __init__(self, name):
        self.name = name
    
    # Instance method - takes 'self' as first parameter
    def bark(self):
        print(f"{self.name} says Woof!")
    
    def rename(self, new_name):
        self.name = new_name

dog = Dog("Willie")
dog.bark()              # Willie says Woof!
dog.rename("Max")
dog.bark()              # Max says Woof!
```

### Class Methods
```python
class Dog:
    species = "Canis familiaris"
    
    def __init__(self, name):
        self.name = name
    
    @classmethod
    def get_species(cls):
        return cls.species
    
    @classmethod
    def create_puppy(cls, name):
        return cls(name)  # Creates new instance

print(Dog.get_species())     # Canis familiaris
puppy = Dog.create_puppy("Buddy")
```

### Static Methods
```python
class MathHelper:
    @staticmethod
    def add(a, b):
        return a + b
    
    @staticmethod
    def is_even(n):
        return n % 2 == 0

# No instance needed
print(MathHelper.add(5, 3))      # 8
print(MathHelper.is_even(4))     # True
```

### Special Methods (Dunder Methods)
```python
class Book:
    def __init__(self, title, pages):
        self.title = title
        self.pages = pages
    
    def __str__(self):
        return f"{self.title}"
    
    def __len__(self):
        return self.pages
    
    def __eq__(self, other):
        return self.title == other.title

book = Book("Python Guide", 300)
print(book)          # Python Guide (uses __str__)
print(len(book))     # 300 (uses __len__)
```

### Method Types Summary
| Type | Decorator | First Param | Use Case |
|------|-----------|-------------|----------|
| Instance | None | `self` | Access instance data |
| Class | `@classmethod` | `cls` | Access class data |
| Static | `@staticmethod` | None | Utility functions |""",

    "inheritance": """## 🧬 Inheritance in Python

**Definition:** Inheritance allows a class to inherit attributes and methods from another class, promoting code reuse.

### Basic Inheritance
```python
# Parent class (base class)
class Animal:
    def __init__(self, name):
        self.name = name
    
    def speak(self):
        print(f"{self.name} makes a sound")

# Child class (derived class)
class Dog(Animal):
    def speak(self):  # Override parent method
        print(f"{self.name} says Woof!")

class Cat(Animal):
    def speak(self):
        print(f"{self.name} says Meow!")

dog = Dog("Willie")
cat = Cat("Whiskers")
dog.speak()  # Willie says Woof!
cat.speak()  # Whiskers says Meow!
```

### Using super()
```python
class Vehicle:
    def __init__(self, brand, year):
        self.brand = brand
        self.year = year

class Car(Vehicle):
    def __init__(self, brand, year, doors):
        super().__init__(brand, year)  # Call parent's __init__
        self.doors = doors
    
    def describe(self):
        return f"{self.year} {self.brand} with {self.doors} doors"

my_car = Car("Toyota", 2022, 4)
print(my_car.describe())  # 2022 Toyota with 4 doors
```

### Multiple Inheritance
```python
class Flyable:
    def fly(self):
        print("Flying!")

class Swimmable:
    def swim(self):
        print("Swimming!")

class Duck(Flyable, Swimmable):
    def quack(self):
        print("Quack!")

duck = Duck()
duck.fly()    # Flying!
duck.swim()   # Swimming!
duck.quack()  # Quack!
```

### Checking Inheritance
```python
class Animal: pass
class Dog(Animal): pass

dog = Dog()

# Check if instance of class
print(isinstance(dog, Dog))     # True
print(isinstance(dog, Animal))  # True

# Check if subclass
print(issubclass(Dog, Animal))  # True
```

### Key Concepts
- **Parent/Base class**: The class being inherited from
- **Child/Derived class**: The class that inherits
- **Override**: Replace parent method with new implementation
- **super()**: Access parent class methods""",

    "loop": """## 🔄 Loops in Python

**Definition:** Loops allow you to execute a block of code repeatedly, either a specific number of times or while a condition is true.

### For Loops
```python
# Iterate over a list
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)

# Iterate with range
for i in range(5):        # 0, 1, 2, 3, 4
    print(i)

for i in range(2, 6):     # 2, 3, 4, 5
    print(i)

for i in range(0, 10, 2): # 0, 2, 4, 6, 8
    print(i)
```

### While Loops
```python
# Basic while loop
count = 0
while count < 5:
    print(count)
    count += 1

# With user input
while True:
    response = input("Enter 'quit' to exit: ")
    if response == 'quit':
        break
```

### Loop Control
```python
# break - exit the loop entirely
for i in range(10):
    if i == 5:
        break  # Stop at 5
    print(i)   # Prints 0-4

# continue - skip to next iteration
for i in range(5):
    if i == 2:
        continue  # Skip 2
    print(i)      # Prints 0, 1, 3, 4

# else - runs if loop completes without break
for i in range(3):
    print(i)
else:
    print("Loop completed!")
```

### Useful Loop Patterns
```python
# enumerate - get index and value
for i, fruit in enumerate(fruits):
    print(f"{i}: {fruit}")

# zip - iterate multiple lists together
names = ["Alice", "Bob"]
ages = [25, 30]
for name, age in zip(names, ages):
    print(f"{name} is {age}")

# List comprehension
squares = [x**2 for x in range(10)]
evens = [x for x in range(20) if x % 2 == 0]
```

### Nested Loops
```python
for i in range(3):
    for j in range(3):
        print(f"({i}, {j})", end=" ")
    print()  # New line after each row
# Output:
# (0, 0) (0, 1) (0, 2)
# (1, 0) (1, 1) (1, 2)
# (2, 0) (2, 1) (2, 2)
```""",

    "if": """## ❓ Conditional Statements (if/elif/else)

**Definition:** Conditional statements allow your program to make decisions and execute different code based on conditions.

### Basic if Statement
```python
age = 18

if age >= 18:
    print("You are an adult")
```

### if-else
```python
age = 15

if age >= 18:
    print("You are an adult")
else:
    print("You are a minor")
```

### if-elif-else
```python
score = 85

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
elif score >= 60:
    grade = "D"
else:
    grade = "F"

print(f"Your grade: {grade}")  # B
```

### Comparison Operators
| Operator | Meaning |
|----------|---------|
| `==` | Equal to |
| `!=` | Not equal to |
| `<` | Less than |
| `>` | Greater than |
| `<=` | Less than or equal |
| `>=` | Greater than or equal |

### Logical Operators
```python
age = 25
has_license = True

# and - both must be true
if age >= 18 and has_license:
    print("Can drive")

# or - at least one must be true
if age < 13 or age > 65:
    print("Discount available")

# not - inverts the boolean
if not has_license:
    print("Cannot drive")
```

### Truthiness
```python
# These are "falsy" (evaluate to False)
if not 0:          print("0 is falsy")
if not "":         print("Empty string is falsy")
if not []:         print("Empty list is falsy")
if not None:       print("None is falsy")

# These are "truthy" (evaluate to True)
if 1:              print("Non-zero is truthy")
if "hello":        print("Non-empty string is truthy")
if [1, 2]:         print("Non-empty list is truthy")
```

### Ternary Operator
```python
# condition_if_true if condition else condition_if_false
age = 20
status = "adult" if age >= 18 else "minor"
print(status)  # adult
```""",

    "import": """## 📥 Importing in Python

**Definition:** Import statements allow you to use code from other modules (files) in your program.

### Import Styles
```python
# Import entire module
import math
print(math.sqrt(16))    # 4.0
print(math.pi)          # 3.14159...

# Import specific items
from math import sqrt, pi
print(sqrt(16))         # 4.0
print(pi)               # 3.14159...

# Import with alias
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Import all (not recommended)
from math import *
```

### Common Standard Library
```python
# Working with files and system
import os
import sys
from pathlib import Path

# Data handling
import json
import csv
import pickle

# Date and time
from datetime import datetime, timedelta

# Random numbers
import random

# Regular expressions
import re

# Collections
from collections import Counter, defaultdict, deque
```

### Importing Your Own Modules
```python
# my_utils.py
def greet(name):
    return f"Hello, {name}!"

# main.py
from my_utils import greet
print(greet("Alice"))

# Or import the whole module
import my_utils
print(my_utils.greet("Alice"))
```

### Package Imports
```python
# From a package (folder with __init__.py)
from mypackage import mymodule
from mypackage.subpackage import helper

# Relative imports (inside a package)
from . import sibling_module
from ..parent_package import something
```

### Best Practices
```python
# Group imports in this order:
# 1. Standard library
import os
import sys

# 2. Third-party packages
import numpy as np
import pandas as pd

# 3. Local imports
from myproject import utils
```""",

    "print": """## 🖨️ Print Function in Python

**Definition:** The `print()` function outputs text and values to the console.

### Basic Printing
```python
print("Hello, World!")
print(42)
print(3.14)
print(True)
```

### Printing Multiple Values
```python
name = "Alice"
age = 25

# Multiple arguments (separated by space)
print("Name:", name, "Age:", age)
# Output: Name: Alice Age: 25

# Custom separator
print("a", "b", "c", sep="-")
# Output: a-b-c

# Custom end character
print("Hello", end=" ")
print("World")
# Output: Hello World
```

### Formatted Strings (f-strings)
```python
name = "Alice"
age = 25
score = 95.5

# f-string (Python 3.6+)
print(f"Name: {name}, Age: {age}")

# Expressions inside f-strings
print(f"Next year: {age + 1}")
print(f"Score: {score:.1f}%")

# Format specifiers
print(f"{42:05d}")      # 00042 (pad with zeros)
print(f"{3.14159:.2f}") # 3.14 (2 decimal places)
print(f"{1000:,}")      # 1,000 (thousand separator)
```

### Other Formatting Methods
```python
# .format() method
print("Hello, {}!".format(name))
print("{0} is {1} years old".format(name, age))
print("{name} is {age}".format(name="Bob", age=30))

# % formatting (older style)
print("Name: %s, Age: %d" % (name, age))
```

### Printing Collections
```python
# Lists
fruits = ["apple", "banana", "cherry"]
print(fruits)  # ['apple', 'banana', 'cherry']

# Pretty printing
from pprint import pprint
data = {"name": "Alice", "scores": [90, 85, 88]}
pprint(data)

# Join list items
print(", ".join(fruits))  # apple, banana, cherry
```

### Print to File
```python
# Write to file instead of console
with open("output.txt", "w") as f:
    print("Hello, File!", file=f)
```""",

    "input": """## ⌨️ Input Function in Python

**Definition:** The `input()` function reads user input from the keyboard and returns it as a string.

### Basic Input
```python
name = input("Enter your name: ")
print(f"Hello, {name}!")
```

### Converting Input Types
```python
# Input is always a string - convert as needed
age = int(input("Enter your age: "))
height = float(input("Enter height (m): "))
```

### Handling Invalid Input
```python
# Using try/except
while True:
    try:
        age = int(input("Enter your age: "))
        break
    except ValueError:
        print("Please enter a valid number!")

print(f"You are {age} years old")
```

### Multiple Inputs
```python
# Split input into multiple values
data = input("Enter x y z: ")
x, y, z = data.split()
print(f"x={x}, y={y}, z={z}")

# Convert to integers
numbers = input("Enter numbers (space-separated): ")
nums = [int(n) for n in numbers.split()]
print(f"Sum: {sum(nums)}")
```

### Input Validation
```python
# Validate yes/no response
while True:
    response = input("Continue? (yes/no): ").lower()
    if response in ["yes", "no"]:
        break
    print("Please enter 'yes' or 'no'")

# Validate number range
while True:
    try:
        score = int(input("Enter score (0-100): "))
        if 0 <= score <= 100:
            break
        print("Score must be between 0 and 100")
    except ValueError:
        print("Please enter a number")
```

### Menu System Example
```python
def show_menu():
    print("\\n1. Add item")
    print("2. View items")
    print("3. Exit")

while True:
    show_menu()
    choice = input("Enter choice: ")
    
    if choice == "1":
        print("Adding item...")
    elif choice == "2":
        print("Viewing items...")
    elif choice == "3":
        print("Goodbye!")
        break
    else:
        print("Invalid choice")
```""",

    "return": """## ↩️ Return Statement in Python

**Definition:** The `return` statement exits a function and optionally sends a value back to the caller.

### Basic Return
```python
def add(a, b):
    return a + b

result = add(3, 5)
print(result)  # 8
```

### Return vs Print
```python
# WRONG - prints but returns None
def add_wrong(a, b):
    print(a + b)

result = add_wrong(3, 5)  # Prints 8
print(result)              # None!

# CORRECT - returns the value
def add_correct(a, b):
    return a + b

result = add_correct(3, 5)
print(result)  # 8
```

### Multiple Return Values
```python
def get_stats(numbers):
    return min(numbers), max(numbers), sum(numbers)

# Unpack returned tuple
low, high, total = get_stats([1, 2, 3, 4, 5])
print(f"Min: {low}, Max: {high}, Sum: {total}")
```

### Conditional Returns
```python
def get_grade(score):
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    else:
        return "F"

print(get_grade(85))  # B
```

### Early Return
```python
def find_first_even(numbers):
    for num in numbers:
        if num % 2 == 0:
            return num  # Exit immediately when found
    return None  # No even number found

result = find_first_even([1, 3, 4, 6, 8])
print(result)  # 4
```

### Return None
```python
# Functions without return statement return None
def greet(name):
    print(f"Hello, {name}!")

result = greet("Alice")  # Prints greeting
print(result)            # None

# Explicit return None
def maybe_process(data):
    if not data:
        return None  # Or just: return
    return process(data)
```

### Return in Recursion
```python
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

print(factorial(5))  # 120
```""",

    # =========================================================================
    # PYTHON FUNDAMENTALS
    # =========================================================================
    
    "python": """## 🐍 What is Python?

**Definition:** Python is a high-level, interpreted, general-purpose programming language created by Guido van Rossum.

### History of Python
| Year | Milestone |
|------|-----------|
| **1989** | Guido van Rossum started Python as a hobby project |
| **1991** | Python 0.9.0 released (had classes, functions, exception handling) |
| **1994** | Python 1.0 released (lambda, map, filter, reduce) |
| **2000** | Python 2.0 released (list comprehensions, garbage collection) |
| **2008** | Python 3.0 released (not backward compatible, fixed inconsistencies) |
| **2020** | Python 2 officially retired (End of Life) |
| **Today** | Python 3.11+ with significant performance improvements |

### Why Python?
```
✓ Easy to Learn     - Clean, readable syntax like English
✓ Versatile         - Web, AI, Data Science, Automation, Games
✓ Large Community   - Millions of developers, extensive support
✓ Rich Ecosystem    - 400,000+ packages on PyPI
✓ Cross-Platform    - Windows, Mac, Linux, embedded systems
✓ Free & Open Source - No licensing costs
✓ High Productivity - Write less code, do more
```

### Python Philosophy (The Zen of Python)
```python
import this
# Beautiful is better than ugly.
# Explicit is better than implicit.
# Simple is better than complex.
# Readability counts.
```

### Python vs Other Languages
| Feature | Python | Java | C++ |
|---------|--------|------|-----|
| Typing | Dynamic | Static | Static |
| Syntax | Simple | Verbose | Complex |
| Speed | Slower | Fast | Fastest |
| Learning Curve | Easy | Medium | Hard |
| Memory Management | Automatic | Automatic | Manual |

### How Python Works
```
Source Code (.py) → Python Interpreter → Bytecode (.pyc) → Python VM → Output
```

### Hello World Comparison
```python
# Python - Simple and clean
print("Hello, World!")

# Java - Verbose
# public class Hello {
#     public static void main(String[] args) {
#         System.out.println("Hello, World!");
#     }
# }
```""",

    "python use": """## 🌍 Where is Python Used? (Real-World Applications)

### 1. Web Development
```python
# Django - Instagram, Pinterest, Spotify
# Flask - Netflix, Reddit, Lyft
# FastAPI - Microsoft, Uber, Netflix

from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to my website!"
```
**Companies:** Instagram, Pinterest, Spotify, Dropbox, Reddit

### 2. Data Science & Analytics
```python
import pandas as pd
import matplotlib.pyplot as plt

# Analyze sales data
sales = pd.read_csv('sales.csv')
monthly_revenue = sales.groupby('month')['revenue'].sum()
monthly_revenue.plot(kind='bar')
plt.title('Monthly Revenue')
plt.show()
```
**Companies:** Netflix (recommendations), Uber (pricing), Airbnb (search)

### 3. Artificial Intelligence & Machine Learning
```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Train a model to predict customer churn
X_train, X_test, y_train, y_test = train_test_split(X, y)
model = RandomForestClassifier()
model.fit(X_train, y_train)
predictions = model.predict(X_test)
```
**Companies:** Google (TensorFlow), Facebook (PyTorch), OpenAI (GPT)

### 4. Automation & Scripting
```python
import os
import shutil
from datetime import datetime

# Automatically organize downloads folder
downloads = '/Users/me/Downloads'
for file in os.listdir(downloads):
    if file.endswith('.pdf'):
        shutil.move(f'{downloads}/{file}', '/Users/me/Documents/PDFs/')
    elif file.endswith(('.jpg', '.png')):
        shutil.move(f'{downloads}/{file}', '/Users/me/Pictures/')
```
**Use Cases:** File management, data backup, report generation

### 5. Scientific Computing
```python
import numpy as np
from scipy import integrate

# Calculate integral of x^2 from 0 to 1
result, error = integrate.quad(lambda x: x**2, 0, 1)
print(f"Integral: {result}")  # 0.333...
```
**Organizations:** NASA, CERN, Universities worldwide

### 6. Game Development
```python
import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("My Game")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0, 0, 0))
    pygame.display.flip()
```
**Games:** Civilization IV, EVE Online, Battlefield 2

### 7. DevOps & System Administration
```python
import subprocess
import paramiko

# SSH into server and run commands
ssh = paramiko.SSHClient()
ssh.connect('server.com', username='admin', password='secret')
stdin, stdout, stderr = ssh.exec_command('df -h')
print(stdout.read().decode())
```
**Tools:** Ansible, SaltStack, Fabric

### 8. Finance & Trading
```python
import yfinance as yf

# Get stock data
apple = yf.Ticker("AAPL")
history = apple.history(period="1mo")
print(history['Close'].mean())  # Average closing price
```
**Companies:** JPMorgan, Goldman Sachs, Bloomberg

### 9. IoT & Embedded Systems
```python
# Raspberry Pi - Control LED
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
GPIO.output(18, GPIO.HIGH)  # Turn on LED
```
**Devices:** Raspberry Pi, MicroPython boards, Home automation

### 10. Cybersecurity
```python
import hashlib
import requests

# Check if password has been breached
password = "mypassword123"
sha1 = hashlib.sha1(password.encode()).hexdigest().upper()
response = requests.get(f'https://api.pwnedpasswords.com/range/{sha1[:5]}')
```
**Tools:** Nmap scripting, Penetration testing, Security analysis""",

    # =========================================================================
    # DATA TYPES
    # =========================================================================
    
    "data type": """## 📊 Data Types in Python

**Definition:** Data types define what kind of value a variable can hold and what operations can be performed on it.

### Numeric Types
```python
# Integer (int) - Whole numbers, unlimited precision
age = 25
big_num = 10**100  # Python handles huge numbers!

# Float - Decimal numbers (64-bit)
price = 19.99
scientific = 1.5e-10  # Scientific notation

# Complex - Real + Imaginary parts
z = 3 + 4j
print(z.real)  # 3.0
print(z.imag)  # 4.0
```

### Text Type
```python
# String (str) - Immutable sequence of characters
name = "Alice"
multiline = '''Line 1
Line 2
Line 3'''
raw = r"C:\\path\\to\\file"  # Raw string
formatted = f"Hello, {name}!"  # f-string
```

### Sequence Types
```python
# List - Mutable, ordered, allows duplicates
fruits = ["apple", "banana", "cherry"]
fruits.append("date")
fruits[0] = "apricot"

# Tuple - Immutable, ordered, allows duplicates
point = (10, 20)
# point[0] = 5  # Error! Tuples are immutable

# Range - Immutable sequence of numbers
numbers = range(1, 10, 2)  # 1, 3, 5, 7, 9
```

### Mapping Type
```python
# Dictionary (dict) - Key-value pairs, mutable
person = {
    "name": "Alice",
    "age": 25,
    "city": "NYC"
}
person["email"] = "alice@email.com"
```

### Set Types
```python
# Set - Unordered, unique elements, mutable
unique_nums = {1, 2, 3, 3, 3}  # {1, 2, 3}
unique_nums.add(4)

# Frozenset - Immutable set
frozen = frozenset([1, 2, 3])
```

### Boolean Type
```python
# bool - True or False
is_active = True
is_empty = False

# Truthy and Falsy values
bool(0)       # False
bool("")      # False
bool([])      # False
bool(None)    # False
bool(1)       # True
bool("hello") # True
```

### None Type
```python
# NoneType - Represents absence of value
result = None
if result is None:
    print("No result yet")
```

### Binary Types
```python
# bytes - Immutable sequence of bytes
data = b"Hello"
print(data[0])  # 72 (ASCII for 'H')

# bytearray - Mutable sequence of bytes
mutable_data = bytearray(b"Hello")
mutable_data[0] = 74  # Change to 'J'

# memoryview - Memory view of bytes
view = memoryview(bytes(5))
```

### Type Checking & Conversion
```python
# Check type
print(type(42))        # <class 'int'>
print(isinstance(42, int))  # True

# Convert types
int("42")      # 42
float("3.14")  # 3.14
str(42)        # "42"
list("abc")    # ['a', 'b', 'c']
tuple([1,2,3]) # (1, 2, 3)
set([1,1,2])   # {1, 2}
```

### Type Summary Table
| Type | Example | Mutable | Ordered |
|------|---------|---------|---------|
| int | `42` | ❌ | N/A |
| float | `3.14` | ❌ | N/A |
| str | `"hello"` | ❌ | ✅ |
| list | `[1, 2, 3]` | ✅ | ✅ |
| tuple | `(1, 2, 3)` | ❌ | ✅ |
| dict | `{"a": 1}` | ✅ | ✅* |
| set | `{1, 2, 3}` | ✅ | ❌ |
| bool | `True` | ❌ | N/A |

*Dicts are ordered in Python 3.7+""",

    # =========================================================================
    # OOP CONCEPTS
    # =========================================================================
    
    "oop": """## 🏗️ Object-Oriented Programming (OOP) in Python

**Definition:** OOP is a programming paradigm that organizes code into objects that contain data (attributes) and behavior (methods).

### The 4 Pillars of OOP

#### 1. Encapsulation
Bundling data and methods that work on that data within a class.
```python
class BankAccount:
    def __init__(self, balance):
        self.__balance = balance  # Private attribute
    
    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
    
    def get_balance(self):
        return self.__balance

account = BankAccount(1000)
account.deposit(500)
print(account.get_balance())  # 1500
# print(account.__balance)    # Error! Private
```

#### 2. Inheritance
Creating new classes based on existing classes.
```python
class Animal:
    def __init__(self, name):
        self.name = name
    
    def speak(self):
        pass

class Dog(Animal):
    def speak(self):
        return f"{self.name} says Woof!"

class Cat(Animal):
    def speak(self):
        return f"{self.name} says Meow!"

dog = Dog("Buddy")
print(dog.speak())  # Buddy says Woof!
```

#### 3. Polymorphism
Same interface, different implementations.
```python
class Shape:
    def area(self):
        pass

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def area(self):
        return self.width * self.height

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
    
    def area(self):
        return 3.14159 * self.radius ** 2

# Same method, different behavior
shapes = [Rectangle(4, 5), Circle(3)]
for shape in shapes:
    print(shape.area())  # 20, 28.27...
```

#### 4. Abstraction
Hiding complex implementation details.
```python
from abc import ABC, abstractmethod

class Vehicle(ABC):
    @abstractmethod
    def start(self):
        pass
    
    @abstractmethod
    def stop(self):
        pass

class Car(Vehicle):
    def start(self):
        return "Car engine started"
    
    def stop(self):
        return "Car engine stopped"

# vehicle = Vehicle()  # Error! Can't instantiate abstract class
car = Car()
print(car.start())  # Car engine started
```

### OOP Concepts Summary
| Concept | Purpose | Example |
|---------|---------|---------|
| **Class** | Blueprint for objects | `class Dog:` |
| **Object** | Instance of a class | `my_dog = Dog()` |
| **Attribute** | Data stored in object | `self.name` |
| **Method** | Function in a class | `def bark(self):` |
| **Constructor** | Initialize object | `__init__` |
| **Encapsulation** | Hide internal details | Private attributes |
| **Inheritance** | Reuse code from parent | `class Cat(Animal):` |
| **Polymorphism** | Same interface, different behavior | Method overriding |
| **Abstraction** | Hide complexity | Abstract base classes |""",

    "encapsulation": """## 🔒 Encapsulation in Python

**Definition:** Encapsulation is the bundling of data and methods that operate on that data within a single unit (class), and restricting direct access to some components.

### Access Modifiers
```python
class Employee:
    def __init__(self, name, salary):
        self.name = name          # Public - accessible everywhere
        self._department = "IT"    # Protected - convention only
        self.__salary = salary     # Private - name mangling
    
    # Getter method
    def get_salary(self):
        return self.__salary
    
    # Setter method with validation
    def set_salary(self, salary):
        if salary > 0:
            self.__salary = salary
        else:
            raise ValueError("Salary must be positive")

emp = Employee("Alice", 50000)
print(emp.name)           # Alice (public)
print(emp._department)    # IT (protected - accessible but shouldn't)
# print(emp.__salary)     # Error! (private)
print(emp.get_salary())   # 50000 (through method)
```

### Name Mangling
```python
class MyClass:
    def __init__(self):
        self.__private = "secret"

obj = MyClass()
# print(obj.__private)      # AttributeError
print(obj._MyClass__private) # "secret" (name mangling)
# But this defeats the purpose - don't do this!
```

### Property Decorator (Pythonic Encapsulation)
```python
class Temperature:
    def __init__(self, celsius):
        self._celsius = celsius
    
    @property
    def celsius(self):
        return self._celsius
    
    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError("Temperature below absolute zero!")
        self._celsius = value
    
    @property
    def fahrenheit(self):
        return self._celsius * 9/5 + 32

temp = Temperature(25)
print(temp.celsius)     # 25 (calls getter)
print(temp.fahrenheit)  # 77.0 (computed property)
temp.celsius = 30       # Calls setter with validation
# temp.celsius = -300   # ValueError!
```

### Benefits of Encapsulation
```
✓ Data Protection  - Prevent accidental modification
✓ Flexibility      - Change implementation without affecting users
✓ Validation       - Control what values are accepted
✓ Maintainability  - Easier to debug and modify
```

### Real-World Example
```python
class BankAccount:
    def __init__(self, account_number, initial_balance=0):
        self.__account_number = account_number
        self.__balance = initial_balance
        self.__transactions = []
    
    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            self.__transactions.append(f"Deposit: +${amount}")
            return True
        return False
    
    def withdraw(self, amount):
        if 0 < amount <= self.__balance:
            self.__balance -= amount
            self.__transactions.append(f"Withdraw: -${amount}")
            return True
        return False
    
    @property
    def balance(self):
        return self.__balance
    
    def get_statement(self):
        return "\\n".join(self.__transactions)

account = BankAccount("12345", 1000)
account.deposit(500)
account.withdraw(200)
print(f"Balance: ${account.balance}")  # $1300
print(account.get_statement())
```""",

    "polymorphism": """## 🔄 Polymorphism in Python

**Definition:** Polymorphism means "many forms" - the ability to use a single interface for different data types or classes.

### 1. Method Overriding (Runtime Polymorphism)
```python
class Animal:
    def speak(self):
        return "Some sound"

class Dog(Animal):
    def speak(self):
        return "Woof!"

class Cat(Animal):
    def speak(self):
        return "Meow!"

class Duck(Animal):
    def speak(self):
        return "Quack!"

# Same method, different behavior
animals = [Dog(), Cat(), Duck()]
for animal in animals:
    print(animal.speak())
# Output: Woof! Meow! Quack!
```

### 2. Duck Typing
```python
# "If it walks like a duck and quacks like a duck, it's a duck"
class Dog:
    def speak(self):
        return "Woof!"

class Robot:
    def speak(self):
        return "Beep boop!"

def make_speak(thing):
    # Don't care about the type, just that it has speak()
    print(thing.speak())

make_speak(Dog())   # Woof!
make_speak(Robot()) # Beep boop!
```

### 3. Operator Overloading
```python
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)
    
    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)
    
    def __str__(self):
        return f"Vector({self.x}, {self.y})"
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

v1 = Vector(2, 3)
v2 = Vector(4, 5)
print(v1 + v2)    # Vector(6, 8)
print(v1 * 3)     # Vector(6, 9)
print(v1 == v2)   # False
```

### 4. Method Overloading (via Default Arguments)
```python
class Calculator:
    def add(self, a, b=0, c=0):
        return a + b + c

calc = Calculator()
print(calc.add(5))        # 5
print(calc.add(5, 3))     # 8
print(calc.add(5, 3, 2))  # 10
```

### 5. Abstract Base Classes
```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass
    
    @abstractmethod
    def perimeter(self):
        pass

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def area(self):
        return self.width * self.height
    
    def perimeter(self):
        return 2 * (self.width + self.height)

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
    
    def area(self):
        return 3.14159 * self.radius ** 2
    
    def perimeter(self):
        return 2 * 3.14159 * self.radius

# Polymorphic function
def print_shape_info(shape):
    print(f"Area: {shape.area():.2f}")
    print(f"Perimeter: {shape.perimeter():.2f}")

shapes = [Rectangle(4, 5), Circle(3)]
for shape in shapes:
    print_shape_info(shape)
    print()
```

### Common Magic Methods for Polymorphism
| Method | Operator | Example |
|--------|----------|---------|
| `__add__` | `+` | `a + b` |
| `__sub__` | `-` | `a - b` |
| `__mul__` | `*` | `a * b` |
| `__truediv__` | `/` | `a / b` |
| `__eq__` | `==` | `a == b` |
| `__lt__` | `<` | `a < b` |
| `__len__` | `len()` | `len(a)` |
| `__str__` | `str()` | `print(a)` |
| `__iter__` | `for` | `for x in a` |""",

    "overloading": """## 🔄 Overloading in Python

**Definition:** Overloading allows using the same function/operator name with different implementations based on arguments or types.

### 1. Method Overloading (via Default Arguments)
Python doesn't support traditional method overloading. Instead, use default arguments:
```python
class Calculator:
    def add(self, a, b=0, c=0):
        return a + b + c

calc = Calculator()
calc.add(5)       # 5 (one argument)
calc.add(5, 3)    # 8 (two arguments)
calc.add(5, 3, 2) # 10 (three arguments)
```

### 2. Method Overloading (via *args)
```python
class Math:
    def add(self, *args):
        return sum(args)

m = Math()
m.add(1, 2)          # 3
m.add(1, 2, 3, 4)    # 10
```

### 3. Operator Overloading (Magic Methods)
```python
class Vector:
    def __init__(self, x, y):
        self.x, self.y = x, y
    
    def __add__(self, other):      # +
        return Vector(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):      # -
        return Vector(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar):     # *
        return Vector(self.x * scalar, self.y * scalar)
    
    def __eq__(self, other):       # ==
        return self.x == other.x and self.y == other.y
    
    def __str__(self):
        return f"Vector({self.x}, {self.y})"

v1, v2 = Vector(2, 3), Vector(4, 5)
print(v1 + v2)  # Vector(6, 8)
print(v1 * 3)   # Vector(6, 9)
```

### 4. Using @singledispatch (functools)
```python
from functools import singledispatch

@singledispatch
def process(data):
    return f"Unknown type: {type(data)}"

@process.register(int)
def _(data):
    return f"Integer: {data * 2}"

@process.register(str)
def _(data):
    return f"String: {data.upper()}"

@process.register(list)
def _(data):
    return f"List with {len(data)} items"

print(process(5))         # Integer: 10
print(process("hello"))   # String: HELLO
print(process([1,2,3]))   # List with 3 items
```

### Common Operators to Overload
| Method | Operator | Example |
|--------|----------|---------|
| `__add__` | `+` | `a + b` |
| `__sub__` | `-` | `a - b` |
| `__mul__` | `*` | `a * b` |
| `__truediv__` | `/` | `a / b` |
| `__eq__` | `==` | `a == b` |
| `__lt__` | `<` | `a < b` |
| `__le__` | `<=` | `a <= b` |
| `__len__` | `len()` | `len(a)` |
| `__getitem__` | `[]` | `a[i]` |
| `__call__` | `()` | `a()` |

**Key Point:** Python favors duck typing over strict overloading - "If it walks like a duck and quacks like a duck, it's a duck." """,

    "abstraction": """## 🎭 Abstraction in Python

**Definition:** Abstraction is the process of hiding complex implementation details and showing only the necessary features of an object.

### Abstract Base Classes (ABC)
```python
from abc import ABC, abstractmethod

class Database(ABC):
    @abstractmethod
    def connect(self):
        pass
    
    @abstractmethod
    def execute(self, query):
        pass
    
    @abstractmethod
    def close(self):
        pass
    
    # Concrete method (has implementation)
    def log(self, message):
        print(f"[DB LOG] {message}")

class MySQLDatabase(Database):
    def connect(self):
        self.log("Connecting to MySQL...")
        # MySQL-specific connection logic
        return "MySQL Connected"
    
    def execute(self, query):
        self.log(f"Executing: {query}")
        # MySQL-specific query execution
        return f"MySQL Result for: {query}"
    
    def close(self):
        self.log("Closing MySQL connection")

class PostgreSQLDatabase(Database):
    def connect(self):
        self.log("Connecting to PostgreSQL...")
        return "PostgreSQL Connected"
    
    def execute(self, query):
        self.log(f"Executing: {query}")
        return f"PostgreSQL Result for: {query}"
    
    def close(self):
        self.log("Closing PostgreSQL connection")

# Usage - same interface, different implementations
def run_query(db: Database, query: str):
    db.connect()
    result = db.execute(query)
    db.close()
    return result

mysql = MySQLDatabase()
postgres = PostgreSQLDatabase()

print(run_query(mysql, "SELECT * FROM users"))
print(run_query(postgres, "SELECT * FROM users"))
```

### Abstract Properties
```python
from abc import ABC, abstractmethod

class Vehicle(ABC):
    @property
    @abstractmethod
    def max_speed(self):
        pass
    
    @property
    @abstractmethod
    def fuel_type(self):
        pass
    
    def describe(self):
        return f"Max Speed: {self.max_speed} km/h, Fuel: {self.fuel_type}"

class Car(Vehicle):
    @property
    def max_speed(self):
        return 200
    
    @property
    def fuel_type(self):
        return "Gasoline"

class ElectricCar(Vehicle):
    @property
    def max_speed(self):
        return 250
    
    @property
    def fuel_type(self):
        return "Electric"

car = Car()
tesla = ElectricCar()
print(car.describe())   # Max Speed: 200 km/h, Fuel: Gasoline
print(tesla.describe()) # Max Speed: 250 km/h, Fuel: Electric
```

### Real-World Example: Payment System
```python
from abc import ABC, abstractmethod

class PaymentProcessor(ABC):
    @abstractmethod
    def process_payment(self, amount):
        pass
    
    @abstractmethod
    def refund(self, transaction_id):
        pass

class CreditCardProcessor(PaymentProcessor):
    def process_payment(self, amount):
        # Credit card API integration hidden
        return f"Charged ${amount} to credit card"
    
    def refund(self, transaction_id):
        return f"Refunded transaction {transaction_id}"

class PayPalProcessor(PaymentProcessor):
    def process_payment(self, amount):
        # PayPal API integration hidden
        return f"Charged ${amount} via PayPal"
    
    def refund(self, transaction_id):
        return f"PayPal refund for {transaction_id}"

class CryptoProcessor(PaymentProcessor):
    def process_payment(self, amount):
        return f"Received {amount} in cryptocurrency"
    
    def refund(self, transaction_id):
        return f"Crypto refund for {transaction_id}"

# User doesn't need to know implementation details
def checkout(processor: PaymentProcessor, amount: float):
    result = processor.process_payment(amount)
    print(result)

checkout(CreditCardProcessor(), 99.99)
checkout(PayPalProcessor(), 49.99)
checkout(CryptoProcessor(), 199.99)
```

### Benefits of Abstraction
```
✓ Simplicity    - Users see only what they need
✓ Security      - Hide sensitive implementation
✓ Flexibility   - Change implementation without affecting users
✓ Modularity    - Separate concerns clearly
✓ Reusability   - Define common interfaces
```""",

    # =========================================================================
    # PYTHON KEYWORDS
    # =========================================================================
    
    "keyword": """## 🔑 Python Keywords

**Definition:** Keywords are reserved words in Python that have special meanings and cannot be used as variable names.

### All Python Keywords (35 total)
```python
import keyword
print(keyword.kwlist)
```

### Control Flow Keywords
```python
# if, elif, else - Conditional execution
if x > 0:
    print("Positive")
elif x < 0:
    print("Negative")
else:
    print("Zero")

# for - Iterate over sequence
for item in items:
    process(item)

# while - Loop while condition is true
while condition:
    do_something()

# break - Exit loop immediately
for i in range(10):
    if i == 5:
        break

# continue - Skip to next iteration
for i in range(10):
    if i == 5:
        continue
    print(i)

# pass - Do nothing (placeholder)
def empty_function():
    pass
```

### Function Keywords
```python
# def - Define a function
def greet(name):
    return f"Hello, {name}!"

# return - Return value from function
def add(a, b):
    return a + b

# lambda - Anonymous function
square = lambda x: x ** 2

# yield - Generator function
def count_up(n):
    for i in range(n):
        yield i
```

### Class Keywords
```python
# class - Define a class
class Dog:
    def __init__(self, name):
        self.name = name

# self - Reference to instance (convention, not keyword)
# Note: 'self' is a convention, not actually a keyword
```

### Exception Handling Keywords
```python
# try, except, finally, raise
try:
    risky_operation()
except ValueError as e:
    print(f"Error: {e}")
finally:
    cleanup()

# raise - Raise an exception
raise ValueError("Invalid input")

# assert - Debug assertion
assert x > 0, "x must be positive"
```

### Logical Keywords
```python
# and, or, not - Logical operators
if a and b:      # Both true
if a or b:       # At least one true
if not a:        # Negation

# True, False - Boolean values
is_valid = True
is_empty = False

# None - Null value
result = None

# is - Identity comparison
if x is None:
    print("x is None")

# in - Membership test
if "a" in "abc":
    print("Found!")
```

### Import Keywords
```python
# import, from, as
import math
from datetime import datetime
import numpy as np  # 'as' for aliasing
```

### Context Manager Keywords
```python
# with - Context management
with open("file.txt") as f:
    content = f.read()

# as - Aliasing in various contexts
import pandas as pd
except Exception as e:
with open("file") as f:
```

### Variable Scope Keywords
```python
# global - Access global variable
x = 10

def modify():
    global x
    x = 20

# nonlocal - Access enclosing scope variable
def outer():
    x = 10
    def inner():
        nonlocal x
        x = 20
    inner()
```

### Async Keywords
```python
# async, await - Asynchronous programming
async def fetch_data():
    await asyncio.sleep(1)
    return "Data"

# Run async function
import asyncio
result = asyncio.run(fetch_data())
```

### Other Keywords
```python
# del - Delete variable/item
del my_variable
del my_list[0]

# True, False, None - Singleton constants
```

### Keywords Summary Table
| Category | Keywords |
|----------|----------|
| Control Flow | `if`, `elif`, `else`, `for`, `while`, `break`, `continue`, `pass` |
| Functions | `def`, `return`, `lambda`, `yield` |
| Classes | `class` |
| Exceptions | `try`, `except`, `finally`, `raise`, `assert` |
| Logical | `and`, `or`, `not`, `True`, `False`, `None`, `is`, `in` |
| Import | `import`, `from`, `as` |
| Scope | `global`, `nonlocal` |
| Context | `with` |
| Async | `async`, `await` |
| Other | `del` |""",

    # =========================================================================
    # PACKAGES AND MODULES
    # =========================================================================
    
    "package": """## 📦 Packages in Python

**Definition:** A package is a way of organizing related modules into a directory hierarchy. It's a folder containing Python modules and a special `__init__.py` file.

### Package Structure
```
mypackage/
│
├── __init__.py        # Makes it a package
├── module1.py         # Module 1
├── module2.py         # Module 2
│
└── subpackage/        # Sub-package
    ├── __init__.py
    └── module3.py
```

### Creating a Package

**mypackage/__init__.py**
```python
# Can be empty or contain initialization code
from .module1 import function1
from .module2 import MyClass

__version__ = "1.0.0"
__all__ = ['function1', 'MyClass']  # What gets exported
```

**mypackage/module1.py**
```python
def function1():
    return "Hello from module1"

def helper():
    return "Internal helper"
```

**mypackage/module2.py**
```python
class MyClass:
    def __init__(self, name):
        self.name = name
    
    def greet(self):
        return f"Hello, {self.name}!"
```

### Using the Package
```python
# Import entire package
import mypackage
print(mypackage.__version__)

# Import specific module
from mypackage import module1
print(module1.function1())

# Import specific function/class
from mypackage.module1 import function1
from mypackage.module2 import MyClass

# Import from subpackage
from mypackage.subpackage import module3
```

### Popular Python Packages

#### Data Science
```python
# NumPy - Numerical computing
import numpy as np
arr = np.array([1, 2, 3, 4, 5])
print(arr.mean())  # 3.0

# Pandas - Data analysis
import pandas as pd
df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
print(df.describe())

# Matplotlib - Visualization
import matplotlib.pyplot as plt
plt.plot([1, 2, 3], [1, 4, 9])
plt.show()
```

#### Web Development
```python
# Flask - Lightweight web framework
from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, World!"

# Django - Full-featured web framework
# django-admin startproject mysite

# FastAPI - Modern API framework
from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}
```

#### Machine Learning
```python
# Scikit-learn - ML algorithms
from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier()
model.fit(X_train, y_train)

# TensorFlow - Deep learning
import tensorflow as tf
model = tf.keras.Sequential([
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(10, activation='softmax')
])

# PyTorch - Deep learning
import torch
import torch.nn as nn
```

### Installing Packages
```bash
# Install from PyPI
pip install package_name

# Install specific version
pip install package_name==1.0.0

# Install from requirements file
pip install -r requirements.txt

# List installed packages
pip list

# Show package info
pip show package_name
```

### requirements.txt Example
```
numpy>=1.20.0
pandas==1.3.0
flask>=2.0.0
requests~=2.26.0
```

### Virtual Environments
```bash
# Create virtual environment
python -m venv myenv

# Activate (Windows)
myenv\\Scripts\\activate

# Activate (Mac/Linux)
source myenv/bin/activate

# Deactivate
deactivate
```""",

    # =========================================================================
    # REGULAR EXPRESSIONS
    # =========================================================================
    
    "regex": """## 🔍 Regular Expressions in Python

**Definition:** Regular expressions (regex) are patterns used to match, search, and manipulate text. Python's `re` module provides regex support.

### Basic Patterns
```python
import re

# . - Any character except newline
# ^ - Start of string
# $ - End of string
# * - 0 or more repetitions
# + - 1 or more repetitions
# ? - 0 or 1 repetition
# [] - Character class
# | - OR
# () - Group
```

### Common Functions
```python
import re

text = "The quick brown fox jumps over the lazy dog"

# re.search() - Find first match
match = re.search(r'quick', text)
if match:
    print(match.group())  # 'quick'
    print(match.start())  # 4 (position)

# re.findall() - Find all matches
words = re.findall(r'\\b\\w{4}\\b', text)  # 4-letter words
print(words)  # ['quick', 'brown', 'over', 'lazy']

# re.sub() - Replace matches
new_text = re.sub(r'dog', 'cat', text)
print(new_text)  # '...lazy cat'

# re.split() - Split by pattern
parts = re.split(r'\\s+', text)  # Split by whitespace
print(parts)
```

### Character Classes
```python
import re

# \\d - Digit [0-9]
# \\D - Non-digit
# \\w - Word character [a-zA-Z0-9_]
# \\W - Non-word character
# \\s - Whitespace
# \\S - Non-whitespace

text = "Order #12345 placed on 2024-01-15"

# Find all numbers
numbers = re.findall(r'\\d+', text)
print(numbers)  # ['12345', '2024', '01', '15']

# Find date pattern
date = re.search(r'\\d{4}-\\d{2}-\\d{2}', text)
print(date.group())  # '2024-01-15'
```

### Quantifiers
```python
import re

# {n}   - Exactly n times
# {n,}  - n or more times
# {n,m} - Between n and m times
# *     - 0 or more (same as {0,})
# +     - 1 or more (same as {1,})
# ?     - 0 or 1 (same as {0,1})

# Phone number patterns
text = "Call 123-456-7890 or 987-654-3210"
phones = re.findall(r'\\d{3}-\\d{3}-\\d{4}', text)
print(phones)  # ['123-456-7890', '987-654-3210']
```

### Groups and Capturing
```python
import re

# Extract parts of a match
email = "contact@example.com"
match = re.search(r'(\\w+)@(\\w+)\\.(\\w+)', email)
if match:
    print(match.group(0))  # Full match: 'contact@example.com'
    print(match.group(1))  # First group: 'contact'
    print(match.group(2))  # Second group: 'example'
    print(match.groups())  # All groups: ('contact', 'example', 'com')

# Named groups
match = re.search(r'(?P<user>\\w+)@(?P<domain>\\w+\\.\\w+)', email)
if match:
    print(match.group('user'))    # 'contact'
    print(match.group('domain'))  # 'example.com'
```

---

## 📧 Example 1: Email Validator
```python
import re

def validate_email(email):
    \"\"\"
    Validate email address format.
    Valid: user@domain.com, user.name@domain.co.uk
    Invalid: user@, @domain.com, user@domain
    \"\"\"
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$'
    
    if re.match(pattern, email):
        return True
    return False

# Test cases
emails = [
    "john@example.com",      # Valid
    "jane.doe@company.co.uk", # Valid
    "invalid@",               # Invalid
    "@nodomain.com",          # Invalid
    "spaces not@allowed.com", # Invalid
]

for email in emails:
    status = "✓ Valid" if validate_email(email) else "✗ Invalid"
    print(f"{email}: {status}")

# Output:
# john@example.com: ✓ Valid
# jane.doe@company.co.uk: ✓ Valid
# invalid@: ✗ Invalid
# @nodomain.com: ✗ Invalid
# spaces not@allowed.com: ✗ Invalid
```

---

## 📝 Example 2: Log File Parser
```python
import re
from collections import Counter

def parse_log_file(log_content):
    \"\"\"
    Parse web server log to extract:
    - IP addresses
    - Timestamps
    - HTTP methods
    - URLs
    - Status codes
    \"\"\"
    # Apache/Nginx log pattern
    pattern = r'(\\d+\\.\\d+\\.\\d+\\.\\d+).*\\[(.+?)\\].*"(GET|POST|PUT|DELETE) (.+?) HTTP.*" (\\d{3})'
    
    results = {
        'requests': [],
        'ip_counts': Counter(),
        'status_counts': Counter(),
        'method_counts': Counter()
    }
    
    for match in re.finditer(pattern, log_content):
        ip, timestamp, method, url, status = match.groups()
        
        results['requests'].append({
            'ip': ip,
            'timestamp': timestamp,
            'method': method,
            'url': url,
            'status': int(status)
        })
        
        results['ip_counts'][ip] += 1
        results['status_counts'][status] += 1
        results['method_counts'][method] += 1
    
    return results

# Sample log data
log_data = \"\"\"
192.168.1.1 - - [01/Jan/2024:10:00:00] "GET /index.html HTTP/1.1" 200
192.168.1.2 - - [01/Jan/2024:10:01:00] "POST /api/login HTTP/1.1" 200
192.168.1.1 - - [01/Jan/2024:10:02:00] "GET /about.html HTTP/1.1" 200
10.0.0.1 - - [01/Jan/2024:10:03:00] "GET /secret.html HTTP/1.1" 404
192.168.1.1 - - [01/Jan/2024:10:04:00] "DELETE /api/user/5 HTTP/1.1" 403
\"\"\"

results = parse_log_file(log_data)

print("=== Log Analysis ===")
print(f"Total requests: {len(results['requests'])}")
print(f"\\nTop IPs: {results['ip_counts'].most_common(3)}")
print(f"Status codes: {dict(results['status_counts'])}")
print(f"Methods: {dict(results['method_counts'])}")

# Output:
# === Log Analysis ===
# Total requests: 5
# Top IPs: [('192.168.1.1', 3), ('192.168.1.2', 1), ('10.0.0.1', 1)]
# Status codes: {'200': 3, '404': 1, '403': 1}
# Methods: {'GET': 3, 'POST': 1, 'DELETE': 1}
```

### Regex Cheat Sheet
| Pattern | Meaning | Example |
|---------|---------|---------|
| `.` | Any character | `a.c` matches "abc" |
| `^` | Start of string | `^Hello` |
| `$` | End of string | `world$` |
| `*` | 0 or more | `ab*c` matches "ac", "abc", "abbc" |
| `+` | 1 or more | `ab+c` matches "abc", "abbc" |
| `?` | 0 or 1 | `colou?r` matches "color", "colour" |
| `\\d` | Digit | `\\d{3}` matches "123" |
| `\\w` | Word char | `\\w+` matches "hello" |
| `\\s` | Whitespace | `\\s+` matches spaces |
| `[abc]` | Any of a,b,c | `[aeiou]` matches vowels |
| `[^abc]` | Not a,b,c | `[^0-9]` matches non-digits |
| `(...)` | Group | `(ab)+` matches "ab", "abab" |
| `\\b` | Word boundary | `\\bword\\b` matches "word" |""",

    # =========================================================================
    # STRING METHODS
    # =========================================================================
    
    "string": """## 📝 Strings in Python

**Definition:** Strings are immutable sequences of characters used to store and manipulate text.

### Creating Strings
```python
# Single and double quotes
single = 'Hello'
double = "World"
multiline = '''Line 1
Line 2
Line 3'''

# Raw strings (no escape processing)
path = r"C:\\Users\\name\\Documents"

# f-strings (formatted strings)
name = "Alice"
age = 25
greeting = f"Hello, {name}! You are {age} years old."
```

### Common String Methods
```python
text = "  Hello, World!  "

# Case methods
text.upper()        # "  HELLO, WORLD!  "
text.lower()        # "  hello, world!  "
text.title()        # "  Hello, World!  "
text.capitalize()   # "  hello, world!  "
text.swapcase()     # "  hELLO, wORLD!  "

# Whitespace methods
text.strip()        # "Hello, World!"
text.lstrip()       # "Hello, World!  "
text.rstrip()       # "  Hello, World!"

# Search methods
text.find("World")   # 9 (index, -1 if not found)
text.index("World")  # 9 (raises ValueError if not found)
text.count("o")      # 2
text.startswith("  H")  # True
text.endswith("!  ")    # True

# Replace and split
text.replace("World", "Python")  # "  Hello, Python!  "
"a,b,c".split(",")    # ['a', 'b', 'c']
"-".join(['a','b','c'])  # "a-b-c"
```

### String Formatting
```python
name = "Alice"
score = 95.678

# f-strings (Python 3.6+) - RECOMMENDED
f"Name: {name}, Score: {score:.2f}"

# .format() method
"Name: {}, Score: {:.2f}".format(name, score)

# % formatting (old style)
"Name: %s, Score: %.2f" % (name, score)

# Format specifiers
f"{42:05d}"      # "00042" (pad with zeros)
f"{3.14159:.2f}" # "3.14" (2 decimal places)
f"{1000:,}"      # "1,000" (thousand separator)
f"{255:x}"       # "ff" (hexadecimal)
f"{7:b}"         # "111" (binary)
f"{'left':<10}"  # "left      " (left align)
f"{'right':>10}" # "     right" (right align)
f"{'center':^10}" # "  center  " (center align)
```

### String Validation
```python
"hello".isalpha()     # True (only letters)
"123".isdigit()       # True (only digits)
"abc123".isalnum()    # True (letters or digits)
"   ".isspace()       # True (only whitespace)
"Hello".istitle()     # True (title case)
"HELLO".isupper()     # True (all uppercase)
"hello".islower()     # True (all lowercase)
```

### String Slicing
```python
text = "Python"
text[0]      # 'P' (first character)
text[-1]     # 'n' (last character)
text[0:3]    # 'Pyt' (slice)
text[::2]    # 'Pto' (every 2nd char)
text[::-1]   # 'nohtyP' (reverse)
```

### Time Complexity
- Access: O(1)
- Slice: O(k) where k is slice size
- Concatenation: O(n+m)
- Search: O(n)""",

    # =========================================================================
    # LIST METHODS
    # =========================================================================
    
    "list": """## 📋 Lists in Python

**Definition:** Lists are mutable, ordered sequences that can hold any type of data.

### Creating Lists
```python
# Empty list
empty = []
empty = list()

# With elements
numbers = [1, 2, 3, 4, 5]
mixed = [1, "hello", 3.14, True, None]
nested = [[1, 2], [3, 4], [5, 6]]

# From other iterables
from_string = list("hello")  # ['h', 'e', 'l', 'l', 'o']
from_range = list(range(5))  # [0, 1, 2, 3, 4]
```

### Adding Elements
```python
fruits = ["apple", "banana"]

# Add single element
fruits.append("cherry")       # ['apple', 'banana', 'cherry']

# Add at specific index
fruits.insert(1, "orange")    # ['apple', 'orange', 'banana', 'cherry']

# Add multiple elements
fruits.extend(["mango", "grape"])
# Or
fruits += ["kiwi", "pear"]
```

### Removing Elements
```python
fruits = ["apple", "banana", "cherry", "banana"]

# Remove by value (first occurrence)
fruits.remove("banana")       # ['apple', 'cherry', 'banana']

# Remove by index
del fruits[0]                 # ['cherry', 'banana']
item = fruits.pop()           # Returns 'banana', list is ['cherry']
item = fruits.pop(0)          # Returns 'cherry', list is []

# Clear all
fruits.clear()                # []
```

### Accessing Elements
```python
nums = [10, 20, 30, 40, 50]

# By index
nums[0]      # 10 (first)
nums[-1]     # 50 (last)
nums[1:4]    # [20, 30, 40] (slice)
nums[::2]    # [10, 30, 50] (every 2nd)
nums[::-1]   # [50, 40, 30, 20, 10] (reversed)

# Find element
nums.index(30)    # 2 (index of value)
nums.count(20)    # 1 (occurrences)
30 in nums        # True (membership)
```

### Sorting and Ordering
```python
nums = [3, 1, 4, 1, 5, 9, 2, 6]

# Sort in place
nums.sort()                   # [1, 1, 2, 3, 4, 5, 6, 9]
nums.sort(reverse=True)       # [9, 6, 5, 4, 3, 2, 1, 1]

# Sort with key function
words = ["banana", "Apple", "cherry"]
words.sort(key=str.lower)     # ['Apple', 'banana', 'cherry']

# Return new sorted list (original unchanged)
sorted_nums = sorted(nums)

# Reverse in place
nums.reverse()

# Return reversed iterator
reversed_nums = list(reversed(nums))
```

### List Comprehensions
```python
# Basic comprehension
squares = [x**2 for x in range(10)]
# [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

# With condition
evens = [x for x in range(20) if x % 2 == 0]
# [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]

# Nested comprehension
matrix = [[i*j for j in range(3)] for i in range(3)]
# [[0, 0, 0], [0, 1, 2], [0, 2, 4]]

# With transformation
names = ["alice", "bob", "charlie"]
upper_names = [name.upper() for name in names]
```

### Useful Functions
```python
nums = [3, 1, 4, 1, 5]

len(nums)    # 5 (length)
sum(nums)    # 14 (sum)
min(nums)    # 1 (minimum)
max(nums)    # 5 (maximum)
any(nums)    # True (any truthy)
all(nums)    # True (all truthy)
```

### Time Complexity
- Access by index: O(1)
- Append: O(1) amortized
- Insert/Delete at index: O(n)
- Search: O(n)
- Sort: O(n log n)""",

    # =========================================================================
    # DICTIONARY METHODS
    # =========================================================================
    
    "dictionary": """## 📖 Dictionaries in Python

**Definition:** Dictionaries are mutable, unordered collections of key-value pairs with O(1) average lookup time.

### Creating Dictionaries
```python
# Empty dictionary
empty = {}
empty = dict()

# With key-value pairs
person = {
    "name": "Alice",
    "age": 25,
    "city": "NYC"
}

# From tuples
pairs = dict([("a", 1), ("b", 2)])

# From keys (all same value)
keys = dict.fromkeys(["a", "b", "c"], 0)
# {'a': 0, 'b': 0, 'c': 0}
```

### Accessing Values
```python
person = {"name": "Alice", "age": 25}

# Direct access (raises KeyError if missing)
person["name"]           # "Alice"

# Safe access with get()
person.get("name")       # "Alice"
person.get("email")      # None
person.get("email", "N/A")  # "N/A" (default)

# Get all keys, values, items
person.keys()    # dict_keys(['name', 'age'])
person.values()  # dict_values(['Alice', 25])
person.items()   # dict_items([('name', 'Alice'), ('age', 25)])
```

### Adding/Updating
```python
person = {"name": "Alice"}

# Add/update single key
person["age"] = 25
person["name"] = "Bob"    # Update existing

# Update multiple keys
person.update({"city": "NYC", "job": "Developer"})

# setdefault - add only if missing
person.setdefault("country", "USA")  # Adds if not exists
person.setdefault("name", "Charlie") # Doesn't change (key exists)
```

### Removing
```python
person = {"name": "Alice", "age": 25, "city": "NYC"}

# Remove specific key
del person["city"]

# Remove and return value
age = person.pop("age")        # Returns 25
email = person.pop("email", None)  # Returns None (default)

# Remove last inserted (Python 3.7+)
key, value = person.popitem()

# Clear all
person.clear()
```

### Dictionary Comprehensions
```python
# Basic comprehension
squares = {x: x**2 for x in range(5)}
# {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}

# With condition
even_squares = {x: x**2 for x in range(10) if x % 2 == 0}
# {0: 0, 2: 4, 4: 16, 6: 36, 8: 64}

# Transform existing dict
prices = {"apple": 1.0, "banana": 0.5}
doubled = {k: v * 2 for k, v in prices.items()}
# {'apple': 2.0, 'banana': 1.0}
```

### Iterating
```python
person = {"name": "Alice", "age": 25}

# Over keys (default)
for key in person:
    print(key)

# Over values
for value in person.values():
    print(value)

# Over key-value pairs
for key, value in person.items():
    print(f"{key}: {value}")
```

### Merging Dictionaries
```python
dict1 = {"a": 1, "b": 2}
dict2 = {"b": 3, "c": 4}

# Python 3.9+ - Union operator
merged = dict1 | dict2     # {'a': 1, 'b': 3, 'c': 4}

# Python 3.5+ - Unpacking
merged = {**dict1, **dict2}

# Update method (modifies dict1)
dict1.update(dict2)
```

### Nested Dictionaries
```python
students = {
    "alice": {
        "age": 20,
        "grades": {"math": 90, "english": 85}
    },
    "bob": {
        "age": 22,
        "grades": {"math": 78, "english": 92}
    }
}

# Access nested values
alice_math = students["alice"]["grades"]["math"]  # 90
```

### Time Complexity
- Get/Set/Delete: O(1) average
- Iteration: O(n)
- Space: O(n)""",

    # =========================================================================
    # COMPREHENSIONS
    # =========================================================================
    
    "comprehension": """## 🔄 Comprehensions in Python

**Definition:** Comprehensions provide a concise way to create lists, dictionaries, sets, and generators from iterables.

### List Comprehension
```python
# Basic syntax: [expression for item in iterable]
squares = [x**2 for x in range(10)]
# [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

# With condition: [expression for item in iterable if condition]
evens = [x for x in range(20) if x % 2 == 0]
# [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]

# With if-else (in expression, not filter)
labels = ["even" if x % 2 == 0 else "odd" for x in range(5)]
# ['even', 'odd', 'even', 'odd', 'even']

# Nested loops
pairs = [(x, y) for x in range(3) for y in range(3)]
# [(0,0), (0,1), (0,2), (1,0), (1,1), (1,2), (2,0), (2,1), (2,2)]

# Flatten nested list
matrix = [[1, 2], [3, 4], [5, 6]]
flat = [num for row in matrix for num in row]
# [1, 2, 3, 4, 5, 6]
```

### Dictionary Comprehension
```python
# Basic syntax: {key: value for item in iterable}
squares = {x: x**2 for x in range(5)}
# {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}

# From two lists
keys = ["a", "b", "c"]
values = [1, 2, 3]
d = {k: v for k, v in zip(keys, values)}
# {'a': 1, 'b': 2, 'c': 3}

# Swap keys and values
original = {"a": 1, "b": 2}
swapped = {v: k for k, v in original.items()}
# {1: 'a', 2: 'b'}

# Filter dictionary
scores = {"alice": 85, "bob": 60, "charlie": 90}
passed = {k: v for k, v in scores.items() if v >= 70}
# {'alice': 85, 'charlie': 90}
```

### Set Comprehension
```python
# Basic syntax: {expression for item in iterable}
unique_squares = {x**2 for x in [-2, -1, 0, 1, 2]}
# {0, 1, 4}

# From string (unique characters)
unique_chars = {char.lower() for char in "Hello World"}
# {'h', 'e', 'l', 'o', ' ', 'w', 'r', 'd'}
```

### Generator Expression
```python
# Basic syntax: (expression for item in iterable)
# Uses parentheses, creates generator (memory efficient)

squares_gen = (x**2 for x in range(1000000))
# Doesn't compute all values at once!

# Use in functions
sum_of_squares = sum(x**2 for x in range(10))
# 285

# Check if any/all
has_even = any(x % 2 == 0 for x in [1, 3, 4, 5])
# True
all_positive = all(x > 0 for x in [1, 2, 3, 4])
# True
```

### Comparison
| Type | Syntax | Returns | Memory |
|------|--------|---------|--------|
| List | `[x for x]` | list | All at once |
| Dict | `{k: v for k, v}` | dict | All at once |
| Set | `{x for x}` | set | All at once |
| Generator | `(x for x)` | generator | One at a time |

### Real-World Examples
```python
# Parse CSV-like data
data = "alice,25\\nbob,30\\ncharlie,35"
people = [
    {"name": line.split(",")[0], "age": int(line.split(",")[1])}
    for line in data.split("\\n")
]

# Filter and transform
words = ["hello", "world", "python", "programming"]
long_upper = [w.upper() for w in words if len(w) > 5]
# ['PYTHON', 'PROGRAMMING']

# Nested data extraction
users = [
    {"name": "Alice", "emails": ["a@x.com", "a@y.com"]},
    {"name": "Bob", "emails": ["b@x.com"]}
]
all_emails = [email for user in users for email in user["emails"]]
# ['a@x.com', 'a@y.com', 'b@x.com']
```""",

    # =========================================================================
    # GENERATORS
    # =========================================================================
    
    "generator": """## ⚡ Generators in Python

**Definition:** Generators are functions that yield values one at a time, allowing iteration without storing all values in memory.

### Generator Functions
```python
# Use 'yield' instead of 'return'
def count_up(n):
    i = 0
    while i < n:
        yield i
        i += 1

# Using the generator
for num in count_up(5):
    print(num)  # 0, 1, 2, 3, 4

# Or manually
gen = count_up(3)
print(next(gen))  # 0
print(next(gen))  # 1
print(next(gen))  # 2
# print(next(gen))  # StopIteration error
```

### Generator Expressions
```python
# Similar to list comprehension but with parentheses
squares_gen = (x**2 for x in range(1000000))
# Memory efficient - values computed on demand

# Convert to list if needed
first_10 = list(x**2 for x in range(10))
```

### Why Use Generators?
```python
# Memory comparison
import sys

# List - stores all values
list_comp = [x**2 for x in range(10000)]
print(sys.getsizeof(list_comp))  # ~87,624 bytes

# Generator - stores only the recipe
gen_exp = (x**2 for x in range(10000))
print(sys.getsizeof(gen_exp))    # ~112 bytes
```

### Infinite Generators
```python
def infinite_counter():
    n = 0
    while True:
        yield n
        n += 1

# Use with caution!
counter = infinite_counter()
for i, num in enumerate(counter):
    print(num)
    if i >= 4:
        break  # 0, 1, 2, 3, 4

def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

# Get first 10 Fibonacci numbers
fib = fibonacci()
first_10 = [next(fib) for _ in range(10)]
# [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
```

### yield from
```python
# Delegate to another generator
def nested_gen():
    yield from range(3)      # 0, 1, 2
    yield from range(10, 13) # 10, 11, 12

list(nested_gen())  # [0, 1, 2, 10, 11, 12]

# Flatten nested lists
def flatten(nested):
    for item in nested:
        if isinstance(item, list):
            yield from flatten(item)
        else:
            yield item

nested = [1, [2, 3, [4, 5]], 6]
list(flatten(nested))  # [1, 2, 3, 4, 5, 6]
```

### Generator Methods
```python
def generator_with_send():
    value = yield "Ready"
    while True:
        value = yield f"Received: {value}"

gen = generator_with_send()
print(next(gen))        # "Ready"
print(gen.send("Hello")) # "Received: Hello"
print(gen.send("World")) # "Received: World"
gen.close()              # Close the generator
```

### Real-World Examples
```python
# Read large file line by line
def read_large_file(file_path):
    with open(file_path, 'r') as f:
        for line in f:
            yield line.strip()

# Process without loading entire file
for line in read_large_file('huge_file.txt'):
    process(line)

# Paginated API results
def get_all_pages(api_url):
    page = 1
    while True:
        data = fetch_page(api_url, page)
        if not data:
            break
        yield from data
        page += 1
```""",

    # =========================================================================
    # LAMBDA FUNCTIONS
    # =========================================================================
    
    "lambda": """## λ Lambda Functions in Python

**Definition:** Lambda functions are small, anonymous functions defined with the `lambda` keyword.

### Basic Syntax
```python
# lambda arguments: expression
# Equivalent to:
# def func(arguments):
#     return expression

# Simple lambda
square = lambda x: x ** 2
print(square(5))  # 25

# Multiple arguments
add = lambda x, y: x + y
print(add(3, 4))  # 7

# No arguments
greet = lambda: "Hello!"
print(greet())  # "Hello!"
```

### Lambda vs Regular Function
```python
# Lambda
multiply = lambda x, y: x * y

# Equivalent regular function
def multiply(x, y):
    return x * y

# Lambda limitations:
# - Single expression only
# - No statements (no if-else blocks, loops)
# - No annotations
# - Harder to debug (no name in traceback)
```

### Common Use Cases

#### 1. With sorted()
```python
# Sort by specific key
students = [
    {"name": "Alice", "grade": 85},
    {"name": "Bob", "grade": 90},
    {"name": "Charlie", "grade": 78}
]

# Sort by grade
by_grade = sorted(students, key=lambda s: s["grade"])

# Sort by name (case-insensitive)
names = ["Alice", "bob", "Charlie"]
sorted_names = sorted(names, key=lambda x: x.lower())

# Sort tuples by second element
pairs = [(1, 'b'), (2, 'a'), (3, 'c')]
sorted_pairs = sorted(pairs, key=lambda x: x[1])
```

#### 2. With map()
```python
# Apply function to all elements
numbers = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x**2, numbers))
# [1, 4, 9, 16, 25]

# Convert strings to int
str_nums = ["1", "2", "3"]
int_nums = list(map(lambda x: int(x), str_nums))
# Or simpler: list(map(int, str_nums))
```

#### 3. With filter()
```python
# Filter elements
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
evens = list(filter(lambda x: x % 2 == 0, numbers))
# [2, 4, 6, 8, 10]

# Filter non-empty strings
strings = ["hello", "", "world", "", "python"]
non_empty = list(filter(lambda s: s, strings))
# ["hello", "world", "python"]
```

#### 4. With reduce()
```python
from functools import reduce

# Reduce to single value
numbers = [1, 2, 3, 4, 5]
product = reduce(lambda x, y: x * y, numbers)
# 120 (1 * 2 * 3 * 4 * 5)

# Find maximum
maximum = reduce(lambda x, y: x if x > y else y, numbers)
# 5
```

### Conditional in Lambda
```python
# Ternary operator in lambda
classify = lambda x: "positive" if x > 0 else "non-positive"
print(classify(5))   # "positive"
print(classify(-3))  # "non-positive"

# More complex (but harder to read)
grade = lambda score: "A" if score >= 90 else ("B" if score >= 80 else "C")
```

### When NOT to Use Lambda
```python
# ❌ Don't assign lambda to variable for reuse
bad = lambda x: x * 2

# ✓ Use regular function instead
def double(x):
    return x * 2

# ❌ Don't use lambda for complex logic
# ✓ Use regular function with proper name

# ❌ Avoid nested lambdas (hard to read)
# ✓ Use regular functions
```""",

    # =========================================================================
    # TYPE HINTS
    # =========================================================================
    
    "type hint": """## 🏷️ Type Hints in Python

**Definition:** Type hints (annotations) specify the expected types of variables, function parameters, and return values.

### Basic Type Hints
```python
# Variable annotations
name: str = "Alice"
age: int = 25
price: float = 19.99
is_active: bool = True

# Function annotations
def greet(name: str) -> str:
    return f"Hello, {name}!"

def add(a: int, b: int) -> int:
    return a + b

# No return value (None)
def print_message(msg: str) -> None:
    print(msg)
```

### Collection Types
```python
from typing import List, Dict, Set, Tuple, Optional

# Lists
def get_names() -> List[str]:
    return ["Alice", "Bob"]

# Dictionaries
def get_scores() -> Dict[str, int]:
    return {"Alice": 90, "Bob": 85}

# Sets
def unique_numbers() -> Set[int]:
    return {1, 2, 3}

# Tuples (fixed length and types)
def get_point() -> Tuple[int, int]:
    return (10, 20)

# Python 3.9+ (no import needed)
def modern_types() -> list[str]:
    return ["a", "b"]
```

### Optional and Union
```python
from typing import Optional, Union

# Optional - can be None
def find_user(id: int) -> Optional[str]:
    # Returns str or None
    if id == 1:
        return "Alice"
    return None

# Union - multiple possible types
def process(value: Union[int, str]) -> str:
    return str(value)

# Python 3.10+ syntax
def modern_union(value: int | str) -> str:
    return str(value)
```

### Callable and Any
```python
from typing import Callable, Any

# Function as parameter
def apply(func: Callable[[int, int], int], a: int, b: int) -> int:
    return func(a, b)

result = apply(lambda x, y: x + y, 3, 4)  # 7

# Any type (avoid if possible)
def accept_anything(value: Any) -> None:
    print(value)
```

### Type Aliases
```python
from typing import List, Dict

# Create type aliases for complex types
Vector = List[float]
Matrix = List[List[float]]
UserData = Dict[str, Union[str, int]]

def scale(vector: Vector, scalar: float) -> Vector:
    return [x * scalar for x in vector]

def get_user() -> UserData:
    return {"name": "Alice", "age": 25}
```

### Generic Types
```python
from typing import TypeVar, Generic, List

T = TypeVar('T')

# Generic function
def first(items: List[T]) -> T:
    return items[0]

# Generic class
class Stack(Generic[T]):
    def __init__(self) -> None:
        self.items: List[T] = []
    
    def push(self, item: T) -> None:
        self.items.append(item)
    
    def pop(self) -> T:
        return self.items.pop()

# Usage
int_stack: Stack[int] = Stack()
int_stack.push(1)
```

### Type Checking Tools
```bash
# Install mypy
pip install mypy

# Run type checker
mypy your_file.py
```

### Benefits of Type Hints
```
✓ Better IDE support (autocomplete, refactoring)
✓ Catch bugs early (with type checkers)
✓ Self-documenting code
✓ Easier maintenance
✓ No runtime overhead (hints are ignored at runtime)
```""",

    # =========================================================================
    # CONTEXT MANAGERS
    # =========================================================================
    
    "context manager": """## 🔐 Context Managers in Python

**Definition:** Context managers handle setup and cleanup of resources automatically using `with` statements.

### Basic Usage
```python
# File handling - automatic close
with open("file.txt", "r") as f:
    content = f.read()
# File automatically closed, even if exception occurs

# Without context manager (risky)
f = open("file.txt", "r")
try:
    content = f.read()
finally:
    f.close()  # Easy to forget!
```

### Creating Context Managers

#### Method 1: Class-based
```python
class FileManager:
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode
        self.file = None
    
    def __enter__(self):
        self.file = open(self.filename, self.mode)
        return self.file
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()
        # Return True to suppress exception, False to propagate
        return False

# Usage
with FileManager("test.txt", "w") as f:
    f.write("Hello, World!")
```

#### Method 2: Using contextlib
```python
from contextlib import contextmanager

@contextmanager
def file_manager(filename, mode):
    f = open(filename, mode)
    try:
        yield f  # This is what 'with' receives
    finally:
        f.close()

# Usage
with file_manager("test.txt", "w") as f:
    f.write("Hello!")
```

### Common Context Managers
```python
# 1. File operations
with open("file.txt") as f:
    data = f.read()

# 2. Database connections
import sqlite3
with sqlite3.connect("database.db") as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")

# 3. Locks (threading)
import threading
lock = threading.Lock()
with lock:
    # Thread-safe code
    shared_data += 1

# 4. Temporary directory
import tempfile
with tempfile.TemporaryDirectory() as tmpdir:
    # tmpdir is auto-deleted after
    pass

# 5. Suppress exceptions
from contextlib import suppress
with suppress(FileNotFoundError):
    os.remove("missing.txt")  # No error if file missing
```

### Multiple Context Managers
```python
# Multiple files at once
with open("input.txt") as infile, open("output.txt", "w") as outfile:
    outfile.write(infile.read().upper())

# Python 3.10+ parenthesized form
with (
    open("file1.txt") as f1,
    open("file2.txt") as f2,
    open("file3.txt") as f3
):
    pass
```

### Timer Context Manager
```python
import time
from contextlib import contextmanager

@contextmanager
def timer(label):
    start = time.time()
    try:
        yield
    finally:
        elapsed = time.time() - start
        print(f"{label}: {elapsed:.4f} seconds")

# Usage
with timer("Processing"):
    # Some operation
    time.sleep(1)
# Output: Processing: 1.0012 seconds
```

### Database Transaction Manager
```python
@contextmanager
def transaction(connection):
    cursor = connection.cursor()
    try:
        yield cursor
        connection.commit()
    except Exception:
        connection.rollback()
        raise

# Usage
with transaction(db_conn) as cursor:
    cursor.execute("INSERT INTO users VALUES (?)", ("Alice",))
    cursor.execute("UPDATE accounts SET balance = 100")
# Auto-commit on success, rollback on error
```""",

    # =========================================================================
    # TESTING IN PYTHON
    # =========================================================================
    
    "testing": """## 🧪 Testing in Python

**Definition:** Testing is the practice of writing code to verify that your software works correctly.

### unittest (Built-in)
```python
import unittest

def add(a, b):
    return a + b

class TestAddFunction(unittest.TestCase):
    def test_add_positive(self):
        self.assertEqual(add(2, 3), 5)
    
    def test_add_negative(self):
        self.assertEqual(add(-1, 1), 0)
    
    def test_add_floats(self):
        self.assertAlmostEqual(add(0.1, 0.2), 0.3, places=5)
    
    def setUp(self):
        # Runs before each test
        pass
    
    def tearDown(self):
        # Runs after each test
        pass

if __name__ == "__main__":
    unittest.main()
```

### pytest (Popular Third-Party)
```python
# pip install pytest

def add(a, b):
    return a + b

# Simple test functions
def test_add_positive():
    assert add(2, 3) == 5

def test_add_negative():
    assert add(-1, 1) == 0

# Test with parameters
import pytest

@pytest.mark.parametrize("a,b,expected", [
    (2, 3, 5),
    (-1, 1, 0),
    (0, 0, 0),
])
def test_add_parametrized(a, b, expected):
    assert add(a, b) == expected

# Test exceptions
def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

def test_divide_by_zero():
    with pytest.raises(ValueError):
        divide(10, 0)
```

### Common Assertions (unittest)
```python
# Equality
self.assertEqual(a, b)       # a == b
self.assertNotEqual(a, b)    # a != b

# Boolean
self.assertTrue(x)           # x is True
self.assertFalse(x)          # x is False

# None
self.assertIsNone(x)         # x is None
self.assertIsNotNone(x)      # x is not None

# Type/Instance
self.assertIsInstance(x, type)
self.assertIs(a, b)          # a is b (same object)

# Containers
self.assertIn(a, b)          # a in b
self.assertNotIn(a, b)       # a not in b

# Comparison
self.assertGreater(a, b)     # a > b
self.assertLess(a, b)        # a < b

# Exceptions
self.assertRaises(Exception, func, args)
```

### Fixtures (pytest)
```python
import pytest

@pytest.fixture
def sample_data():
    return {"name": "Alice", "age": 25}

@pytest.fixture
def database():
    db = create_db()
    yield db  # Test runs here
    db.close()  # Cleanup after test

def test_user_name(sample_data):
    assert sample_data["name"] == "Alice"

def test_database_query(database):
    result = database.query("SELECT * FROM users")
    assert len(result) > 0
```

### Mocking
```python
from unittest.mock import Mock, patch

# Mock object
mock_api = Mock()
mock_api.get_user.return_value = {"name": "Alice"}
result = mock_api.get_user(1)
assert result["name"] == "Alice"

# Patch (replace during test)
@patch("module.external_api_call")
def test_with_patch(mock_call):
    mock_call.return_value = "mocked response"
    result = function_that_uses_api()
    assert result == "mocked response"
```

### Running Tests
```bash
# unittest
python -m unittest test_module.py
python -m unittest discover  # Find all tests

# pytest
pytest                    # Run all tests
pytest test_file.py       # Run specific file
pytest -v                 # Verbose output
pytest -k "test_add"      # Run tests matching pattern
pytest --cov=mymodule     # Code coverage
```

### Test Structure (AAA Pattern)
```python
def test_user_registration():
    # Arrange - Set up test data
    user_data = {"name": "Alice", "email": "alice@example.com"}
    
    # Act - Perform the action
    result = register_user(user_data)
    
    # Assert - Verify the result
    assert result.success == True
    assert result.user.name == "Alice"
```"""
}

# =============================================================================
# COMMON MISTAKES DATABASE
# =============================================================================

COMMON_MISTAKES = {
    r"print\s*\(": {
        "issue": "Using `print()` instead of `return`",
        "fix": "The tests check return values. Replace `print(result)` with `return result`",
        "example": "```python\n# Wrong\ndef add(a, b):\n    print(a + b)\n\n# Correct\ndef add(a, b):\n    return a + b\n```"
    },
    r"def\s+\w+\s*\(\s*\)\s*:": {
        "issue": "Function defined with no parameters",
        "fix": "Your function needs parameters to receive input. Check the expected function signature.",
        "example": "```python\n# Wrong\ndef solve():\n    pass\n\n# Correct\ndef solve(n):\n    pass\n```"
    },
    r"\.sort\(\)(?!\s*\))": {
        "issue": "`.sort()` returns None",
        "fix": "`.sort()` modifies the list in-place and returns None. Use `sorted()` if you need a new list.",
        "example": "```python\n# Wrong\nresult = nums.sort()  # result is None!\n\n# Correct\nnums.sort()  # modifies nums\nresult = nums\n\n# Or use sorted\nresult = sorted(nums)\n```"
    },
    r"(\w+)\s*=\s*(\w+)\s*=": {
        "issue": "Possible variable aliasing issue",
        "fix": "Multiple assignment creates references to the same object for mutable types.",
        "example": "```python\n# Be careful with\na = b = []  # a and b point to same list!\na.append(1)  # b is also affected\n\n# Safe\na = []\nb = []\n```"
    },
    r"for\s+\w+\s+in\s+range\s*\(\s*len\s*\(": {
        "issue": "Using `for i in range(len(...))`",
        "fix": "This is often unnecessary. Use `enumerate()` if you need both index and value.",
        "example": "```python\n# Less Pythonic\nfor i in range(len(items)):\n    print(i, items[i])\n\n# More Pythonic\nfor i, item in enumerate(items):\n    print(i, item)\n```"
    },
    r"if\s+\w+\s*==\s*True": {
        "issue": "Comparing to `True` explicitly",
        "fix": "Just use the condition directly for boolean values.",
        "example": "```python\n# Unnecessary\nif is_valid == True:\n\n# Better\nif is_valid:\n```"
    },
    r"if\s+\w+\s*==\s*None": {
        "issue": "Using `==` for None comparison",
        "fix": "Use `is None` or `is not None` for None checks.",
        "example": "```python\n# Wrong\nif x == None:\n\n# Correct\nif x is None:\n```"
    },
    r"\[\s*\]\s*\+\s*\[": {
        "issue": "Concatenating lists in a loop",
        "fix": "List concatenation creates new lists. Use `.append()` or `.extend()` instead.",
        "example": "```python\n# Slow - O(n²)\nresult = []\nfor item in items:\n    result = result + [item]\n\n# Fast - O(n)\nresult = []\nfor item in items:\n    result.append(item)\n```"
    }
}

# =============================================================================
# PROBLEM-SPECIFIC HINTS
# =============================================================================

PROBLEM_HINTS = {
    "sum": {
        "concept": "Accumulation",
        "hints": [
            "Use a variable to keep track of the running total",
            "Initialize your sum variable to 0 before the loop",
            "Python's built-in `sum()` function can do this in one line",
            "For specific ranges, use `sum(range(start, end))`"
        ],
        "template": """def sum_numbers(n):
    total = 0
    for i in range(1, n + 1):
        total += i
    return total
    # Or simply: return sum(range(1, n + 1))"""
    },
    "reverse": {
        "concept": "String/List manipulation",
        "hints": [
            "Python supports negative slicing: `s[::-1]`",
            "You can use a two-pointer approach swapping elements",
            "For lists, you can use `.reverse()` method (in-place)",
            "`reversed()` returns an iterator you can convert to list"
        ],
        "template": """# Method 1: Slicing
def reverse(s):
    return s[::-1]

# Method 2: Two pointers (for in-place)
def reverse_list(arr):
    left, right = 0, len(arr) - 1
    while left < right:
        arr[left], arr[right] = arr[right], arr[left]
        left += 1
        right -= 1"""
    },
    "palindrome": {
        "concept": "String comparison",
        "hints": [
            "A palindrome reads the same forwards and backwards",
            "Compare the string with its reverse",
            "Two pointers can check without extra space",
            "Consider case sensitivity and non-alphanumeric characters"
        ],
        "template": """# Simple approach
def is_palindrome(s):
    return s == s[::-1]

# Two pointers
def is_palindrome(s):
    left, right = 0, len(s) - 1
    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1
    return True"""
    },
    "factorial": {
        "concept": "Mathematical recursion/iteration",
        "hints": [
            "Factorial: n! = n × (n-1) × ... × 1",
            "Base case: 0! = 1 and 1! = 1",
            "Can be solved with recursion or a simple loop",
            "Python's `math.factorial()` is built-in"
        ],
        "template": """# Iterative
def factorial(n):
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

# Recursive
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)"""
    },
    "fibonacci": {
        "concept": "Sequence generation",
        "hints": [
            "F(n) = F(n-1) + F(n-2) with F(0)=0, F(1)=1",
            "Simple recursion is O(2^n) - very slow!",
            "Use iteration or memoization for O(n)",
            "You only need to track the last two numbers"
        ],
        "template": """# Efficient iterative
def fibonacci(n):
    if n <= 1:
        return n
    
    prev2, prev1 = 0, 1
    for _ in range(2, n + 1):
        prev2, prev1 = prev1, prev2 + prev1
    return prev1

# With memoization
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n):
    if n <= 1:
        return n
    return fib(n-1) + fib(n-2)"""
    },
    "prime": {
        "concept": "Number theory",
        "hints": [
            "A prime has exactly 2 factors: 1 and itself",
            "Only check up to √n (if no divisor found, it's prime)",
            "2 is the only even prime",
            "Handle edge cases: 0, 1, negative numbers are not prime"
        ],
        "template": """def is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True"""
    },
    "max": {
        "concept": "Finding extremes",
        "hints": [
            "Initialize with first element or negative infinity",
            "Track maximum as you iterate",
            "Python's `max()` function does this"
        ],
        "template": """def find_max(arr):
    if not arr:
        return None
    
    maximum = arr[0]
    for num in arr[1:]:
        if num > maximum:
            maximum = num
    return maximum
    # Or simply: return max(arr)"""
    },
    "min": {
        "concept": "Finding extremes",
        "hints": [
            "Initialize with first element or positive infinity",
            "Track minimum as you iterate",
            "Python's `min()` function does this"
        ],
        "template": """def find_min(arr):
    if not arr:
        return None
    
    minimum = arr[0]
    for num in arr[1:]:
        if num < minimum:
            minimum = num
    return minimum
    # Or simply: return min(arr)"""
    },
    "count": {
        "concept": "Frequency counting",
        "hints": [
            "Use a dictionary to store counts",
            "`collections.Counter` is perfect for this",
            "`.get(key, 0)` avoids KeyError",
            "For single item count, use `.count()` method"
        ],
        "template": """# Using dictionary
def count_chars(s):
    counts = {}
    for char in s:
        counts[char] = counts.get(char, 0) + 1
    return counts

# Using Counter
from collections import Counter
def count_chars(s):
    return dict(Counter(s))"""
    },
    "duplicate": {
        "concept": "Set operations",
        "hints": [
            "Sets only store unique elements",
            "Compare `len(list)` vs `len(set(list))`",
            "Track seen elements in a set",
            "O(n) time with O(n) space using set"
        ],
        "template": """# Check for duplicates
def has_duplicates(arr):
    return len(arr) != len(set(arr))

# Find duplicates
def find_duplicates(arr):
    seen = set()
    duplicates = []
    for item in arr:
        if item in seen:
            duplicates.append(item)
        else:
            seen.add(item)
    return duplicates"""
    },
    "anagram": {
        "concept": "Character comparison",
        "hints": [
            "Anagrams have same characters in different order",
            "Sort both strings and compare",
            "Or count character frequencies",
            "Consider case sensitivity"
        ],
        "template": """# Sorting approach
def is_anagram(s1, s2):
    return sorted(s1.lower()) == sorted(s2.lower())

# Counting approach
from collections import Counter
def is_anagram(s1, s2):
    return Counter(s1.lower()) == Counter(s2.lower())"""
    },
    "sort": {
        "concept": "Ordering elements",
        "hints": [
            "Python's built-in sort is highly optimized (Timsort)",
            "`.sort()` is in-place, `sorted()` returns new list",
            "Use `key` parameter for custom sorting",
            "Consider if you need stable sort"
        ],
        "template": """# Built-in sorting
arr.sort()                       # In-place, ascending
arr.sort(reverse=True)           # In-place, descending
sorted_arr = sorted(arr)         # New list
sorted_by_len = sorted(strings, key=len)"""
    },
    "binary": {
        "concept": "Number systems",
        "hints": [
            "`bin(n)` converts to binary string (prefixed with '0b')",
            "Binary digits via repeated `% 2` and `// 2`",
            "`int('1010', 2)` converts binary string to int",
            "Bitwise operators: `&`, `|`, `^`, `<<`, `>>`"
        ],
        "template": """# To binary string
def to_binary(n):
    return bin(n)[2:]  # Remove '0b' prefix

# Manual conversion
def to_binary_manual(n):
    if n == 0:
        return '0'
    bits = []
    while n:
        bits.append(str(n % 2))
        n //= 2
    return ''.join(reversed(bits))"""
    }
}

# =============================================================================
# INTERVIEW QUESTIONS DATABASE
# =============================================================================

INTERVIEW_QUESTIONS = [
    # Easy
    {"q": "What's the time complexity of your solution? Can you explain why?", "level": "easy"},
    {"q": "Are there any edge cases you should handle? What are they?", "level": "easy"},
    {"q": "Can you walk me through your solution step by step?", "level": "easy"},
    {"q": "What happens if the input is empty? Does your solution handle it?", "level": "easy"},
    
    # Medium
    {"q": "Is there a more efficient solution? What trade-offs would it have?", "level": "medium"},
    {"q": "What's the space complexity? Can you reduce it?", "level": "medium"},
    {"q": "How would your solution scale with input 10x or 100x larger?", "level": "medium"},
    {"q": "What data structures did you consider? Why did you choose this one?", "level": "medium"},
    {"q": "Can you solve this without using extra space?", "level": "medium"},
    
    # Hard
    {"q": "How would you modify this to handle concurrent access?", "level": "hard"},
    {"q": "What if we needed to support streaming input?", "level": "hard"},
    {"q": "How would you test this thoroughly? What test cases would you write?", "level": "hard"},
    {"q": "Can you implement this using a different algorithm paradigm?", "level": "hard"},
]

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def analyze_code(code: str) -> List[Dict]:
    """Analyze code for common mistakes and provide detailed feedback."""
    issues = []
    
    for pattern, info in COMMON_MISTAKES.items():
        if re.search(pattern, code, re.IGNORECASE):
            issues.append(info)
    
    # Check for missing return
    if "def " in code and "return" not in code:
        issues.append({
            "issue": "No return statement found",
            "fix": "Make sure your function returns a value instead of printing it.",
            "example": "Add `return result` at the end of your function."
        })
    
    return issues[:3]  # Return top 3 issues


def get_problem_hints(question: str, function_name: str) -> Dict:
    """Get comprehensive hints based on problem keywords."""
    text = (question + " " + function_name).lower()
    
    for keyword, data in PROBLEM_HINTS.items():
        if keyword in text:
            return data
    
    return {
        "concept": "General problem solving",
        "hints": [
            "Break the problem into smaller steps",
            "Think about what data structure would help",
            "Consider edge cases first",
            "Start with the simplest solution"
        ]
    }


def get_concept_explanation(topic: str) -> Optional[str]:
    """
    Get detailed explanation for a programming concept.
    Uses well-structured manual concepts first, PDF as fallback for other topics.
    """
    topic_lower = topic.lower()
    
    # First check manual concepts (these are well-structured and clear)
    for key, explanation in CONCEPTS.items():
        if key in topic_lower:
            return explanation
    
    # For topics not in manual concepts, try PDF knowledge base
    if PDF_KB_AVAILABLE:
        pdf_answer = query_pdf_knowledge(f"What is {topic} in Python? Explain {topic}.")
        if pdf_answer:
            return pdf_answer
    
    return None


def extract_keywords(text: str) -> List[str]:
    """Extract key programming concepts from text."""
    keywords = []
    concept_list = list(CONCEPTS.keys()) + list(PROBLEM_HINTS.keys())
    
    for concept in concept_list:
        if concept in text.lower():
            keywords.append(concept)
    
    return keywords


# =============================================================================
# MAIN RESPONSE GENERATION
# =============================================================================

def _find_concept_answer(topic: str) -> Optional[str]:
    """Find the best matching concept answer for a single topic."""
    topic_lower = topic.lower().strip()
    
    # Helper function to check if words match (including plurals)
    def words_match(word1, word2):
        w1, w2 = word1.lower(), word2.lower()
        if w1 == w2:
            return True
        if w1 + 's' == w2 or w2 + 's' == w1:
            return True
        if w1 + 'es' == w2 or w2 + 'es' == w1:
            return True
        if w1.rstrip('ies') + 'y' == w2 or w2.rstrip('ies') + 'y' == w1:
            return True
        return False
    
    topic_words = topic_lower.split()
    
    # Common Python terms - prefer Python CONCEPTS over automation
    python_priority_terms = ['class', 'object', 'function', 'method', 'variable', 'loop', 
                             'list', 'dict', 'tuple', 'set', 'string', 'integer', 'float',
                             'exception', 'import', 'module', 'decorator', 'generator',
                             'iterator', 'comprehension', 'lambda', 'inheritance', 'polymorphism']
    
    # Automation keywords - use automation concepts
    automation_keywords = ['selenium', 'webdriver', 'robot', 'xpath', 'locator', 'browser',
                           'element', 'wait', 'grid', 'pytest', 'fixture', 'allure', 
                           'jenkins', 'docker', 'pom', 'page object']
    
    is_python_term = topic_lower in python_priority_terms or any(t in python_priority_terms for t in topic_words)
    is_automation_term = any(kw in topic_lower for kw in automation_keywords)
    
    # Check Python CONCEPTS first if it's a common Python term (and not explicitly automation)
    if is_python_term and not is_automation_term:
        best_match = None
        best_score = 0
        
        for concept_key in CONCEPTS.keys():
            score = 0
            concept_words_list = concept_key.split()
            
            if concept_key == topic_lower:
                score = 100
            elif concept_key in topic_words:
                score = 95
            elif len(concept_words_list) > 1 and concept_key in topic_lower:
                score = 90
            elif any(words_match(concept_key, tw) for tw in topic_words):
                score = 85
            elif any(concept_key in tw or tw in concept_key for tw in topic_words):
                score = 70 + len(concept_key)
            elif concept_key in topic_lower:
                score = 50 + len(concept_key)
            
            if score > best_score:
                best_score = score
                best_match = concept_key
        
        if best_match and best_score > 0:
            return CONCEPTS[best_match]
    
    # Check automation concepts (Selenium, Robot Framework, etc.)
    if AUTOMATION_CONCEPTS_AVAILABLE:
        auto_answer = _match_automation_concept(topic, topic_words)
        if auto_answer:
            return auto_answer
    
    # Check advanced concepts (async, dataclass, pathlib, etc.)
    if ADVANCED_CONCEPTS_AVAILABLE:
        for concept_key in ADVANCED_CONCEPTS.keys():
            if concept_key in topic_lower or topic_lower in concept_key:
                return ADVANCED_CONCEPTS[concept_key]
            # Also check for word matches
            for tw in topic_words:
                if concept_key == tw or concept_key in tw or tw in concept_key:
                    return ADVANCED_CONCEPTS[concept_key]
    
    # Check infrastructure concepts (networking, servers, storage)
    if INFRASTRUCTURE_CONCEPTS_AVAILABLE:
        for concept_key in INFRASTRUCTURE_CONCEPTS.keys():
            if concept_key in topic_lower or topic_lower in concept_key:
                return INFRASTRUCTURE_CONCEPTS[concept_key]
            for tw in topic_words:
                if concept_key == tw or concept_key in tw or tw in concept_key:
                    return INFRASTRUCTURE_CONCEPTS[concept_key]
    
    # Check Linux concepts
    if LINUX_CONCEPTS_AVAILABLE:
        for concept_key in LINUX_CONCEPTS.keys():
            if concept_key in topic_lower or topic_lower in concept_key:
                return LINUX_CONCEPTS[concept_key]
            for tw in topic_words:
                if concept_key == tw or concept_key in tw or tw in concept_key:
                    return LINUX_CONCEPTS[concept_key]
    
    # Fallback: Find best matching concept from CONCEPTS
    best_match = None
    best_score = 0
    
    for concept_key in CONCEPTS.keys():
        score = 0
        concept_words_list = concept_key.split()
        
        if concept_key == topic_lower:
            score = 100
        elif concept_key in topic_words:
            score = 95
        elif len(concept_words_list) > 1 and concept_key in topic_lower:
            score = 90
        elif any(words_match(concept_key, tw) for tw in topic_words):
            score = 85
        elif any(concept_key in tw or tw in concept_key for tw in topic_words):
            score = 70 + len(concept_key)
        elif concept_key in topic_lower:
            score = 50 + len(concept_key)
        
        if score > best_score:
            best_score = score
            best_match = concept_key
    
    if best_match and best_score > 0:
        return CONCEPTS[best_match]
    return None


def _handle_multiple_topics(user_message: str) -> Optional[str]:
    """
    Detect and handle multiple topics in a single message.
    Returns combined answers or None if not a multi-topic query.
    """
    msg_lower = user_message.lower()
    
    # Skip if message contains context markers (indicates concatenated message from UI)
    context_markers = ["previous conversation:", "current question:", "be concise", 
                       "bullet points", "keep under", "assistant:", "user:"]
    if any(marker in msg_lower for marker in context_markers):
        return None
    
    # Skip very long messages (likely contain context/conversation history)
    if len(user_message) > 300:
        return None
    
    # Check if this looks like multiple topics
    # Patterns: "explain X, Y, Z" or "what is X and Y" or "X, Y, Z"
    has_comma = ',' in user_message
    has_and = ' and ' in msg_lower
    
    if not (has_comma or has_and):
        return None
    
    # Remove question keywords to get topics
    topic_part = msg_lower
    for kw in ["explain", "what is", "what are", "tell me about", "define", "describe", 
               "teach me", "how does", "how do", "?"]:
        topic_part = topic_part.replace(kw, " ")
    
    # Split by comma and "and"
    topic_part = topic_part.replace(" and ", ",")
    topics = [t.strip() for t in topic_part.split(",") if t.strip()]
    
    # Filter out empty/small topics
    topics = [t for t in topics if len(t) > 1]
    
    if len(topics) < 2:
        return None
    
    # Find answers for each topic
    answers = []
    found_topics = []
    
    for topic in topics:
        answer = _find_concept_answer(topic)
        if answer:
            answers.append(answer)
            found_topics.append(topic)
    
    if len(answers) < 2:
        return None  # Let normal flow handle it
    
    # Build combined response
    response = f"## 📚 Multiple Topics: {', '.join(found_topics).title()}\n\n"
    response += f"*Explaining {len(answers)} topics...*\n\n"
    response += "---\n\n"
    
    for i, answer in enumerate(answers):
        response += answer
        if i < len(answers) - 1:
            response += "\n\n---\n\n"
    
    return response


# =============================================================================
# CODE EXPLANATION FEATURE
# =============================================================================

def explain_code(code: str) -> str:
    """
    Generate a detailed line-by-line explanation of Python code.
    
    Args:
        code: Python code to explain
        
    Returns:
        Detailed explanation with line-by-line breakdown
    """
    if not code or not code.strip():
        return """## 📝 Code Explanation

I'd be happy to explain code for you! Please paste some Python code and I'll break it down line by line.

**Example request:**
```
Explain this code:
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```"""
    
    lines = code.strip().split('\n')
    
    # Analyze the code structure
    has_function = bool(re.search(r'\bdef\s+\w+\s*\(', code))
    has_class = bool(re.search(r'\bclass\s+\w+', code))
    has_loop = bool(re.search(r'\b(for|while)\b', code))
    has_conditional = bool(re.search(r'\bif\b', code))
    has_import = bool(re.search(r'\b(import|from)\b', code))
    has_list_comp = bool(re.search(r'\[.*for.*in.*\]', code))
    has_recursion = False
    
    # Detect function name and check for recursion
    func_match = re.search(r'def\s+(\w+)\s*\(', code)
    func_name = func_match.group(1) if func_match else None
    if func_name and func_name in code[code.find('def '):]:
        # Check if function calls itself
        has_recursion = bool(re.search(rf'\b{func_name}\s*\(', code[code.find('):'):]))
    
    response = "## 🔍 Code Explanation\n\n"
    
    # Overview
    response += "### Overview\n"
    if has_class:
        class_match = re.search(r'class\s+(\w+)', code)
        class_name = class_match.group(1) if class_match else "Class"
        response += f"This code defines a **class `{class_name}`**.\n\n"
    elif has_function:
        response += f"This code defines a **function `{func_name}`**.\n\n"
    else:
        response += "This is a **code snippet** with the following elements:\n\n"
    
    # Key concepts used
    concepts = []
    if has_function:
        concepts.append("Function definition")
    if has_class:
        concepts.append("Class/OOP")
    if has_loop:
        concepts.append("Loops")
    if has_conditional:
        concepts.append("Conditionals")
    if has_list_comp:
        concepts.append("List comprehension")
    if has_recursion:
        concepts.append("Recursion")
    if has_import:
        concepts.append("Module imports")
    
    if concepts:
        response += f"**Concepts used:** {', '.join(concepts)}\n\n"
    
    # Line-by-line explanation
    response += "### Line-by-Line Breakdown\n\n"
    response += "```python\n"
    
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped:
            response += f"{i}: {line}\n"
    
    response += "```\n\n"
    
    # Explain each significant line
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if not stripped or stripped.startswith('#'):
            continue
            
        explanation = _explain_line(stripped, i)
        if explanation:
            response += f"**Line {i}:** {explanation}\n\n"
    
    # Summary
    response += "### Summary\n"
    if has_recursion:
        response += f"- This is a **recursive function** - `{func_name}` calls itself\n"
        response += "- Make sure there's a base case to prevent infinite recursion\n"
    if has_loop and has_conditional:
        response += "- Uses iteration with conditional logic\n"
    if has_list_comp:
        response += "- Uses Pythonic list comprehension for concise code\n"
    
    response += "\n💡 **Need more detail on any part?** Just ask!"
    
    return response


def _explain_line(line: str, line_num: int) -> str:
    """Generate explanation for a single line of code."""
    
    # Function definition
    if line.startswith('def '):
        match = re.match(r'def\s+(\w+)\s*\((.*?)\)', line)
        if match:
            name, params = match.groups()
            param_list = [p.strip() for p in params.split(',') if p.strip()]
            if param_list:
                return f"Defines function `{name}` with parameters: `{', '.join(param_list)}`"
            return f"Defines function `{name}` with no parameters"
    
    # Class definition
    if line.startswith('class '):
        match = re.match(r'class\s+(\w+)(?:\((.*?)\))?', line)
        if match:
            name, parent = match.groups()
            if parent:
                return f"Defines class `{name}` inheriting from `{parent}`"
            return f"Defines class `{name}`"
    
    # Return statement
    if line.startswith('return '):
        value = line[7:].strip()
        return f"Returns the value: `{value}`"
    
    # If statement
    if line.startswith('if '):
        condition = line[3:].rstrip(':')
        return f"Checks condition: `{condition}`"
    
    # Elif statement
    if line.startswith('elif '):
        condition = line[5:].rstrip(':')
        return f"Alternative condition: `{condition}`"
    
    # Else statement
    if line == 'else:':
        return "Executes if no previous conditions were true"
    
    # For loop
    if line.startswith('for '):
        match = re.match(r'for\s+(\w+)\s+in\s+(.+?):', line)
        if match:
            var, iterable = match.groups()
            return f"Loops through `{iterable}`, assigning each item to `{var}`"
    
    # While loop
    if line.startswith('while '):
        condition = line[6:].rstrip(':')
        return f"Loops while condition `{condition}` is true"
    
    # Import statement
    if line.startswith('import '):
        module = line[7:].strip()
        return f"Imports the `{module}` module"
    
    if line.startswith('from '):
        match = re.match(r'from\s+(\S+)\s+import\s+(.+)', line)
        if match:
            module, items = match.groups()
            return f"Imports `{items}` from the `{module}` module"
    
    # Assignment
    if '=' in line and not any(op in line for op in ['==', '!=', '<=', '>=']):
        parts = line.split('=', 1)
        if len(parts) == 2:
            var = parts[0].strip()
            val = parts[1].strip()
            # Check for augmented assignment
            if var.endswith(('+', '-', '*', '/', '%', '&', '|', '^')):
                op = var[-1]
                var = var[:-1].strip()
                return f"Updates `{var}` using `{op}=` with `{val}`"
            return f"Assigns `{val}` to variable `{var}`"
    
    # Print statement
    if line.startswith('print('):
        content = line[6:-1] if line.endswith(')') else line[6:]
        return f"Prints: `{content}`"
    
    # Method call
    if '.' in line and '(' in line:
        match = re.match(r'(\w+)\.(\w+)\((.*?)\)', line)
        if match:
            obj, method, args = match.groups()
            return f"Calls method `{method}` on `{obj}`"
    
    # List/dict/set comprehension
    if '[' in line and 'for' in line and 'in' in line:
        return "List comprehension - creates a list in a single line"
    
    if '{' in line and 'for' in line and 'in' in line:
        if ':' in line:
            return "Dictionary comprehension - creates a dict in a single line"
        return "Set comprehension - creates a set in a single line"
    
    return ""


def _detect_code_explanation_request(message: str) -> Optional[str]:
    """
    Detect if user is asking to explain code and extract the code.
    
    Returns:
        The code to explain, or None if not a code explanation request
    """
    msg_lower = message.lower()
    
    # Check for code explanation patterns
    explain_patterns = [
        r'explain\s+(?:this\s+)?code[:\s]*(.+)',
        r'what\s+does\s+this\s+code\s+(?:do|mean)[:\s]*(.+)',
        r'break\s*down\s+(?:this\s+)?code[:\s]*(.+)',
        r'explain\s+line\s*by\s*line[:\s]*(.+)',
        r'how\s+does\s+this\s+(?:code\s+)?work[:\s]*(.+)',
    ]
    
    for pattern in explain_patterns:
        match = re.search(pattern, message, re.IGNORECASE | re.DOTALL)
        if match:
            code = match.group(1).strip()
            # Clean up common prefixes
            code = re.sub(r'^[:\s-]+', '', code)
            if code and ('def ' in code or '=' in code or 'for ' in code or 'if ' in code or 'class ' in code):
                return code
    
    # Check if message starts with code directly after "explain"
    if 'explain' in msg_lower and ('def ' in message or 'class ' in message):
        # Find where code starts
        for marker in ['def ', 'class ', 'import ', 'from ']:
            if marker in message:
                idx = message.find(marker)
                return message[idx:].strip()
    
    return None


def generate_response(
    visitor_id: str,
    user_message: str,
    question: str = "",
    function_name: str = "",
    user_code: str = "",
    interview_mode: bool = False
) -> str:
    """Generate a comprehensive, helpful response based on user input.

    visitor_id scopes the self-learning lookups (learned responses,
    corrections) to this visitor's own history instead of a shared global
    one — see visitor_identity.py for how it's obtained.
    """

    msg_lower = user_message.lower().strip()
    spelling_notice = ""  # Will hold any spelling correction notice

    # ==========================================================================
    # SPELLING CORRECTION: Check and fix typos in the query
    # ==========================================================================
    SmartMatcher = get_smart_matcher(visitor_id)
    if SmartMatcher:
        corrections = SmartMatcher.get_spelling_corrections(user_message)
        if corrections:
            # Build a notice about what was corrected
            correction_pairs = [f"'{wrong}' → '{right}'" for wrong, right in corrections.items()]
            spelling_notice = f"🔤 **Auto-corrected:** {', '.join(correction_pairs)}\n\n"
            
            # Update the message with corrections for processing
            corrected_message = user_message
            for wrong, right in corrections.items():
                # Case-insensitive replacement
                corrected_message = re.sub(
                    re.escape(wrong),
                    right,
                    corrected_message,
                    flags=re.IGNORECASE
                )
            user_message = corrected_message
    msg_lower = user_message.lower().strip()
    
    # Interview mode - act like a technical interviewer
    if interview_mode:
        return generate_interview_response(user_message, question, function_name, user_code)
    
    # ==========================================================================
    # SELF-LEARNING: Check for learned responses (corrections + rated)
    # ==========================================================================
    learned_response = _check_learned_response(visitor_id, user_message)
    if learned_response and learned_response.get("answer"):
        # We have a learned response - format it with confidence indicator
        return spelling_notice + _format_learned_response(learned_response)
    
    # ==========================================================================
    # CODE EXPLANATION REQUEST - Handle "explain this code" requests
    # ==========================================================================
    code_to_explain = _detect_code_explanation_request(user_message)
    if code_to_explain:
        return explain_code(code_to_explain)
    
    # Also check if user is asking to explain their current code
    if user_code and any(phrase in msg_lower for phrase in ["explain my code", "explain this code", "what does my code do", "explain code"]):
        return explain_code(user_code)
    
    # ==========================================================================
    # DIRECT CONCEPT NAME DETECTION - Handle queries like "Robot Framework", "Selenium", etc.
    # ==========================================================================
    direct_concept_names = [
        # Automation concepts
        "robot framework", "selenium", "selenium webdriver", "pytest", "unittest",
        "page object model", "pom", "xpath", "css selector", "webdriver",
        "selenium grid", "selenium waits", "selenium locators", "selenium actions",
        "robot framework keywords", "robot framework variables", "robot framework libraries",
        "seleniumlibrary", "pabot", "allure", "jenkins", "docker",
        # Python concepts
        "python", "list", "dictionary", "tuple", "set", "string", "function", "class",
        "loop", "for loop", "while loop", "if else", "exception", "decorator", "generator",
        "lambda", "comprehension", "list comprehension", "inheritance", "polymorphism",
        "encapsulation", "abstraction", "recursion", "module", "package"
    ]
    
    # Check if the message IS a concept name (with optional punctuation)
    clean_msg = msg_lower.replace("?", "").replace("!", "").replace(".", "").strip()
    
    for concept_name in direct_concept_names:
        if clean_msg == concept_name or clean_msg == f"about {concept_name}":
            # PRIORITY: Check Python concepts FIRST for core Python terms
            # This ensures "class" returns Python class, not Selenium ActionChains
            if concept_name in CONCEPTS:
                return spelling_notice + CONCEPTS[concept_name]
            
            # Then try automation concept match (for selenium, robot, etc.)
            if AUTOMATION_CONCEPTS_AVAILABLE:
                auto_match = _match_automation_concept(concept_name, concept_name.split())
                if auto_match:
                    return spelling_notice + auto_match
            
            # Try partial match in CONCEPTS
            for key in CONCEPTS:
                if concept_name in key or key in concept_name:
                    return spelling_notice + CONCEPTS[key]
    
    # Check for multiple topics first (e.g., "explain loops, classes, functions")
    multi_topic_response = _handle_multiple_topics(user_message)
    if multi_topic_response:
        return multi_topic_response
    
    # Check for concept explanations (expanded to include more question types)
    concept_keywords = ["what is", "what are", "explain", "how does", "how do", "how to",
                       "tell me about", "teach me", "define", "why do we", "why is", "why are", 
                       "why use", "why should", "why need", "what's", "whats", "describe",
                       "show me", "give me example", "example of", "about"]
    is_concept_question = any(keyword in msg_lower for keyword in concept_keywords)
    
    if is_concept_question:
        # Extract the topic from the question
        topic = msg_lower
        # Remove question markers first
        topic = topic.replace("?", "")
        # Remove concept keywords (whole words only)
        # (re already imported at module level)
        removal_keywords = concept_keywords + ["use"]  # Also remove common verbs
        for keyword in removal_keywords:
            topic = re.sub(r'\b' + re.escape(keyword) + r'\b', ' ', topic)
        # Remove articles and prepositions (whole words only)
        for word in ["a", "an", "the", "in", "of", "for"]:
            topic = re.sub(r'\b' + word + r'\b', ' ', topic)
        topic = " ".join(topic.split()).strip()  # Clean up spaces
        topic_words = [w for w in topic.split() if w != "python"]  # Remove "python" for better matching
        
        # CHECK AUTOMATION CONCEPTS FIRST if query contains automation-related words
        automation_priority_words = ['selenium', 'webdriver', 'robot', 'framework', 'pytest', 
                                     'xpath', 'locator', 'locators', 'browser', 'grid', 'headless',
                                     'jenkins', 'docker', 'allure', 'fixture', 'fixtures', 'pabot',
                                     'wait', 'waits', 'element', 'elements', 'css selector',
                                     'page object', 'pom', 'alert', 'frame', 'iframe']
        is_automation_query = any(word in msg_lower for word in automation_priority_words)
        
        if is_automation_query and AUTOMATION_CONCEPTS_AVAILABLE:
            auto_match = _match_automation_concept(topic, topic_words)
            if auto_match:
                return spelling_notice + auto_match
        
        # Helper function to check if words match (including plurals)
        def words_match(word1, word2):
            w1, w2 = word1.lower(), word2.lower()
            if w1 == w2:
                return True
            # Check plurals (simple s, es, ies)
            if w1 + 's' == w2 or w2 + 's' == w1:
                return True
            if w1 + 'es' == w2 or w2 + 'es' == w1:
                return True
            if w1.rstrip('ies') + 'y' == w2 or w2.rstrip('ies') + 'y' == w1:
                return True
            return False
        
        # CHECK SPECIALIZED CONCEPTS FIRST (before general Python concepts)
        # This ensures "dataclass" matches before "class", "asyncio" before generic matches, etc.
        
        # =======================================================================
        # PRIORITY 1: Check if query matches CORE PYTHON CONCEPTS first
        # This ensures "class", "function", "list", etc. return Python content
        # =======================================================================
        core_python_concepts = {
            'class', 'classes', 'function', 'functions', 'method', 'methods',
            'list', 'lists', 'dict', 'dictionary', 'dictionaries', 'tuple', 'tuples',
            'set', 'sets', 'string', 'strings', 'loop', 'loops', 'for', 'while',
            'if', 'else', 'elif', 'exception', 'exceptions', 'decorator', 'decorators',
            'generator', 'generators', 'lambda', 'comprehension', 'inheritance',
            'polymorphism', 'encapsulation', 'abstraction', 'recursion', 'module',
            'package', 'import', 'variable', 'variables', 'object', 'objects',
            'oop', 'iterator', 'iterators'
        }
        
        # Check if query is about core Python (not explicitly automation)
        automation_indicators = {'selenium', 'webdriver', 'robot', 'pytest', 'fixture', 
                                'locator', 'xpath', 'browser', 'actionchains', 'actions',
                                'element', 'click', 'send_keys', 'find_element', 'driver'}
        is_automation_query = any(ind in msg_lower for ind in automation_indicators)
        
        # If it's a core Python concept and NOT explicitly about automation, check Python first
        topic_has_core_concept = any(cc in topic_words or cc in topic for cc in core_python_concepts)
        
        if topic_has_core_concept and not is_automation_query:
            # Check Python CONCEPTS for exact matches first
            for concept_key in CONCEPTS.keys():
                # Exact word match
                if concept_key in topic_words:
                    return spelling_notice + CONCEPTS[concept_key]
                # Handle plurals: "classes" -> "class"
                singular = concept_key.rstrip('s') if concept_key.endswith('s') else concept_key
                for tw in topic_words:
                    tw_singular = tw.rstrip('s') if tw.endswith('s') else tw
                    if concept_key == tw_singular or singular == tw or singular == tw_singular:
                        return spelling_notice + CONCEPTS[concept_key]
        
        # =======================================================================
        # PRIORITY 2: Advanced Python concepts (async, dataclass, pathlib)
        # =======================================================================
        if ADVANCED_CONCEPTS_AVAILABLE:
            for concept_key in ADVANCED_CONCEPTS.keys():
                if concept_key in topic or any(concept_key == tw or concept_key in tw for tw in topic_words):
                    return spelling_notice + ADVANCED_CONCEPTS[concept_key]
        
        # =======================================================================
        # PRIORITY 3: Automation concepts ONLY if query has automation indicators
        # =======================================================================
        if AUTOMATION_CONCEPTS_AVAILABLE and is_automation_query:
            auto_match = _match_automation_concept(topic, topic_words)
            if auto_match:
                return spelling_notice + auto_match
        
        # =======================================================================
        # PRIORITY 4: Infrastructure concepts (networking, servers, storage)
        # =======================================================================
        if INFRASTRUCTURE_CONCEPTS_AVAILABLE:
            for concept_key in INFRASTRUCTURE_CONCEPTS.keys():
                if concept_key in topic or any(concept_key == tw or concept_key in tw for tw in topic_words):
                    return spelling_notice + INFRASTRUCTURE_CONCEPTS[concept_key]
        
        # =======================================================================
        # PRIORITY 5: Linux concepts (systemd, bash, etc.)
        # =======================================================================
        if LINUX_CONCEPTS_AVAILABLE:
            # Concept aliases: map specific terms to their parent concepts
            linux_concept_aliases = {
                'chmod': 'linux_permissions', 'chown': 'linux_permissions', 'chgrp': 'linux_permissions',
                'permissions': 'linux_permissions', 'umask': 'linux_permissions',
                'boot': 'linux_boot', 'grub2': 'grub', 'bootloader': 'grub',
                'kernel': 'linux_kernel', 'distro': 'linux_distro', 'distribution': 'linux_distro',
                'packages': 'linux_packages', 'apt': 'linux_packages', 'yum': 'linux_packages', 'dnf': 'linux_packages',
                'process': 'linux_processes', 'ps': 'linux_processes', 'top': 'linux_processes',
                'firewall': 'linux_firewall', 'iptables': 'linux_firewall', 'ufw': 'linux_firewall',
                'logs': 'linux_logs', 'journalctl': 'linux_logs', 'syslog': 'linux_logs',
                'users': 'linux_users', 'groups': 'linux_users', 'useradd': 'linux_users',
                'filesystem': 'linux_filesystem', 'fhs': 'linux_filesystem',
                'network': 'linux_networking', 'networking': 'linux_networking',
                'hardening': 'linux_hardening', 'security': 'linux_hardening',
            }
            
            # Check for aliased terms first
            for tw in topic_words:
                if tw in linux_concept_aliases:
                    alias_target = linux_concept_aliases[tw]
                    if alias_target in LINUX_CONCEPTS:
                        return spelling_notice + LINUX_CONCEPTS[alias_target]
            
            for concept_key in LINUX_CONCEPTS.keys():
                if concept_key in topic or any(concept_key == tw or concept_key in tw for tw in topic_words):
                    return spelling_notice + LINUX_CONCEPTS[concept_key]
        
        # =======================================================================
        # PRIORITY 6: Automation concepts (fallback for non-explicit queries)
        # =======================================================================
        if AUTOMATION_CONCEPTS_AVAILABLE and not topic_has_core_concept:
            auto_match = _match_automation_concept(topic, topic_words)
            if auto_match:
                return spelling_notice + auto_match
        
        # Find the best matching concept from general Python CONCEPTS
        best_match = None
        best_score = 0
        
        for concept_key in CONCEPTS.keys():
            score = 0
            concept_words = concept_key.split()
            
            # Exact match in topic words (highest priority)
            if concept_key in topic_words:
                score = 100
            # Multi-word concept - check if all words are present
            elif len(concept_words) > 1:
                if concept_key in topic:
                    score = 95
                elif all(any(words_match(cw, tw) for tw in topic_words) for cw in concept_words):
                    score = 90
            # Single word - check with plural matching
            elif any(words_match(concept_key, tw) for tw in topic_words):
                score = 85
            # Check if concept is substring of any topic word
            elif any(concept_key in tw or tw in concept_key for tw in topic_words):
                score = 70 + len(concept_key)
            # Substring match in full topic
            elif concept_key in topic:
                score = 50 + len(concept_key)
            
            if score > best_score:
                best_score = score
                best_match = concept_key
        
        if best_match and best_score > 0:
            return spelling_notice + CONCEPTS[best_match]
        
        # If no manual match, try PDF knowledge base
        if PDF_KB_AVAILABLE:
            pdf_answer = query_pdf_knowledge(user_message)
            if pdf_answer:
                return spelling_notice + pdf_answer
    
    # General Python questions - try PDF knowledge base
    python_question_keywords = ["how to", "can you", "why does", "when should", "what's the difference"]
    if any(kw in msg_lower for kw in python_question_keywords):
        # Check manual concepts - sort by length for more specific matches
        sorted_concepts = sorted(CONCEPTS.keys(), key=len, reverse=True)
        for concept_key in sorted_concepts:
            if concept_key in msg_lower.split() or concept_key in msg_lower:
                return spelling_notice + CONCEPTS[concept_key]
        
        # Then try PDF
        if PDF_KB_AVAILABLE:
            pdf_answer = query_pdf_knowledge(user_message)
            if pdf_answer:
                return spelling_notice + pdf_answer
    
    # Check for "where" questions about Python usage
    if "where" in msg_lower and "python" in msg_lower:
        if "python use" in CONCEPTS:
            return CONCEPTS["python use"]
    
    # Check for "why" questions about Python
    if "why" in msg_lower and "python" in msg_lower:
        # "why python", "why use python", "why do we need python", etc.
        if "python" in CONCEPTS:
            return CONCEPTS["python"]
    
    # Any remaining question with "python" - try the python concept
    if "python" in msg_lower and "?" in user_message:
        # First try PDF for specific Python questions
        if PDF_KB_AVAILABLE:
            pdf_answer = query_pdf_knowledge(user_message)
            if pdf_answer:
                return pdf_answer
        # Fallback to python concept
        if "python" in CONCEPTS:
            return CONCEPTS["python"]
    
    # Hint request
    if any(word in msg_lower for word in ["hint", "help", "stuck", "clue", "tip", "guide"]):
        return generate_hint_response(question, function_name, user_code)
    
    # Explain problem request
    if any(word in msg_lower for word in ["explain problem", "understand", "what does", "what should", "problem mean"]):
        return generate_problem_explanation(question, function_name)
    
    # Error/debugging help
    if any(word in msg_lower for word in ["error", "wrong", "not working", "failed", "bug", "debug", "fix"]):
        return generate_debug_response(user_code, question, function_name)
    
    # Complexity question
    if any(word in msg_lower for word in ["complexity", "big o", "time", "space", "efficient", "optimize"]):
        return generate_complexity_response(question, function_name)
    
    # Solution request
    if any(word in msg_lower for word in ["solution", "answer", "show me", "give me code"]):
        return generate_solution_guidance(question, function_name)
    
    # Approach/strategy question
    if any(word in msg_lower for word in ["approach", "strategy", "how to start", "where to begin"]):
        return generate_approach_response(question, function_name)
    
    # Compare/difference question
    if any(word in msg_lower for word in ["difference", "compare", "vs", "versus", "better"]):
        return generate_comparison_response(msg_lower)
    
    # Greeting (check for whole words only, not substrings like "mac-hi-ne")
    msg_words = msg_lower.split()
    if any(word in msg_words for word in ["hi", "hello", "hey", "hii", "heyy"]) or msg_lower.strip() in ["hi", "hello", "hey"]:
        problem_context = f"I'm here to help you solve **`{function_name}`**!\n\n" if function_name else ""
        return f"""👋 Hello! I'm your Python tutor.

{problem_context}**I can help you with:**
• 💡 "Give me a hint" - progressive hints
• 📖 "Explain the problem" - understand requirements
• 🐛 "Help with error" - debug your code
• 📚 "What is [concept]" - learn Python concepts
• 🎯 "How to approach this" - strategy guidance
• 📕 Ask any Python question - powered by Python Crash Course!

What would you like to know?"""

    # Thanks
    if any(word in msg_lower for word in ["thank", "thanks", "helpful"]):
        return random.choice([
            "You're welcome! Keep coding! 💪",
            "Happy to help! You've got this! 🚀",
            "Anytime! Keep practicing! ⭐",
            "Glad I could help! Good luck! 🎯"
        ])
    
    # ==========================================================================
    # CATCH-ALL: Try to answer ANY question using available knowledge sources
    # ==========================================================================
    
    # If it looks like a question, try to answer it
    is_question = "?" in user_message or any(w in msg_lower for w in 
        ["what", "why", "how", "when", "where", "which", "can", "could", "would", "should", "is", "are", "do", "does"])
    
    if is_question:
        # Try PDF knowledge base first (no API needed)
        if PDF_KB_AVAILABLE:
            _ensure_pdf_kb_initialized()
            pdf_answer = query_pdf_knowledge(user_message)
            if pdf_answer:
                return spelling_notice + pdf_answer
        
        # Try Groq AI for complex/unmatched questions (if available)
        groq_response = _try_groq_for_complex_query(user_message, question, function_name, user_code)
        if groq_response:
            return spelling_notice + groq_response
        
        # Try to match any concept as a last resort
        for concept_key in CONCEPTS.keys():
            if concept_key in msg_lower:
                return spelling_notice + CONCEPTS[concept_key]
        
        # Try advanced concepts (async, dataclass, pathlib, etc.)
        if ADVANCED_CONCEPTS_AVAILABLE:
            for concept_key in ADVANCED_CONCEPTS.keys():
                if concept_key in msg_lower:
                    return spelling_notice + ADVANCED_CONCEPTS[concept_key]
        
        # Try infrastructure concepts (networking, servers, storage)
        if INFRASTRUCTURE_CONCEPTS_AVAILABLE:
            for concept_key in INFRASTRUCTURE_CONCEPTS.keys():
                if concept_key in msg_lower:
                    return spelling_notice + INFRASTRUCTURE_CONCEPTS[concept_key]
        
        # Try Linux concepts
        if LINUX_CONCEPTS_AVAILABLE:
            for concept_key in LINUX_CONCEPTS.keys():
                if concept_key in msg_lower:
                    return spelling_notice + LINUX_CONCEPTS[concept_key]
    
    # Direct concept lookup for single-word queries
    msg_single = msg_lower.strip()
    if ' ' not in msg_single:
        if ADVANCED_CONCEPTS_AVAILABLE and msg_single in ADVANCED_CONCEPTS:
            return spelling_notice + ADVANCED_CONCEPTS[msg_single]
        if LINUX_CONCEPTS_AVAILABLE:
            # Check direct match first
            if msg_single in LINUX_CONCEPTS:
                return spelling_notice + LINUX_CONCEPTS[msg_single]
            # Check Linux aliases for single-word queries
            linux_single_aliases = {
                'chmod': 'linux_permissions', 'chown': 'linux_permissions', 'chgrp': 'linux_permissions',
                'permissions': 'linux_permissions', 'umask': 'linux_permissions',
                'boot': 'linux_boot', 'grub': 'grub', 'bootloader': 'grub',
                'kernel': 'linux_kernel', 'distro': 'linux_distro',
                'packages': 'linux_packages', 'apt': 'linux_packages', 'yum': 'linux_packages',
                'process': 'linux_processes', 'processes': 'linux_processes',
                'firewall': 'linux_firewall', 'iptables': 'linux_firewall',
                'logs': 'linux_logs', 'journalctl': 'linux_logs',
                'users': 'linux_users', 'groups': 'linux_users',
                'filesystem': 'linux_filesystem', 'network': 'linux_networking',
            }
            if msg_single in linux_single_aliases:
                alias_target = linux_single_aliases[msg_single]
                if alias_target in LINUX_CONCEPTS:
                    return spelling_notice + LINUX_CONCEPTS[alias_target]
        if INFRASTRUCTURE_CONCEPTS_AVAILABLE and msg_single in INFRASTRUCTURE_CONCEPTS:
            return spelling_notice + INFRASTRUCTURE_CONCEPTS[msg_single]
    
    # Final fallback: Direct concept lookup for multi-word queries
    msg_clean = msg_lower.strip()
    if msg_clean in CONCEPTS:
        return spelling_notice + CONCEPTS[msg_clean]
    if ADVANCED_CONCEPTS_AVAILABLE and msg_clean in ADVANCED_CONCEPTS:
        return spelling_notice + ADVANCED_CONCEPTS[msg_clean]
    if LINUX_CONCEPTS_AVAILABLE and msg_clean in LINUX_CONCEPTS:
        return spelling_notice + LINUX_CONCEPTS[msg_clean]
    if INFRASTRUCTURE_CONCEPTS_AVAILABLE and msg_clean in INFRASTRUCTURE_CONCEPTS:
        return spelling_notice + INFRASTRUCTURE_CONCEPTS[msg_clean]
    
    # Final fallback: Check for meaningful matches in all concept keys
    # Filter out common/stop words that cause false matches (e.g., 'is' in 'list')
    stop_words = {'what', 'is', 'are', 'a', 'an', 'the', 'how', 'do', 'does', 'can', 'i', 
                  'to', 'in', 'on', 'of', 'for', 'me', 'my', 'about', 'tell', 'explain', 
                  'show', 'give', 'please', 'help', 'with', 'this', 'that', 'it', 'be'}
    meaningful_words = [w for w in msg_clean.split() if w not in stop_words and len(w) > 2]
    
    # Helper function for safe concept matching
    def matches_concept(concept_key, words, message):
        # Exact key match in message
        if concept_key in message.split():
            return True
        # Word matches concept key exactly or is significant substring
        for w in words:
            if w == concept_key:  # Exact word match
                return True
            # Only allow substring matches for words >= 4 chars to avoid 'is' in 'list'
            if len(w) >= 4 and (w in concept_key or concept_key in w):
                return True
        return False
    
    # Check if query has automation indicators - if so, check automation FIRST
    final_automation_indicators = {'selenium', 'webdriver', 'robot', 'pytest', 'fixture', 
                                   'locator', 'xpath', 'browser', 'actionchains', 'actions',
                                   'element', 'click', 'driver', 'page', 'pom'}
    has_automation_indicator = any(ind in meaningful_words for ind in final_automation_indicators)
    
    if has_automation_indicator and AUTOMATION_CONCEPTS_AVAILABLE:
        # Check Automation FIRST for automation-related queries
        auto_match = _match_automation_concept(msg_clean, meaningful_words)
        if auto_match:
            return spelling_notice + auto_match
    
    # Check Python CONCEPTS (only if not an automation query)
    if not has_automation_indicator:
        for concept_key in CONCEPTS.keys():
            if matches_concept(concept_key, meaningful_words, msg_clean):
                return spelling_notice + CONCEPTS[concept_key]
    
    # Check Advanced
    if ADVANCED_CONCEPTS_AVAILABLE:
        for concept_key in ADVANCED_CONCEPTS.keys():
            if matches_concept(concept_key, meaningful_words, msg_clean):
                return spelling_notice + ADVANCED_CONCEPTS[concept_key]
    
    # Check Automation (fallback for non-indicator queries)
    if not has_automation_indicator and AUTOMATION_CONCEPTS_AVAILABLE:
        auto_match = _match_automation_concept(msg_clean, meaningful_words)
        if auto_match:
            return spelling_notice + auto_match
    
    # If automation query didn't match, try Python CONCEPTS as fallback
    if has_automation_indicator:
        for concept_key in CONCEPTS.keys():
            if matches_concept(concept_key, meaningful_words, msg_clean):
                return spelling_notice + CONCEPTS[concept_key]
    # Check Infrastructure
    if INFRASTRUCTURE_CONCEPTS_AVAILABLE:
        for concept_key in INFRASTRUCTURE_CONCEPTS.keys():
            if matches_concept(concept_key, meaningful_words, msg_clean):
                return spelling_notice + INFRASTRUCTURE_CONCEPTS[concept_key]
    # Check Linux
    if LINUX_CONCEPTS_AVAILABLE:
        for concept_key in LINUX_CONCEPTS.keys():
            if matches_concept(concept_key, meaningful_words, msg_clean):
                return spelling_notice + LINUX_CONCEPTS[concept_key]
    
    # Default helpful response (only if nothing else worked)
    return spelling_notice + generate_default_response(question, function_name, user_code, user_message)


def generate_interview_response(
    user_message: str, 
    question: str, 
    function_name: str, 
    user_code: str,
    interview_state: dict = None
) -> str:
    """
    Generate context-aware interviewer-style responses.
    
    Uses the interview engine for stateful, stage-aware responses when available,
    falls back to basic responses otherwise.
    """
    
    # Try to use the interview engine for advanced responses
    try:
        from interview_engine import InterviewEngine, InterviewState, InterviewStage
        
        # If we have an interview state dict, reconstruct the engine
        if interview_state and isinstance(interview_state, dict):
            engine = _get_interview_engine_from_state(interview_state, question, function_name)
            if engine:
                return engine.process_response(user_message, user_code)
    except ImportError:
        pass
    
    # Fallback to enhanced basic interview responses
    return _generate_basic_interview_response(user_message, question, function_name, user_code)


def _get_interview_engine_from_state(state_dict: dict, question: str, function_name: str):
    """Reconstruct interview engine from session state dict."""
    try:
        from interview_engine import (
            InterviewEngine, InterviewState, InterviewConfig,
            InterviewStage, InterviewDifficulty, InterviewType, InterviewScores
        )
        
        # Create config from state
        config = InterviewConfig(
            difficulty=InterviewDifficulty(state_dict.get('difficulty', 'mid')),
            interview_type=InterviewType(state_dict.get('interview_type', 'technical')),
            time_limit_minutes=state_dict.get('time_limit', 30),
            show_live_score=state_dict.get('show_live_score', False),
        )
        
        # Create state
        state = InterviewState(config=config)
        state.problem_name = question
        state.function_name = function_name
        
        # Restore stage
        stage_value = state_dict.get('current_stage', 'intro')
        state.current_stage = InterviewStage(stage_value)
        
        # Restore conversation history
        state.conversation_history = state_dict.get('conversation_history', [])
        
        # Restore tracking flags
        state.user_mentioned_complexity = state_dict.get('user_mentioned_complexity', False)
        state.user_mentioned_edge_cases = state_dict.get('user_mentioned_edge_cases', False)
        state.user_asked_clarifying = state_dict.get('user_asked_clarifying', False)
        state.user_explained_approach = state_dict.get('user_explained_approach', False)
        state.code_attempts = state_dict.get('code_attempts', 0)
        state.asked_questions = state_dict.get('asked_questions', [])
        
        # Restore scores
        scores_dict = state_dict.get('scores', {})
        state.scores = InterviewScores(
            problem_solving=scores_dict.get('problem_solving', 0),
            communication=scores_dict.get('communication', 0),
            code_quality=scores_dict.get('code_quality', 0),
            complexity_analysis=scores_dict.get('complexity_analysis', 0),
        )
        
        return InterviewEngine(state)
    except Exception:
        return None


def _generate_basic_interview_response(
    user_message: str, 
    question: str, 
    function_name: str, 
    user_code: str
) -> str:
    """Generate basic interview responses without the full engine."""
    
    msg_lower = user_message.lower()
    
    # Analyze what the user has mentioned
    mentioned_complexity = any(p in msg_lower for p in [
        'o(', 'time complexity', 'space complexity', 'linear', 'quadratic', 'big o'
    ])
    mentioned_edge_cases = any(p in msg_lower for p in [
        'edge case', 'empty', 'null', 'none', 'negative', 'zero', 'boundary'
    ])
    has_substantial_code = user_code and len(user_code.strip()) > 100 and 'def ' in user_code
    asking_question = '?' in user_message
    
    # If they're asking a question, redirect appropriately
    if asking_question:
        redirect_responses = [
            "Good question! But let me hear your thoughts first - what's your initial approach to this problem?",
            "I'd like you to think through that. What have you considered so far?",
            "Let's explore that together. Walk me through your thinking.",
            "That's something worth discussing. But first, how would you break down this problem?",
        ]
        return random.choice(redirect_responses)
    
    # Context-aware follow-ups based on what they've mentioned
    followups = []
    
    if has_substantial_code:
        if not mentioned_complexity:
            followups.extend([
                f"I see you've written some code. What's the time complexity of your `{function_name}` solution?",
                "Good progress on the code. Can you analyze the space complexity?",
                f"Walk me through your `{function_name}` implementation. What's the Big O?",
            ])
        elif not mentioned_edge_cases:
            followups.extend([
                "Your complexity analysis is good. Now, what edge cases should we consider?",
                "How would your solution handle an empty input?",
                "What happens if the input contains duplicates?",
            ])
        else:
            followups.extend([
                "Excellent analysis! Is there a way to optimize this further?",
                "Can you think of an alternative approach that might be more efficient?",
                "What trade-offs did you consider in your implementation?",
            ])
    else:
        # They haven't written much code yet
        if not any(p in msg_lower for p in ['approach', 'plan', 'strategy', 'first', 'step']):
            followups.extend([
                "Before we dive into code, walk me through your approach.",
                "How would you break down this problem? What's the first step?",
                f"What algorithm or technique do you think would work well for `{function_name}`?",
            ])
        else:
            followups.extend([
                "Good approach! Go ahead and start implementing. Talk me through your code as you write it.",
                "That sounds reasonable. Let's see how you'd translate that into code.",
                "I like your thinking. What data structure would you use?",
            ])
    
    # Add some variety with general probing questions
    general_followups = [
        f"What's the expected behavior of `{function_name}` for edge cases?",
        "How would you test this to make sure it works correctly?",
        "What would you do differently if performance was critical?",
        "Can you identify any potential bugs in your current approach?",
    ]
    
    # Select from appropriate pool
    if followups:
        return random.choice(followups)
    return random.choice(general_followups)


def get_interview_state_dict(engine) -> dict:
    """Convert interview engine state to a serializable dict for session storage."""
    try:
        state = engine.state
        return {
            'difficulty': state.config.difficulty.value,
            'interview_type': state.config.interview_type.value,
            'time_limit': state.config.time_limit_minutes,
            'show_live_score': state.config.show_live_score,
            'current_stage': state.current_stage.value,
            'conversation_history': state.conversation_history,
            'user_mentioned_complexity': state.user_mentioned_complexity,
            'user_mentioned_edge_cases': state.user_mentioned_edge_cases,
            'user_asked_clarifying': state.user_asked_clarifying,
            'user_explained_approach': state.user_explained_approach,
            'code_attempts': state.code_attempts,
            'asked_questions': state.asked_questions,
            'scores': {
                'problem_solving': state.scores.problem_solving,
                'communication': state.scores.communication,
                'code_quality': state.scores.code_quality,
                'complexity_analysis': state.scores.complexity_analysis,
            },
            'start_time': state.start_time.isoformat() if state.start_time else None,
        }
    except Exception:
        return {}


def generate_interview_feedback_summary(interview_state: dict) -> str:
    """Generate a comprehensive feedback summary for a completed interview."""
    try:
        from interview_engine import InterviewEngine
        
        engine = _get_interview_engine_from_state(interview_state, "", "")
        if engine:
            return engine.force_end_interview()
    except ImportError:
        pass
    
    # Fallback basic feedback
    scores = interview_state.get('scores', {})
    total = sum(scores.values()) / 4 if scores else 0
    
    return f"""## 📊 Interview Summary

**Estimated Score:** {total:.0f}/100

### Areas Covered:
- Complexity Analysis: {'✓' if interview_state.get('user_mentioned_complexity') else '✗'}
- Edge Cases: {'✓' if interview_state.get('user_mentioned_edge_cases') else '✗'}
- Clear Approach: {'✓' if interview_state.get('user_explained_approach') else '✗'}

### Tips for Improvement:
1. Always discuss time and space complexity
2. Consider edge cases before coding
3. Think out loud - communication matters!

Keep practicing! 🚀"""


def generate_hint_response(question: str, function_name: str, user_code: str) -> str:
    """Generate progressive, helpful hints."""
    
    hints_data = get_problem_hints(question, function_name)
    code_issues = analyze_code(user_code)
    
    response = f"""## 💡 Hints for `{function_name}`

**Concept:** {hints_data['concept']}

### Progressive Hints:
"""
    
    for i, hint in enumerate(hints_data['hints'], 1):
        response += f"\n**{i}.** {hint}"
    
    if 'template' in hints_data:
        response += f"""

### 📝 Code Template:
```python
{hints_data['template']}
```
"""
    
    if code_issues:
        response += "\n\n### ⚠️ Issues in Your Code:\n"
        for issue in code_issues:
            response += f"\n**Issue:** {issue['issue']}\n"
            response += f"**Fix:** {issue['fix']}\n"
    
    return response


def generate_problem_explanation(question: str, function_name: str) -> str:
    """Generate a detailed problem explanation."""
    
    hints_data = get_problem_hints(question, function_name)
    
    return f"""## 📖 Problem Explanation

**Function:** `{function_name}`

**Task:** {question}

### Understanding the Problem:
1. **Input:** What data does your function receive?
2. **Output:** What should your function return?
3. **Constraints:** Any limits on input size or values?

### Key Concept: {hints_data['concept']}

### Approach:
{hints_data['hints'][0]}

### Steps to Solve:
1. Read the problem carefully - what's being asked?
2. Think of simple examples and trace through them
3. Identify the pattern or algorithm needed
4. Consider edge cases (empty input, single element, etc.)
5. Write your solution and test with examples

### Related Concepts:
You might want to review these topics: **{hints_data['concept']}**

Would you like a hint on how to start coding?"""


def generate_debug_response(user_code: str, question: str, function_name: str) -> str:
    """Generate debugging assistance."""
    
    issues = analyze_code(user_code)
    
    response = f"""## 🔍 Debug Assistant for `{function_name}`

"""
    
    if issues:
        response += "### Issues Found:\n"
        for i, issue in enumerate(issues, 1):
            response += f"""
**{i}. {issue['issue']}**
- **Fix:** {issue['fix']}
- **Example:**
{issue['example']}
"""
    else:
        response += """### No obvious issues detected.

**General Debugging Checklist:**
"""
    
    response += """
### 🔧 Common Problems to Check:

1. **Return vs Print**
   - Using `return` (not `print`) to give output?

2. **Function Signature**
   - Parameters match what tests expect?

3. **Edge Cases**
   - Empty input handled?
   - Single element handled?
   - Negative numbers (if applicable)?

4. **Off-by-One Errors**
   - Loop bounds correct?
   - Index access within range?

5. **Type Issues**
   - Returning correct type (list vs int vs string)?
   - Comparing compatible types?

### 🐛 Quick Debug Tip:
Add print statements to trace your code:
```python
def """ + function_name + """(...):
    print(f"Input: {...}")  # See what you receive
    # your code
    print(f"Result: {result}")  # See what you return
    return result
```
"""
    
    return response


def generate_complexity_response(question: str, function_name: str) -> str:
    """Generate complexity analysis guidance."""
    
    return f"""## ⏱️ Complexity Analysis for `{function_name}`

### Time Complexity Quick Reference:

| Complexity | Name | Example Operations |
|------------|------|-------------------|
| **O(1)** | Constant | Array access, hash lookup |
| **O(log n)** | Logarithmic | Binary search |
| **O(n)** | Linear | Single loop, linear search |
| **O(n log n)** | Linearithmic | Efficient sorting |
| **O(n²)** | Quadratic | Nested loops |
| **O(2ⁿ)** | Exponential | Naive recursion |

### Analyzing Your Solution:

**Count your loops:**
- 1 loop over n elements = O(n)
- Nested loops = O(n × m) or O(n²)
- Loop with halving = O(log n)

**Check operations inside loops:**
- Each operation's complexity multiplies

**Common patterns:**
```python
# O(n) - Single pass
for item in items:
    # O(1) work

# O(n²) - Nested loops
for i in items:
    for j in items:
        # O(1) work

# O(n log n) - Sorting
sorted(items)

# O(1) - Dictionary lookup
if key in my_dict:
```

### Space Complexity:
- Extra array of size n = O(n)
- Fixed variables = O(1)
- Recursion depth d = O(d) stack space

What approach are you considering?"""


def generate_solution_guidance(question: str, function_name: str) -> str:
    """Guide toward solution without giving it away."""
    
    hints_data = get_problem_hints(question, function_name)
    
    return f"""## 🎯 Solution Guidance for `{function_name}`

I won't give you the direct answer, but I'll guide you there!

### Key Insight:
{hints_data['hints'][0]}

### Problem Breakdown:
1. **Input Processing:** What form is your input in?
2. **Core Logic:** {hints_data['hints'][1] if len(hints_data['hints']) > 1 else 'Think about the main operation needed'}
3. **Output Formation:** What should you return?

### Building Blocks:
```python
def {function_name}(...):
    # Step 1: Handle edge cases
    if not input_data:
        return ...
    
    # Step 2: Initialize variables
    result = ...
    
    # Step 3: Main logic
    for item in input_data:
        # process item
        pass
    
    # Step 4: Return result
    return result
```

### Questions to Ask Yourself:
- What's the simplest case?
- What changes from step to step?
- What do I need to track?

Want a more specific hint?"""


def generate_approach_response(question: str, function_name: str) -> str:
    """Generate strategic approach guidance."""
    
    hints_data = get_problem_hints(question, function_name)
    
    return f"""## 🗺️ Strategy for `{function_name}`

### Step-by-Step Approach:

**1. Understand (2 min)**
- Read the problem twice
- Identify input/output format
- Note any constraints

**2. Examples (2 min)**
- Work through provided examples by hand
- Create your own simple example
- Identify the pattern

**3. Approach (3 min)**
- What data structure fits? (list, dict, set?)
- What algorithm pattern? (loop, recursion, two pointers?)
- What's the core operation?

**4. Pseudocode (2 min)**
```
function {function_name}:
    handle edge cases
    initialize tracking variables
    process input
    return result
```

**5. Code (5 min)**
- Translate pseudocode to Python
- Start simple, add complexity

**6. Test (2 min)**
- Run with examples
- Try edge cases

### For This Problem:
- **Concept:** {hints_data['concept']}
- **First thought:** {hints_data['hints'][0]}

Ready to start coding?"""


def generate_comparison_response(query: str) -> str:
    """Generate comparison explanations."""
    
    comparisons = {
        "list tuple": """## List vs Tuple

| Aspect | List | Tuple |
|--------|------|-------|
| **Mutability** | Mutable ✓ | Immutable ✗ |
| **Syntax** | `[1, 2, 3]` | `(1, 2, 3)` |
| **Use case** | Dynamic data | Fixed data |
| **Dict key** | No | Yes |
| **Memory** | More | Less |
| **Speed** | Slower | Faster |

**Use List when:** Data changes, need append/remove
**Use Tuple when:** Data fixed, dict keys, function returns""",
        
        "set list": """## Set vs List

| Aspect | Set | List |
|--------|-----|------|
| **Order** | Unordered | Ordered |
| **Duplicates** | No | Yes |
| **Lookup** | O(1) | O(n) |
| **Syntax** | `{1, 2, 3}` | `[1, 2, 3]` |

**Use Set when:** Need unique items, fast membership test
**Use List when:** Order matters, duplicates allowed""",

        "sort sorted": """## sort() vs sorted()

| Aspect | `.sort()` | `sorted()` |
|--------|-----------|------------|
| **Returns** | None | New list |
| **Original** | Modified | Unchanged |
| **Works on** | Lists only | Any iterable |

```python
nums = [3, 1, 2]

# .sort() - in-place
nums.sort()
# nums is now [1, 2, 3]

# sorted() - new list
nums = [3, 1, 2]
new_nums = sorted(nums)
# nums still [3, 1, 2], new_nums is [1, 2, 3]
```"""
    }
    
    for key, explanation in comparisons.items():
        if all(word in query for word in key.split()):
            return explanation
    
    return "I can compare Python concepts! Try asking about 'list vs tuple', 'set vs list', or 'sort vs sorted'."


def generate_default_response(question: str, function_name: str, user_code: str, original_question: str = "") -> str:
    """
    Generate a response by trying all available knowledge sources.
    This is the fallback when no specific pattern matches.
    """
    # If there's no context at all, show help menu with original question
    if not function_name and not question:
        return _show_help_menu(original_question)
    
    # If we have a problem context, give problem-specific help
    if function_name:
        keywords = extract_keywords(question + " " + function_name)
        
        response = f"""## 💡 Help with `{function_name}`

I can help you solve this problem! Here's what you can ask:

**Getting Started:**
- "Give me a hint" - I'll guide you step by step
- "Explain the problem" - I'll break down what's needed
- "How to approach this" - Strategy and algorithm suggestions

**If You're Stuck:**
- "What's wrong with my code" - I'll analyze your code
- "Help with error" - Debugging assistance

**Learning:**
- "What is [concept]" - Ask about any Python concept
- "Time complexity" - Efficiency analysis
"""
        
        if keywords:
            response += f"""
**Related Concepts:** {', '.join(keywords)}
Try asking: "What is {keywords[0]}?" for a detailed explanation!
"""
        return response
    
    # Generic question - try to be helpful
    return _show_help_menu()


def _show_help_menu(original_question: str = "") -> str:
    """Show help or acknowledge when we don't have a specific answer."""
    kb_status = ""
    if PDF_KB_AVAILABLE:
        _ensure_pdf_kb_initialized()
        if is_knowledge_base_ready():
            kb_status = "📚 **Python Crash Course loaded** - Ask me anything about Python!\n\n"
    
    # If there was an original question, acknowledge it
    if original_question:
        return f"""## 🤔 I don't have specific information about that topic

I searched my knowledge base but couldn't find a detailed answer for your question.

**What I can help with:**
- Core Python concepts (lists, dicts, loops, functions, classes)
- Object-oriented programming (OOP, inheritance, polymorphism)
- Data structures and algorithms
- Python syntax and best practices
- Debugging and error handling

**Try rephrasing or ask about:**
- "What is [Python concept]?"
- "How do I [do something in Python]?"
- "Explain [programming concept]"

{kb_status}"""
    
    return f"""## 🤖 Python AI Tutor

{kb_status}I'm here to help you learn Python! Here's what I can do:

### 📖 Ask Me About Python:
- "What is a list?" - Data structures
- "Explain OOP" - Object-oriented programming  
- "What is recursion?" - Algorithms
- "How do loops work?" - Control flow
- "What is Python?" - Language overview

### 💡 Problem Solving:
- "Give me a hint" - Step-by-step guidance
- "Explain the problem" - Understand requirements
- "How to approach this" - Strategy help

### 🐛 Debugging:
- "Help with error" - Fix your code
- "What's wrong" - Bug analysis

**Try asking a question!** For example:
- "What is a dictionary in Python?"
- "How do I use list comprehension?"
- "Why do we use functions?"
"""


# =============================================================================
# CODE REVIEW AND BUG DETECTION
# =============================================================================

def get_code_review(code: str, question: str, function_name: str, time_taken: float) -> str:
    """Provide comprehensive code review."""
    
    issues = analyze_code(code)
    
    # Analyze code characteristics
    lines = [l for l in code.split('\n') if l.strip() and not l.strip().startswith('#')]
    num_lines = len(lines)
    has_loop = bool(re.search(r'\b(for|while)\b', code))
    has_nested = bool(re.search(r'(for|while).*\n.*\s+(for|while)', code, re.DOTALL))
    uses_comprehension = bool(re.search(r'\[.*for.*in.*\]', code))
    uses_builtin = bool(re.search(r'\b(sum|max|min|sorted|reversed|zip|map|filter|any|all)\b', code))
    has_recursion = bool(re.search(rf'\b{function_name}\s*\(', code[code.find('def '):]))
    
    review = f"""## ✨ Code Review for `{function_name}`

"""
    
    # Time feedback
    if time_taken < 60:
        review += "⚡ **Speed:** Excellent! Solved in under a minute.\n\n"
    elif time_taken < 180:
        review += "👍 **Speed:** Good pace. Thoughtful approach.\n\n"
    elif time_taken < 300:
        review += "💪 **Speed:** Took your time - that's okay for complex problems.\n\n"
    else:
        review += "🎯 **Speed:** Persistence paid off! Sometimes problems need more thought.\n\n"
    
    # Code characteristics
    review += "### Code Analysis:\n\n"
    
    # Length
    if num_lines <= 3:
        review += "✓ **Conciseness:** Very clean and minimal - excellent!\n"
    elif num_lines <= 8:
        review += "✓ **Length:** Well-structured, readable code.\n"
    elif num_lines <= 15:
        review += "○ **Length:** Consider if any parts can be simplified.\n"
    else:
        review += "△ **Length:** Might benefit from refactoring into smaller functions.\n"
    
    # Patterns
    if uses_comprehension:
        review += "✓ **Style:** Nice use of list comprehension - Pythonic!\n"
    
    if uses_builtin:
        review += "✓ **Built-ins:** Good use of Python's optimized functions.\n"
    
    if has_recursion:
        review += "○ **Recursion:** Recursive solution - check for stack limits.\n"
    
    # Complexity estimate
    review += "\n### Complexity Estimate:\n\n"
    if has_nested:
        review += "- **Time:** Likely O(n²) due to nested loops\n"
        review += "- Consider: Can you reduce to O(n) with a hash table?\n"
    elif has_loop or uses_comprehension:
        review += "- **Time:** Likely O(n) - good efficiency!\n"
    else:
        review += "- **Time:** Possibly O(1) or O(log n) - efficient!\n"
    
    # Issues
    if issues:
        review += "\n### Suggestions:\n\n"
        for issue in issues:
            review += f"⚠️ **{issue['issue']}**\n{issue['fix']}\n\n"
    
    # Positive closing
    review += "\n---\n**Overall:** Keep practicing! Each problem makes you stronger. 💪"
    
    return review


def get_bug_hint(code: str, error_message: str, question: str, function_name: str) -> str:
    """Provide detailed bug analysis and hints."""
    
    response = f"""## 🔍 Bug Analysis for `{function_name}`

"""
    
    error_lower = error_message.lower()
    
    # Specific error analysis
    if "indentation" in error_lower:
        response += """### IndentationError

**What it means:** Python uses indentation to define code blocks.

**Common causes:**
- Mixed tabs and spaces
- Inconsistent indentation levels
- Missing indentation after `if`, `for`, `while`, `def`, etc.

**Fix:**
```python
# Wrong
def my_function():
result = 0  # Not indented!

# Correct
def my_function():
    result = 0  # Indented with 4 spaces
```

**Tip:** Configure your editor to use 4 spaces for tabs."""

    elif "name" in error_lower and "not defined" in error_lower:
        # Extract the undefined name if possible
        match = re.search(r"name '(\w+)' is not defined", error_message)
        var_name = match.group(1) if match else "variable"
        
        response += f"""### NameError: '{var_name}' is not defined

**What it means:** You're using a name that Python doesn't recognize.

**Common causes:**
1. **Typo:** Check spelling of `{var_name}`
2. **Not defined yet:** Define before using
3. **Scope issue:** Variable defined inside function/loop
4. **Case sensitivity:** `myVar` ≠ `myvar`

**Fix:**
```python
# Make sure to define before use
{var_name} = initial_value  # Define first
print({var_name})  # Then use
```"""

    elif "type" in error_lower:
        response += """### TypeError

**What it means:** Operation on incompatible types.

**Common causes:**
1. Adding string + number
2. Wrong number of arguments
3. Calling non-callable object
4. None + something

**Fixes:**
```python
# String + int
result = "Value: " + str(42)  # Convert int to str

# Or use f-string
result = f"Value: {42}"

# Check for None before operations
if value is not None:
    result = value + 1
```"""

    elif "index" in error_lower:
        response += """### IndexError

**What it means:** Trying to access an index that doesn't exist.

**Common causes:**
1. Empty list access
2. Off-by-one in loop
3. Negative index too large

**Fixes:**
```python
# Check before access
if arr:  # or len(arr) > 0
    first = arr[0]

# Check index bounds
if 0 <= index < len(arr):
    element = arr[index]

# Be careful with loops
for i in range(len(arr)):  # Goes 0 to len-1
    print(arr[i])
```"""

    elif "key" in error_lower:
        response += """### KeyError

**What it means:** Dictionary key doesn't exist.

**Fixes:**
```python
# Use .get() with default
value = my_dict.get('key', default_value)

# Check before access
if 'key' in my_dict:
    value = my_dict['key']

# Use defaultdict
from collections import defaultdict
my_dict = defaultdict(int)  # Default 0
my_dict['new_key'] += 1  # Works!
```"""

    elif "syntax" in error_lower:
        response += """### SyntaxError

**What it means:** Python can't understand your code structure.

**Common causes:**
1. Missing colon after `if`, `for`, `while`, `def`, `class`
2. Unmatched parentheses, brackets, or quotes
3. Invalid characters
4. Wrong indentation

**Checklist:**
- [ ] Colon after if/for/while/def?
- [ ] Matching `(` and `)`?
- [ ] Matching `[` and `]`?
- [ ] Matching quotes `"` or `'`?
- [ ] No Python keywords as variable names?"""

    elif "return" in error_lower or ("none" in error_lower and "+" in error_lower):
        response += f"""### None/Return Issue

**What it means:** Your function returns None instead of a value.

**Common causes:**
1. Using `print()` instead of `return`
2. Missing return statement
3. Return only in some code paths

**Fix for `{function_name}`:**
```python
def {function_name}(n):
    result = ...  # Calculate
    return result  # Don't forget this!
```

**Check:** Every code path should return something."""

    else:
        # General debug help
        response += """### General Debug Tips

1. **Read the error message carefully**
   - Line number tells you where
   - Error type tells you what

2. **Add print statements**
```python
print(f"Input: {input_value}")
print(f"After step 1: {intermediate}")
print(f"Final: {result}")
```

3. **Check your assumptions**
   - What type is each variable?
   - What value at each step?

4. **Simplify**
   - Test with smallest input
   - Comment out parts to isolate issue"""

    # Add code-specific issues
    code_issues = analyze_code(code)
    if code_issues:
        response += "\n\n### Also Found in Your Code:\n"
        for issue in code_issues[:2]:
            response += f"\n⚠️ **{issue['issue']}:** {issue['fix']}"

    return response


def get_smart_hint(code: str, question: str, function_name: str, static_hints: list, hint_level: int) -> str:
    """Generate progressive, intelligent hints."""
    
    hints_data = get_problem_hints(question, function_name)
    code_issues = analyze_code(code)
    
    # Level 1: Conceptual hint
    if hint_level == 1:
        return f"""## 💡 Hint 1: Concept

**This problem is about:** {hints_data['concept']}

**Think about:**
- {hints_data['hints'][0]}

**Key question:** What type of result should you return?

*Need more help? Ask for another hint!*"""

    # Level 2: Approach hint
    if hint_level == 2:
        hint = hints_data['hints'][1] if len(hints_data['hints']) > 1 else hints_data['hints'][0]
        
        response = f"""## 💡 Hint 2: Approach

**Strategy:** {hint}

**Suggested structure:**
```python
def {function_name}(...):
    # 1. Handle edge case
    # 2. Initialize result
    # 3. Process input
    # 4. Return result
```
"""
        
        if code_issues:
            response += f"\n**⚠️ In your code:** {code_issues[0]['issue']}"
        
        return response

    # Level 3: More specific
    if hint_level == 3:
        hint = hints_data['hints'][2] if len(hints_data['hints']) > 2 else static_hints[0] if static_hints else hints_data['hints'][-1]
        
        template_section = ""
        if hints_data.get('template'):
            template_code = hints_data.get('template', '')
            template_section = f"**Template:**\n```python\n{template_code}\n```"
        
        return f"""## 💡 Hint 3: Details

**Specific tip:** {hint}

**Common patterns for this type:**
- Loop through elements
- Track state in a variable
- Build result incrementally

{template_section}

*Almost there! One more hint available.*"""

    # Level 4+: Strong hint with example
    default_template = f"def {function_name}(n):\n    # Your logic here\n    result = 0\n    # Process input\n    return result"
    template = hints_data.get('template', default_template)
    
    return f"""## 💡 Hint {hint_level}: Nearly Complete

**Here's a template to follow:**
```python
{template}
```

**Key insights:**
1. {hints_data['hints'][0]}
2. {hints_data['hints'][1] if len(hints_data['hints']) > 1 else 'Start simple'}
3. Test with the provided examples

**You're so close!** Try implementing this structure. 💪"""
