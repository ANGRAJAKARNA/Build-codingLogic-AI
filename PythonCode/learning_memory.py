# learning_memory.py
"""
Advanced Self-Learning Memory Module for PyCode AI Chatbot

Provides intelligent learning capabilities:
1. ConversationMemory - Persistent storage with user profiling
2. FeedbackLearner - Learning from feedback with correction reuse
3. SmartMatcher - Advanced similarity matching for Q&A
4. ConfidenceScorer - Track and display response confidence

Key Features:
- Remember past conversations across sessions
- Learn from user ratings to improve responses
- ACTIVELY USE user corrections for future responses
- Track user skill level and adapt responses
- Confidence scoring for responses
- Smart question similarity matching
"""

import json
import os
import re
import math
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple

from persistence import atomic_write_json, get_visitor_dir


# =============================================================================
# SMART MATCHER - Advanced similarity matching with stemming & synonyms
# =============================================================================

# Common misspellings / typos mapping for programming terms
TYPO_CORRECTIONS = {
    # Selenium variations
    "slenium": "selenium", "selinium": "selenium", "selenum": "selenium",
    "selnium": "selenium", "selemium": "selenium", "celenium": "selenium",
    "seleniun": "selenium", "seleniam": "selenium", "selineum": "selenium",
    
    # Python variations
    "pyhton": "python", "pythn": "python", "pyton": "python",
    "pythom": "python", "phyton": "python", "pytho": "python",
    
    # Dictionary variations
    "dictonary": "dictionary", "dictionry": "dictionary", "dictinary": "dictionary",
    "dicionary": "dictionary", "dicitonary": "dictionary", "dict": "dictionary",
    
    # Function variations
    "funciton": "function", "fucntion": "function", "funtion": "function",
    "functoin": "function", "functon": "function", "fnction": "function",
    
    # Variable variations
    "varible": "variable", "variabel": "variable", "varialbe": "variable",
    "veriable": "variable", "varaible": "variable",
    
    # String variations
    "stirng": "string", "strng": "string", "strig": "string",
    "sring": "string", "strign": "string",
    
    # Class variations
    "calss": "class", "clas": "class", "claass": "class",
    
    # List variations
    "lsit": "list", "lis": "list", "liist": "list",
    
    # Loop variations
    "lop": "loop", "lopp": "loop", "lool": "loop",
    
    # Tuple variations
    "tupe": "tuple", "tupel": "tuple", "tupple": "tuple", "tupl": "tuple",
    
    # Exception/Error variations
    "execption": "exception", "exeption": "exception", "excepton": "exception",
    "eror": "error", "erro": "error", "errror": "error",
    
    # Inheritance variations
    "inheritence": "inheritance", "inheratance": "inheritance", "inheritane": "inheritance",
    
    # Method variations
    "methd": "method", "metod": "method", "mehod": "method",
    
    # Return variations
    "retrun": "return", "retur": "return", "retrn": "return",
    
    # Import variations
    "improt": "import", "imort": "import", "impor": "import",
    
    # Iterator/Iteration variations
    "iterater": "iterator", "itterator": "iterator", "itertor": "iterator",
    "iterration": "iteration", "iteratin": "iteration",
    
    # Boolean variations
    "boolen": "boolean", "boolena": "boolean", "booean": "boolean",
    "true": "True", "flase": "false", "fasle": "false",
    
    # Object variations
    "obect": "object", "objct": "object", "objetc": "object",
    
    # Argument/Parameter variations
    "argumet": "argument", "arguemnt": "argument", "argumnet": "argument",
    "paramter": "parameter", "paramerter": "parameter", "paramenter": "parameter",
    
    # Global/Local variations
    "gobal": "global", "golbal": "global", "gloabl": "global",
    "locla": "local", "loacl": "local",
    
    # Lambda variations
    "lamda": "lambda", "lamba": "lambda", "lambad": "lambda",
    
    # Recursion variations
    "recurison": "recursion", "recursoin": "recursion", "recusion": "recursion",
    "recusrion": "recursion",
    
    # Decorator variations
    "decorater": "decorator", "decotator": "decorator", "decortor": "decorator",
    
    # Comprehension variations
    "comprehention": "comprehension", "comprhension": "comprehension",
    "comrehension": "comprehension",
    
    # Array variations
    "aray": "array", "arry": "array", "arra": "array",
    
    # Algorithm variations
    "algoritm": "algorithm", "algorith": "algorithm", "algorithim": "algorithm",
    "algortihm": "algorithm",
    
    # Integer/Float variations
    "interger": "integer", "intger": "integer", "integr": "integer",
    "flot": "float", "flaot": "float",
    
    # Pytest/Robot Framework variations
    "pytset": "pytest", "pyest": "pytest", "pytet": "pytest",
    "robort": "robot", "robto": "robot", "robt": "robot",
    "framwork": "framework", "freework": "framework", "framewrok": "framework",
    
    # XPath/CSS variations
    "xpth": "xpath", "xpaht": "xpath",
    "seletor": "selector", "selecter": "selector", "selctor": "selector",
    
    # API variations
    "restapi": "rest_api", "reast": "rest", "rstapi": "restapi",
    
    # Browser variations
    "browsr": "browser", "broswer": "browser", "borwser": "browser",
    "chromee": "chrome", "chorme": "chrome",
    "fireofx": "firefox", "firfox": "firefox",
    
    # Element/Locator variations
    "elemnt": "element", "eleemnt": "element", "elment": "element",
    "locater": "locator", "loactor": "locator",
    
    # Debug variations
    "debg": "debug", "debgu": "debug", "deubg": "debug",
    
    # Assert variations  
    "assret": "assert", "asert": "assert", "asssert": "assert",
    
    # Module/Package variations
    "modul": "module", "moduel": "module", "moudule": "module",
    "pacakge": "package", "pakage": "package", "packge": "package",
}

# Synonym mapping for common programming terms
SYNONYMS = {
    # Data structures
    "list": ["array", "collection", "sequence", "arr"],
    "dict": ["dictionary", "hashmap", "map", "hash", "mapping"],
    "tuple": ["immutable_list", "record"],
    "set": ["unique_collection", "hashset"],
    
    # Operations
    "append": ["add", "push", "insert", "extend"],
    "remove": ["delete", "pop", "discard", "drop"],
    "iterate": ["loop", "traverse", "cycle", "walk"],
    "function": ["method", "func", "def", "procedure", "routine"],
    
    # OOP
    "class": ["object", "type", "blueprint"],
    "inheritance": ["extend", "inherit", "subclass", "derive"],
    "instance": ["object", "entity"],
    
    # Control flow
    "loop": ["iteration", "for", "while", "repeat", "cycle"],
    "condition": ["if", "else", "elif", "branch", "switch"],
    "exception": ["error", "except", "try", "catch", "raise"],
    
    # Python specific
    "decorator": ["wrapper", "annotation"],
    "generator": ["yield", "iterator", "lazy"],
    "comprehension": ["listcomp", "dictcomp", "genexp"],
    "lambda": ["anonymous", "inline", "arrow"],
    
    # Testing/Automation
    "selenium": ["webdriver", "browser_automation", "web_testing"],
    "pytest": ["test", "fixture", "testing", "unittest"],
    "robot": ["robotframework", "keyword_driven", "rf"],
    "xpath": ["locator", "selector", "path"],
    "element": ["webelement", "node", "tag"],
    
    # General
    "create": ["make", "new", "initialize", "construct", "build"],
    "get": ["fetch", "retrieve", "obtain", "access", "read"],
    "check": ["verify", "validate", "test", "assert", "confirm"],
    "string": ["str", "text", "chars"],
    "integer": ["int", "number", "num"],
    "variable": ["var", "value", "data"],
}

# Build reverse synonym lookup
REVERSE_SYNONYMS = {}
for key, synonyms in SYNONYMS.items():
    REVERSE_SYNONYMS[key] = key  # Map to self
    for syn in synonyms:
        REVERSE_SYNONYMS[syn] = key  # Map synonym to canonical form


class SmartMatcher:
    """
    Advanced text similarity matching with:
    - Word stemming (removes common suffixes)
    - Synonym expansion (dict = dictionary = hashmap)
    - Optional semantic search with sentence-transformers
    """
    
    # Stop words to ignore in matching
    STOP_WORDS = {
        'what', 'is', 'the', 'a', 'an', 'how', 'do', 'does', 'can', 'you', 
        'me', 'tell', 'about', 'explain', 'i', 'want', 'to', 'know', 'please',
        'could', 'would', 'should', 'why', 'when', 'where', 'which', 'are',
        'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having',
        'this', 'that', 'these', 'those', 'my', 'your', 'his', 'her', 'its',
        'give', 'show', 'need', 'use', 'using', 'used', 'work', 'works'
    }
    
    # Semantic model (lazy loaded)
    _semantic_model = None
    _embeddings_cache = {}
    SEMANTIC_AVAILABLE = False
    
    @staticmethod
    def levenshtein_distance(s1: str, s2: str) -> int:
        """
        Calculate Levenshtein (edit) distance between two strings.
        This measures how many single-character edits are needed to transform s1 into s2.
        """
        if len(s1) < len(s2):
            return SmartMatcher.levenshtein_distance(s2, s1)
        
        if len(s2) == 0:
            return len(s1)
        
        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                # j+1 instead of j since previous_row and current_row are one character longer
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        
        return previous_row[-1]
    
    @staticmethod
    def correct_spelling(word: str) -> str:
        """
        Correct common spelling mistakes in programming terms.
        
        Uses:
        1. Direct typo lookup (for known misspellings)
        2. Levenshtein distance for fuzzy matching against known terms
        
        Returns the corrected word or original if no correction found.
        """
        word_lower = word.lower()
        
        # 1. Direct lookup in typo corrections
        if word_lower in TYPO_CORRECTIONS:
            return TYPO_CORRECTIONS[word_lower]
        
        # 2. Check against known terms using Levenshtein distance
        # Only try fuzzy matching for words that are reasonably long
        if len(word_lower) >= 4:
            # Known programming terms to match against
            KNOWN_TERMS = set(SYNONYMS.keys()) | set(sum(SYNONYMS.values(), [])) | {
                # Testing/Automation
                'selenium', 'python', 'pytest', 'robot', 'framework', 'xpath', 'css',
                'browser', 'chrome', 'firefox', 'safari', 'edge', 'element', 'locator',
                'click', 'send', 'keys', 'wait', 'scroll', 'assert', 'verify',
                # General programming
                'database', 'api', 'rest', 'json', 'xml', 'html', 'script',
                'module', 'package', 'import', 'export', 'async', 'await',
                'promise', 'callback', 'closure', 'scope', 'global', 'local',
                'recursion', 'algorithm', 'sorting', 'searching', 'binary',
                'linked', 'stack', 'queue', 'tree', 'graph', 'heap',
                'debugging', 'testing', 'automation', 'integration', 'unit',
                # Linux/Shell - IMPORTANT: These should NOT be corrected
                'bash', 'shell', 'linux', 'unix', 'terminal', 'console', 'command',
                'chmod', 'chown', 'grep', 'awk', 'sed', 'find', 'xargs', 'pipe',
                'stdout', 'stdin', 'stderr', 'sudo', 'root', 'user', 'group',
                'systemd', 'service', 'daemon', 'cron', 'crontab', 'process',
                'kernel', 'filesystem', 'mount', 'disk', 'partition',
                # Networking
                'tcp', 'udp', 'http', 'https', 'ftp', 'ssh', 'dns', 'dhcp',
                'socket', 'port', 'network', 'firewall', 'iptables',
                # Data structures
                'hash', 'list', 'dict', 'array', 'tuple', 'set', 'map',
                # DevOps
                'docker', 'kubernetes', 'jenkins', 'ansible', 'terraform',
                'nginx', 'apache', 'redis', 'mongodb', 'mysql', 'postgres',
                # Common plurals - should NOT be corrected to singular
                'classes', 'functions', 'methods', 'variables', 'modules', 'packages',
                'lists', 'dicts', 'dictionaries', 'tuples', 'sets', 'strings',
                'loops', 'iterators', 'generators', 'decorators', 'exceptions',
                'objects', 'instances', 'attributes', 'arguments', 'parameters',
                'imports', 'exports', 'tests', 'fixtures', 'assertions',
                'elements', 'locators', 'selectors', 'drivers', 'browsers',
                'files', 'directories', 'paths', 'commands', 'scripts',
                # Selenium-specific - waits is a valid concept name!
                'waits', 'actions', 'alerts', 'frames', 'cookies', 'screenshots',
                # Linux commands - should not be corrected
                'chmod', 'chown', 'chgrp', 'mkdir', 'rmdir', 'touch', 'nano', 'vim'
            }
            
            # IMPORTANT: If the word is already a known term, don't try to correct it
            if word_lower in KNOWN_TERMS:
                return word_lower
            
            best_match = None
            best_distance = float('inf')
            
            for term in KNOWN_TERMS:
                # Only compare with terms of similar length (within 2 chars)
                if abs(len(term) - len(word_lower)) <= 2:
                    distance = SmartMatcher.levenshtein_distance(word_lower, term)
                    # Accept if distance is small relative to word length
                    # For short words (4-6 chars): max 1 edit
                    # For medium words (7-10 chars): max 2 edits
                    # For long words (11+ chars): max 3 edits
                    max_distance = 1 if len(word_lower) <= 6 else (2 if len(word_lower) <= 10 else 3)
                    
                    if distance <= max_distance and distance < best_distance:
                        best_distance = distance
                        best_match = term
            
            if best_match:
                return best_match
        
        return word_lower
    
    @staticmethod
    def stem_word(word: str) -> str:
        """
        Simple word stemming - removes common suffixes.
        Examples: running -> run, appending -> append, listed -> list
        """
        word = word.lower()
        
        # Handle special cases first
        if word in ['running', 'using', 'being']:
            return word[:-4] + word[-4]  # Keep as is for ambiguous cases
        
        # Remove common suffixes (order matters - longest first)
        suffixes = [
            ('ying', 'y'),      # copying -> copy
            ('ying', 'ie'),     # lying -> lie
            ('ation', ''),      # iteration -> iter
            ('tion', ''),       # function -> func (careful)
            ('ment', ''),       # element -> ele
            ('ning', 'n'),      # running -> run (doubled consonant)
            ('ting', 't'),      # getting -> get
            ('ping', 'p'),      # stopping -> stop
            ('ming', 'm'),      # programming -> program
            ('ding', 'd'),      # adding -> add
            ('bing', 'b'),      # grabbing -> grab
            ('ging', 'g'),      # debugging -> debug
            ('sing', 's'),      # processing -> process
            ('zing', 'z'),      # initializing -> initialize
            ('ing', ''),        # general -ing removal
            ('ies', 'y'),       # dictionaries -> dictionary
            ('es', ''),         # classes -> class
            ('ed', ''),         # called -> call
            ('ly', ''),         # quickly -> quick
            ('er', ''),         # faster -> fast
            ('est', ''),        # fastest -> fast
            ('s', ''),          # lists -> list
        ]
        
        for suffix, replacement in suffixes:
            if word.endswith(suffix) and len(word) > len(suffix) + 2:
                stemmed = word[:-len(suffix)] + replacement
                # Don't over-stem short words
                if len(stemmed) >= 3:
                    return stemmed
        
        return word
    
    @staticmethod
    def normalize_word(word: str) -> str:
        """
        Normalize a word using:
        1. Spelling correction (typo fixing)
        2. Stemming (suffix removal)
        3. Synonym mapping (canonical form)
        """
        # First, correct any spelling mistakes
        corrected = SmartMatcher.correct_spelling(word)
        # Then stem the corrected word
        stemmed = SmartMatcher.stem_word(corrected)
        # Map to canonical form if it's a known synonym
        return REVERSE_SYNONYMS.get(stemmed, stemmed)
    
    @staticmethod
    def extract_keywords(text: str, include_corrections: bool = True) -> set:
        """
        Extract and normalize meaningful keywords from text.
        
        Args:
            text: Input text to extract keywords from
            include_corrections: If True, also include the original word if spelling was corrected
        """
        # Lowercase and split
        words = re.findall(r'\b[a-z_][a-z0-9_]*\b', text.lower())
        # Filter stop words, normalize, and filter short words
        normalized = set()
        for w in words:
            if w not in SmartMatcher.STOP_WORDS and len(w) > 2:
                normalized.add(SmartMatcher.normalize_word(w))
        return normalized
    
    @staticmethod
    def get_spelling_corrections(text: str) -> dict:
        """
        Find spelling mistakes in text and return corrections.
        
        Returns:
            Dict mapping original misspelled word to corrected word.
            Only includes words that were actually corrected.
        """
        corrections = {}
        words = re.findall(r'\b[a-z_][a-z0-9_]*\b', text.lower())
        
        for word in words:
            if word in SmartMatcher.STOP_WORDS or len(word) <= 2:
                continue
            
            corrected = SmartMatcher.correct_spelling(word)
            if corrected != word:
                corrections[word] = corrected
        
        return corrections
    
    @staticmethod
    def correct_text(text: str) -> tuple:
        """
        Correct spelling in entire text.
        
        Returns:
            Tuple of (corrected_text, corrections_dict)
        """
        corrections = SmartMatcher.get_spelling_corrections(text)
        corrected_text = text
        
        for wrong, right in corrections.items():
            # Case-insensitive replacement
            import re as re_module
            corrected_text = re_module.sub(
                re_module.escape(wrong), 
                right, 
                corrected_text, 
                flags=re_module.IGNORECASE
            )
        
        return corrected_text, corrections
    
    @staticmethod
    def expand_with_synonyms(words: set) -> set:
        """Expand a word set to include all known synonyms."""
        expanded = set(words)
        for word in words:
            # If word is a canonical form, add its synonyms
            if word in SYNONYMS:
                expanded.update(SYNONYMS[word])
            # Also add the canonical form
            if word in REVERSE_SYNONYMS:
                canonical = REVERSE_SYNONYMS[word]
                expanded.add(canonical)
                if canonical in SYNONYMS:
                    expanded.update(SYNONYMS[canonical])
        return expanded
    
    @staticmethod
    def calculate_similarity(text1: str, text2: str, use_semantic: bool = False) -> float:
        """
        Calculate similarity score between two texts.
        
        Args:
            text1: First text
            text2: Second text
            use_semantic: If True and available, use semantic embeddings
            
        Returns:
            Score between 0.0 and 1.0
        """
        # Try semantic search first if requested and available
        if use_semantic and SmartMatcher.SEMANTIC_AVAILABLE:
            try:
                return SmartMatcher._semantic_similarity(text1, text2)
            except Exception:
                pass  # Fall back to keyword matching
        
        # Extract and normalize keywords
        words1 = SmartMatcher.extract_keywords(text1)
        words2 = SmartMatcher.extract_keywords(text2)
        
        if not words1 or not words2:
            return 0.0
        
        # Expand with synonyms for better matching
        expanded1 = SmartMatcher.expand_with_synonyms(words1)
        expanded2 = SmartMatcher.expand_with_synonyms(words2)
        
        # Calculate intersection using expanded sets
        # But use original sets for union to avoid over-counting
        intersection = len(expanded1 & expanded2)
        union = len(words1 | words2)
        
        if union == 0:
            return 0.0
        
        # Modified Jaccard with synonym boost
        base_score = intersection / union
        
        # Bonus for direct word matches (not just synonym matches)
        direct_matches = len(words1 & words2)
        direct_bonus = direct_matches * 0.1
        
        # Bonus for exact phrase in text
        phrase_bonus = 0.0
        text1_lower = text1.lower()
        text2_lower = text2.lower()
        for word in words1:
            if word in text2_lower:
                phrase_bonus += 0.03
        
        return min(1.0, base_score + direct_bonus + phrase_bonus)
    
    @staticmethod
    def _init_semantic_model():
        """Lazy-load the semantic model."""
        if SmartMatcher._semantic_model is not None:
            return True
        
        try:
            from sentence_transformers import SentenceTransformer
            # Use a small, fast model
            SmartMatcher._semantic_model = SentenceTransformer('all-MiniLM-L6-v2')
            SmartMatcher.SEMANTIC_AVAILABLE = True
            return True
        except ImportError:
            SmartMatcher.SEMANTIC_AVAILABLE = False
            return False
    
    @staticmethod
    def _get_embedding(text: str):
        """Get embedding for text, using cache."""
        if text in SmartMatcher._embeddings_cache:
            return SmartMatcher._embeddings_cache[text]
        
        if not SmartMatcher._init_semantic_model():
            return None
        
        embedding = SmartMatcher._semantic_model.encode(text)
        # Cache with size limit
        if len(SmartMatcher._embeddings_cache) > 1000:
            # Remove oldest entries (simple approach)
            keys = list(SmartMatcher._embeddings_cache.keys())[:100]
            for k in keys:
                del SmartMatcher._embeddings_cache[k]
        
        SmartMatcher._embeddings_cache[text] = embedding
        return embedding
    
    @staticmethod
    def _semantic_similarity(text1: str, text2: str) -> float:
        """Calculate semantic similarity using embeddings."""
        emb1 = SmartMatcher._get_embedding(text1)
        emb2 = SmartMatcher._get_embedding(text2)
        
        if emb1 is None or emb2 is None:
            return 0.0
        
        # Cosine similarity
        import numpy as np
        dot = np.dot(emb1, emb2)
        norm1 = np.linalg.norm(emb1)
        norm2 = np.linalg.norm(emb2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return float(dot / (norm1 * norm2))
    
    @staticmethod
    def find_best_match(query: str, candidates: List[Dict], 
                        key: str = "q", threshold: float = 0.25,
                        use_semantic: bool = False) -> Optional[Tuple[Dict, float]]:
        """
        Find the best matching candidate for a query.
        
        Args:
            query: The search query
            candidates: List of dicts to search
            key: Dict key containing text to match
            threshold: Minimum similarity score to return (lowered from 0.3)
            use_semantic: Use semantic embeddings if available
            
        Returns:
            Tuple of (best_match_dict, score) or None
        """
        best_match = None
        best_score = 0.0
        
        # Try semantic search first if available and there are many candidates
        if use_semantic and len(candidates) > 0:
            try:
                SmartMatcher._init_semantic_model()
            except Exception:
                pass
        
        for candidate in candidates:
            if key not in candidate:
                continue
            
            # Calculate similarity
            score = SmartMatcher.calculate_similarity(
                query, candidate[key], 
                use_semantic=use_semantic and SmartMatcher.SEMANTIC_AVAILABLE
            )
            
            if score > best_score:
                best_score = score
                best_match = candidate
        
        if best_score >= threshold:
            return (best_match, best_score)
        return None
    
    @staticmethod
    def is_semantic_available() -> bool:
        """Check if semantic search is available."""
        return SmartMatcher._init_semantic_model()


# =============================================================================
# CONFIDENCE SCORER - Track response confidence
# =============================================================================

class ConfidenceScorer:
    """Calculate and track confidence scores for responses."""
    
    # Confidence levels
    LEVELS = {
        (0.0, 0.3): ("low", "🔴"),
        (0.3, 0.6): ("medium", "🟡"),
        (0.6, 0.8): ("high", "🟢"),
        (0.8, 1.0): ("very_high", "⭐"),
    }
    
    @staticmethod
    def calculate_confidence(
        source: str,
        similarity_score: float = 0.0,
        feedback_score: int = 0,
        times_used: int = 0
    ) -> Dict:
        """
        Calculate confidence score for a response.
        
        Args:
            source: Where the response came from ('correction', 'learned', 'generated')
            similarity_score: How similar the query was to stored data (0-1)
            feedback_score: User feedback score (positive count)
            times_used: How many times this response was used
            
        Returns:
            Dict with confidence score, level, and icon
        """
        # Base confidence by source
        source_weights = {
            "correction": 0.9,      # User corrections are highly trusted
            "learned_exact": 0.85,  # Exact match from learned
            "learned_similar": 0.7, # Similar match from learned
            "generated": 0.5,       # Generated response
            "fallback": 0.3         # Fallback/default response
        }
        
        base = source_weights.get(source, 0.5)
        
        # Boost from similarity
        similarity_boost = similarity_score * 0.2
        
        # Boost from positive feedback (diminishing returns)
        feedback_boost = min(0.2, math.log(feedback_score + 1) * 0.05)
        
        # Boost from usage (trust increases with use)
        usage_boost = min(0.1, times_used * 0.02)
        
        # Calculate final score (capped at 1.0)
        score = min(1.0, base + similarity_boost + feedback_boost + usage_boost)
        
        # Determine level and icon
        level, icon = "medium", "🟡"
        for (low, high), (lvl, ico) in ConfidenceScorer.LEVELS.items():
            if low <= score < high:
                level, icon = lvl, ico
                break
        
        return {
            "score": round(score, 2),
            "level": level,
            "icon": icon,
            "source": source,
            "details": {
                "base": round(base, 2),
                "similarity_boost": round(similarity_boost, 2),
                "feedback_boost": round(feedback_boost, 2),
                "usage_boost": round(usage_boost, 2)
            }
        }


# =============================================================================
# CONVERSATION MEMORY - Persistent memory across sessions
# =============================================================================

class ConversationMemory:
    """
    Persistent conversation memory that stores Q&A pairs,
    user preferences, and enables context-aware responses.
    """
    
    def __init__(self, file_path: str = "chat_memory.json"):
        self.file_path = file_path
        self.memory = self._load()
        self._ensure_structure()
    
    def _ensure_structure(self):
        """Ensure all required keys exist in memory."""
        defaults = {
            "user_preferences": {},
            "past_qa": [],
            "learned_facts": [],
            "session_count": 0,
            "topics_asked": {},
            "last_session": None,
            "user_profile": {
                "skill_level": "unknown",  # beginner, intermediate, advanced, unknown
                "interests": [],           # Most asked topics
                "response_preference": "detailed",  # concise, detailed
                "questions_count": 0,
                "correct_answers": 0,
                "topics_mastered": []
            }
        }
        for key, value in defaults.items():
            if key not in self.memory:
                self.memory[key] = value
        
        # Ensure user_profile sub-keys exist
        if "user_profile" not in self.memory:
            self.memory["user_profile"] = defaults["user_profile"]
        else:
            for k, v in defaults["user_profile"].items():
                if k not in self.memory["user_profile"]:
                    self.memory["user_profile"][k] = v
    
    def _load(self) -> Dict:
        """Load memory from JSON file."""
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
        return {}
    
    def _save(self):
        """Save memory to JSON file (atomic — safe if the same visitor has
        two tabs open writing concurrently)."""
        try:
            atomic_write_json(self.file_path, self.memory)
        except (IOError, OSError):
            pass
    
    def remember_preference(self, key: str, value: Any):
        """
        Store a user preference.
        
        Examples:
            memory.remember_preference("skill_level", "intermediate")
            memory.remember_preference("preferred_topics", ["selenium", "pytest"])
        """
        self.memory["user_preferences"][key] = value
        self._save()
    
    def get_user_preferences(self) -> Dict:
        """Get all stored user preferences."""
        return self.memory.get("user_preferences", {})
    
    def get_preference(self, key: str, default: Any = None) -> Any:
        """Get a specific user preference."""
        return self.memory.get("user_preferences", {}).get(key, default)
    
    def store_qa(self, question: str, answer: str, topic: str = None, rating: int = None):
        """
        Store a Q&A pair for future reference.
        
        Args:
            question: User's question
            answer: Bot's response
            topic: Detected topic (optional)
            rating: User rating 1-5 (optional, can be added later)
        """
        qa_entry = {
            "q": question,
            "a": answer[:500],  # Truncate long answers
            "topic": topic,
            "rating": rating,
            "timestamp": datetime.now().isoformat()
        }
        self.memory["past_qa"].append(qa_entry)
        
        # Track topic frequency
        if topic:
            topics = self.memory.get("topics_asked", {})
            topics[topic] = topics.get(topic, 0) + 1
            self.memory["topics_asked"] = topics
        
        # Keep only last 100 Q&A pairs to manage file size
        if len(self.memory["past_qa"]) > 100:
            self.memory["past_qa"] = self.memory["past_qa"][-100:]
        
        self._save()
    
    def update_qa_rating(self, question: str, rating: int):
        """Update rating for an existing Q&A pair."""
        for qa in reversed(self.memory["past_qa"]):
            if qa["q"] == question:
                qa["rating"] = rating
                self._save()
                return True
        return False
    
    def get_relevant_context(self, query: str, limit: int = 3) -> List[Dict]:
        """
        Find relevant past Q&A pairs based on query similarity.
        Uses simple keyword matching for efficiency.
        
        Args:
            query: Current user query
            limit: Maximum number of results
            
        Returns:
            List of relevant Q&A dictionaries
        """
        query_words = set(query.lower().split())
        # Remove common words
        stop_words = {'what', 'is', 'the', 'a', 'an', 'how', 'do', 'does', 'can', 'you', 'me', 'tell', 'about', 'explain'}
        query_words -= stop_words
        
        if not query_words:
            return []
        
        scored_qa = []
        for qa in self.memory.get("past_qa", []):
            q_words = set(qa["q"].lower().split())
            # Score based on word overlap
            overlap = len(query_words & q_words)
            if overlap > 0:
                # Boost highly-rated responses
                rating_boost = (qa.get("rating") or 3) / 5
                score = overlap * rating_boost
                scored_qa.append((score, qa))
        
        # Sort by score descending
        scored_qa.sort(key=lambda x: x[0], reverse=True)
        return [qa for _, qa in scored_qa[:limit]]
    
    def get_topic_history(self, topic: str, limit: int = 5) -> List[Dict]:
        """Get past Q&A for a specific topic."""
        return [
            qa for qa in self.memory.get("past_qa", [])
            if qa.get("topic") == topic
        ][-limit:]
    
    def get_frequent_topics(self, limit: int = 5) -> List[tuple]:
        """Get most frequently asked topics."""
        topics = self.memory.get("topics_asked", {})
        sorted_topics = sorted(topics.items(), key=lambda x: x[1], reverse=True)
        return sorted_topics[:limit]
    
    def add_learned_fact(self, topic: str, fact: str):
        """Store a new fact learned from user interaction."""
        self.memory["learned_facts"].append({
            "topic": topic,
            "fact": fact,
            "timestamp": datetime.now().isoformat()
        })
        # Keep only last 50 facts
        if len(self.memory["learned_facts"]) > 50:
            self.memory["learned_facts"] = self.memory["learned_facts"][-50:]
        self._save()
    
    def get_learned_facts(self, topic: str = None) -> List[Dict]:
        """Get learned facts, optionally filtered by topic."""
        facts = self.memory.get("learned_facts", [])
        if topic:
            return [f for f in facts if f.get("topic") == topic]
        return facts
    
    def increment_session(self):
        """Increment session count and update last session time."""
        self.memory["session_count"] = self.memory.get("session_count", 0) + 1
        self.memory["last_session"] = datetime.now().isoformat()
        self._save()
    
    def get_stats(self) -> Dict:
        """Get memory statistics."""
        return {
            "total_qa": len(self.memory.get("past_qa", [])),
            "total_facts": len(self.memory.get("learned_facts", [])),
            "session_count": self.memory.get("session_count", 0),
            "topics_count": len(self.memory.get("topics_asked", {})),
            "top_topics": self.get_frequent_topics(3),
            "user_profile": self.memory.get("user_profile", {})
        }
    
    # =========================================================================
    # USER PROFILE TRACKING - Adaptive learning based on user behavior
    # =========================================================================
    
    def update_user_profile(self, question: str, topic: str = None, was_helpful: bool = None):
        """
        Update user profile based on interaction.
        Tracks skill level, interests, and preferences.
        """
        profile = self.memory.get("user_profile", {})
        
        # Increment question count
        profile["questions_count"] = profile.get("questions_count", 0) + 1
        
        # Track topics of interest
        if topic:
            interests = profile.get("interests", [])
            if topic not in interests:
                interests.append(topic)
                # Keep only top 10 interests
                if len(interests) > 10:
                    # Remove least frequent
                    topic_counts = self.memory.get("topics_asked", {})
                    interests.sort(key=lambda t: topic_counts.get(t, 0), reverse=True)
                    interests = interests[:10]
            profile["interests"] = interests
        
        # Track successful interactions
        if was_helpful:
            profile["correct_answers"] = profile.get("correct_answers", 0) + 1
        
        # Infer skill level from question complexity
        self._update_skill_level(question, profile)
        
        self.memory["user_profile"] = profile
        self._save()
    
    def _update_skill_level(self, question: str, profile: Dict):
        """Infer user skill level from question patterns."""
        q_lower = question.lower()
        
        # Advanced indicators
        advanced_keywords = [
            'decorator', 'metaclass', 'asyncio', 'coroutine', 'generator',
            'descriptor', 'context manager', 'abc', 'abstract', 'mixin',
            'multithreading', 'multiprocessing', 'gil', 'bytecode', 'cpython',
            'memory management', 'garbage collection', 'design pattern'
        ]
        
        # Intermediate indicators
        intermediate_keywords = [
            'class', 'inheritance', 'exception', 'comprehension', 'lambda',
            'module', 'package', 'file handling', 'json', 'api', 'database',
            'testing', 'pytest', 'selenium', 'regex', 'recursion'
        ]
        
        # Beginner indicators
        beginner_keywords = [
            'what is', 'how to', 'basic', 'simple', 'beginner', 'start',
            'first', 'hello world', 'variable', 'print', 'input'
        ]
        
        # Count matches
        advanced_count = sum(1 for kw in advanced_keywords if kw in q_lower)
        intermediate_count = sum(1 for kw in intermediate_keywords if kw in q_lower)
        beginner_count = sum(1 for kw in beginner_keywords if kw in q_lower)
        
        # Determine skill level
        questions_count = profile.get("questions_count", 1)
        current_level = profile.get("skill_level", "unknown")
        
        if advanced_count >= 1:
            new_level = "advanced"
        elif intermediate_count >= 1:
            new_level = "intermediate"
        elif beginner_count >= 1:
            new_level = "beginner"
        else:
            new_level = current_level
        
        # Only update if we have enough data (avoid jumping around)
        if questions_count > 3 or current_level == "unknown":
            profile["skill_level"] = new_level
    
    def get_user_profile(self) -> Dict:
        """Get the user's profile."""
        return self.memory.get("user_profile", {})
    
    def get_skill_level(self) -> str:
        """Get the user's detected skill level."""
        return self.memory.get("user_profile", {}).get("skill_level", "unknown")
    
    def get_user_interests(self) -> List[str]:
        """Get topics the user is interested in."""
        return self.memory.get("user_profile", {}).get("interests", [])
    
    def should_give_detailed_response(self) -> bool:
        """Determine if user prefers detailed responses."""
        profile = self.memory.get("user_profile", {})
        skill = profile.get("skill_level", "unknown")
        pref = profile.get("response_preference", "detailed")
        
        # Beginners get detailed by default
        if skill == "beginner":
            return True
        # Advanced users might prefer concise
        if skill == "advanced" and pref != "detailed":
            return False
        return True
    
    def mark_topic_mastered(self, topic: str):
        """Mark a topic as mastered (user got it right multiple times)."""
        profile = self.memory.get("user_profile", {})
        mastered = profile.get("topics_mastered", [])
        if topic not in mastered:
            mastered.append(topic)
            profile["topics_mastered"] = mastered
            self.memory["user_profile"] = profile
            self._save()


# =============================================================================
# FEEDBACK LEARNER - Learn from user feedback
# =============================================================================

class FeedbackLearner:
    """
    Learn from user feedback (thumbs up/down) to improve responses.
    Stores good responses to reuse and bad responses to avoid.
    """
    
    def __init__(self, file_path: str = "feedback_data.json"):
        self.file_path = file_path
        self.data = self._load()
        self._ensure_structure()
    
    def _ensure_structure(self):
        """Ensure all required keys exist."""
        defaults = {
            "good_responses": {},  # topic -> [{"q": ..., "a": ..., "score": ...}]
            "bad_responses": {},   # topic -> [{"q": ..., "a": ...}]
            "corrections": [],     # [{"original_q": ..., "original_a": ..., "corrected_a": ..., "topic": ...}]
            "feedback_count": {"positive": 0, "negative": 0}
        }
        for key, value in defaults.items():
            if key not in self.data:
                self.data[key] = value
    
    def _load(self) -> Dict:
        """Load feedback data from JSON file."""
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
        return {}
    
    def _save(self):
        """Save feedback data to JSON file (atomic — safe if the same
        visitor has two tabs open writing concurrently)."""
        try:
            atomic_write_json(self.file_path, self.data)
        except (IOError, OSError):
            pass
    
    def record_feedback(self, topic: str, question: str, answer: str, 
                        is_helpful: bool, correction: str = None):
        """
        Record user feedback on a response.
        
        Args:
            topic: The topic of the question
            question: User's original question
            answer: Bot's response
            is_helpful: True for thumbs up, False for thumbs down
            correction: User's correction (optional, for thumbs down)
        """
        topic = topic or "general"
        
        if is_helpful:
            # Store as good response
            if topic not in self.data["good_responses"]:
                self.data["good_responses"][topic] = []
            
            # Check if this Q&A already exists and update score
            found = False
            for entry in self.data["good_responses"][topic]:
                if entry["q"] == question:
                    entry["score"] = entry.get("score", 1) + 1
                    found = True
                    break
            
            if not found:
                self.data["good_responses"][topic].append({
                    "q": question,
                    "a": answer[:500],  # Truncate
                    "score": 1,
                    "timestamp": datetime.now().isoformat()
                })
            
            self.data["feedback_count"]["positive"] += 1
        else:
            # Store as bad response
            if topic not in self.data["bad_responses"]:
                self.data["bad_responses"][topic] = []
            
            self.data["bad_responses"][topic].append({
                "q": question,
                "a": answer[:300],
                "timestamp": datetime.now().isoformat()
            })
            
            # Store correction if provided
            if correction:
                self.data["corrections"].append({
                    "original_q": question,
                    "original_a": answer[:300],
                    "corrected_a": correction,
                    "topic": topic,
                    "timestamp": datetime.now().isoformat()
                })
            
            self.data["feedback_count"]["negative"] += 1
        
        # Keep data manageable
        self._cleanup()
        self._save()
    
    def _cleanup(self):
        """Keep data size manageable."""
        # Limit good responses per topic
        for topic in self.data["good_responses"]:
            entries = self.data["good_responses"][topic]
            if len(entries) > 20:
                # Keep highest scored
                entries.sort(key=lambda x: x.get("score", 0), reverse=True)
                self.data["good_responses"][topic] = entries[:20]
        
        # Limit bad responses per topic
        for topic in self.data["bad_responses"]:
            if len(self.data["bad_responses"][topic]) > 10:
                self.data["bad_responses"][topic] = self.data["bad_responses"][topic][-10:]
        
        # Limit corrections
        if len(self.data["corrections"]) > 30:
            self.data["corrections"] = self.data["corrections"][-30:]
    
    def get_best_response(self, topic: str) -> Optional[Dict]:
        """
        Get the highest-rated response for a topic.
        
        Returns:
            Dict with 'q', 'a', 'score' or None if no good responses exist
        """
        if topic not in self.data.get("good_responses", {}):
            return None
        
        entries = self.data["good_responses"][topic]
        if not entries:
            return None
        
        # Return highest scored
        return max(entries, key=lambda x: x.get("score", 0))
    
    def get_corrections(self, topic: str = None) -> List[Dict]:
        """Get user-provided corrections, optionally filtered by topic."""
        corrections = self.data.get("corrections", [])
        if topic:
            return [c for c in corrections if c.get("topic") == topic]
        return corrections
    
    def should_avoid(self, answer_fragment: str, topic: str = None) -> bool:
        """
        Check if a response pattern has been rated poorly.
        
        Args:
            answer_fragment: Part of the answer to check
            topic: Optional topic to narrow search
            
        Returns:
            True if this pattern should be avoided
        """
        bad_responses = self.data.get("bad_responses", {})
        
        if topic and topic in bad_responses:
            for bad in bad_responses[topic]:
                if answer_fragment.lower() in bad.get("a", "").lower():
                    return True
        else:
            # Check all topics
            for topic_responses in bad_responses.values():
                for bad in topic_responses:
                    if answer_fragment.lower() in bad.get("a", "").lower():
                        return True
        
        return False
    
    def get_stats(self) -> Dict:
        """Get feedback statistics."""
        counts = self.data.get("feedback_count", {"positive": 0, "negative": 0})
        total = counts["positive"] + counts["negative"]
        
        return {
            "total_feedback": total,
            "positive": counts["positive"],
            "negative": counts["negative"],
            "satisfaction_rate": (counts["positive"] / total * 100) if total > 0 else 0,
            "corrections_count": len(self.data.get("corrections", [])),
            "topics_with_good_responses": len(self.data.get("good_responses", {}))
        }
    
    def find_similar_question(self, question: str, topic: str = None) -> Optional[Dict]:
        """
        Find a similar question that was rated positively.
        Uses advanced similarity matching.
        
        Returns:
            Best matching Q&A dict with confidence or None
        """
        good_responses = self.data.get("good_responses", {})
        topics_to_check = [topic] if topic else list(good_responses.keys())
        
        all_candidates = []
        for t in topics_to_check:
            if t in good_responses:
                for entry in good_responses[t]:
                    entry_copy = entry.copy()
                    entry_copy["_topic"] = t
                    all_candidates.append(entry_copy)
        
        if not all_candidates:
            return None
        
        # Use SmartMatcher with semantic search if available
        result = SmartMatcher.find_best_match(
            question, all_candidates, key="q", threshold=0.25,
            use_semantic=True  # Try semantic search for better matching
        )
        
        if result:
            match, score = result
            match["_similarity"] = score
            match["_confidence"] = ConfidenceScorer.calculate_confidence(
                source="learned_similar" if score < 0.8 else "learned_exact",
                similarity_score=score,
                feedback_score=match.get("score", 0)
            )
            return match
        return None
    
    def find_correction(self, question: str, topic: str = None) -> Optional[Dict]:
        """
        Find a user correction that matches the question.
        Corrections are the highest priority for responses.
        
        Returns:
            Matching correction dict with confidence or None
        """
        corrections = self.data.get("corrections", [])
        
        if topic:
            corrections = [c for c in corrections if c.get("topic") == topic]
        
        if not corrections:
            return None
        
        # Use SmartMatcher with semantic search for better correction matching
        result = SmartMatcher.find_best_match(
            question, corrections, key="original_q", threshold=0.30,
            use_semantic=True  # Semantic search helps find corrections better
        )
        
        if result:
            match, score = result
            return {
                "corrected_answer": match["corrected_a"],
                "original_question": match["original_q"],
                "topic": match.get("topic"),
                "similarity": score,
                "confidence": ConfidenceScorer.calculate_confidence(
                    source="correction",
                    similarity_score=score
                )
            }
        return None
    
    def get_learned_response(self, question: str, topic: str = None) -> Optional[Dict]:
        """
        Get the best learned response for a question.
        Priority: Corrections > Highly-rated similar > Best for topic
        
        Returns:
            Dict with 'answer', 'source', 'confidence' or None
        """
        # 1. First check corrections (highest priority)
        correction = self.find_correction(question, topic)
        if correction and correction["similarity"] >= 0.35:
            return {
                "answer": correction["corrected_answer"],
                "source": "correction",
                "confidence": correction["confidence"],
                "match_type": "user_correction"
            }
        
        # 2. Check for similar highly-rated questions
        similar = self.find_similar_question(question, topic)
        if similar:
            confidence = similar.get("_confidence", {})
            # Only use if score is good enough
            if similar.get("score", 0) >= 2 or similar.get("_similarity", 0) >= 0.6:
                return {
                    "answer": similar["a"],
                    "source": "learned",
                    "confidence": confidence,
                    "match_type": "similar_rated",
                    "original_question": similar["q"],
                    "rating_score": similar.get("score", 0)
                }
        
        # 3. Check for best response on topic (lower confidence)
        if topic:
            best = self.get_best_response(topic)
            if best and best.get("score", 0) >= 3:
                return {
                    "answer": best["a"],
                    "source": "learned",
                    "confidence": ConfidenceScorer.calculate_confidence(
                        source="learned_similar",
                        similarity_score=0.3,
                        feedback_score=best.get("score", 0)
                    ),
                    "match_type": "topic_best",
                    "rating_score": best.get("score", 0)
                }
        
        return None
    
    def increment_usage(self, question: str, topic: str = None):
        """Track that a learned response was used."""
        good_responses = self.data.get("good_responses", {})
        topics_to_check = [topic] if topic else list(good_responses.keys())
        
        for t in topics_to_check:
            if t in good_responses:
                for entry in good_responses[t]:
                    if SmartMatcher.calculate_similarity(question, entry["q"]) > 0.5:
                        entry["times_used"] = entry.get("times_used", 0) + 1
                        self._save()
                        return


# =============================================================================
# TOPIC DETECTION - Helper for categorizing questions
# =============================================================================

# Common topic patterns
TOPIC_PATTERNS = {
    "list": ["list", "lists", "array", "append", "extend", "pop", "slice"],
    "dictionary": ["dict", "dictionary", "dictionaries", "key", "keys", "values", "items"],
    "tuple": ["tuple", "tuples", "immutable"],
    "set": ["set", "sets", "union", "intersection", "difference"],
    "string": ["string", "strings", "str", "format", "split", "join", "strip"],
    "function": ["function", "functions", "def", "return", "parameter", "argument", "args", "kwargs"],
    "class": ["class", "classes", "object", "oop", "self", "init", "__init__"],
    "loop": ["loop", "loops", "for", "while", "iteration", "iterate"],
    "exception": ["exception", "exceptions", "try", "except", "error", "raise", "finally"],
    "decorator": ["decorator", "decorators", "@", "wrapper"],
    "generator": ["generator", "generators", "yield", "iteration"],
    "lambda": ["lambda", "anonymous", "inline function"],
    "comprehension": ["comprehension", "list comprehension", "dict comprehension"],
    "inheritance": ["inheritance", "inherit", "parent", "child", "super"],
    "module": ["module", "modules", "import", "package", "pip"],
    "file": ["file", "files", "open", "read", "write", "close"],
    "selenium": ["selenium", "webdriver", "browser", "element", "locator", "xpath", "css selector"],
    "robot_framework": ["robot", "robot framework", "keyword", "test case", "robotframework"],
    "pytest": ["pytest", "fixture", "fixtures", "test_", "assert"],
    "api": ["api", "rest", "request", "response", "endpoint", "http"],
    "database": ["database", "sql", "query", "table", "sqlite", "mysql", "postgres"],
    "async": ["async", "await", "asyncio", "coroutine", "concurrent"],
    "regex": ["regex", "regular expression", "pattern", "match", "search", "re."],
    "networking": ["network", "socket", "tcp", "udp", "ip", "port", "http"],
    "linux": ["linux", "bash", "shell", "command", "terminal", "chmod", "grep"]
}


def detect_topic(message: str) -> Optional[str]:
    """
    Detect the main topic from a user message.
    
    Args:
        message: User's question/message
        
    Returns:
        Topic string or None if no clear topic detected
    """
    msg_lower = message.lower()
    
    # Score each topic
    topic_scores = {}
    for topic, keywords in TOPIC_PATTERNS.items():
        score = sum(1 for kw in keywords if kw in msg_lower)
        if score > 0:
            topic_scores[topic] = score
    
    if not topic_scores:
        return None
    
    # Return highest scoring topic
    return max(topic_scores.items(), key=lambda x: x[1])[0]


# =============================================================================
# SINGLETON INSTANCES - Global access throughout the app
# =============================================================================

# Per-visitor instance caches. Streamlit Cloud runs one shared process for
# every visitor, so a single global instance here would mean every visitor
# reads/writes the same chat memory and feedback data. Keyed by visitor_id
# (see visitor_identity.py) instead, with a bounded size so a long-lived
# process doesn't slowly accumulate memory across many distinct anonymous
# visitors over time — a simple FIFO eviction (oldest-inserted key first),
# not strict LRU, which is enough to bound growth without extra bookkeeping.
_memory_instances: Dict[str, "ConversationMemory"] = {}
_feedback_instances: Dict[str, "FeedbackLearner"] = {}
_MAX_CACHED_VISITORS = 200


def _evict_oldest_if_over_capacity(cache: Dict) -> None:
    if len(cache) > _MAX_CACHED_VISITORS:
        oldest_key = next(iter(cache))
        cache.pop(oldest_key, None)


def get_memory(visitor_id: str) -> ConversationMemory:
    """Get this visitor's ConversationMemory instance, creating it (backed
    by their own chat_memory.json under data/visitors/<visitor_id>/) if
    this is the first call for that visitor in this process."""
    if visitor_id not in _memory_instances:
        path = get_visitor_dir(visitor_id) / "chat_memory.json"
        _memory_instances[visitor_id] = ConversationMemory(file_path=str(path))
        _evict_oldest_if_over_capacity(_memory_instances)
    return _memory_instances[visitor_id]


def get_feedback_learner(visitor_id: str) -> FeedbackLearner:
    """Get this visitor's FeedbackLearner instance, creating it (backed by
    their own feedback_data.json under data/visitors/<visitor_id>/) if this
    is the first call for that visitor in this process."""
    if visitor_id not in _feedback_instances:
        path = get_visitor_dir(visitor_id) / "feedback_data.json"
        _feedback_instances[visitor_id] = FeedbackLearner(file_path=str(path))
        _evict_oldest_if_over_capacity(_feedback_instances)
    return _feedback_instances[visitor_id]


# =============================================================================
# CONVENIENCE FUNCTIONS - Easy integration
# =============================================================================

def store_interaction(visitor_id: str, question: str, answer: str, rating: int = None):
    """
    Store a Q&A interaction (convenience wrapper).

    Args:
        visitor_id: Anonymous per-visitor id (see visitor_identity.py) —
            selects whose chat memory this gets stored in
        question: User's question
        answer: Bot's response
        rating: Optional rating (1-5)
    """
    topic = detect_topic(question)
    memory = get_memory(visitor_id)
    memory.store_qa(question, answer, topic, rating)


def record_user_feedback(visitor_id: str, question: str, answer: str, is_positive: bool, correction: str = None):
    """
    Record user feedback (convenience wrapper).

    Args:
        visitor_id: Anonymous per-visitor id
        question: Original question
        answer: Bot's response
        is_positive: True for thumbs up, False for thumbs down
        correction: User's correction text (optional)
    """
    topic = detect_topic(question)
    learner = get_feedback_learner(visitor_id)
    learner.record_feedback(topic, question, answer, is_positive, correction)


def get_learning_context(visitor_id: str, query: str) -> Dict:
    """
    Get all learning-related context for a query.

    Returns dict with:
        - relevant_qa: Past similar Q&A pairs
        - best_rated: Highest rated response for topic
        - corrections: Any user corrections for topic
        - topic: Detected topic
        - learned_response: Best learned response to use
        - user_profile: User's profile info
    """
    topic = detect_topic(query)
    memory = get_memory(visitor_id)
    learner = get_feedback_learner(visitor_id)

    # Get the best learned response (corrections > rated > topic best)
    learned_response = learner.get_learned_response(query, topic)

    return {
        "topic": topic,
        "relevant_qa": memory.get_relevant_context(query, limit=2),
        "best_rated": learner.get_best_response(topic) if topic else None,
        "similar_good": learner.find_similar_question(query, topic),
        "corrections": learner.get_corrections(topic) if topic else [],
        "learned_response": learned_response,
        "user_profile": memory.get_user_profile(),
        "skill_level": memory.get_skill_level()
    }


def get_combined_stats(visitor_id: str) -> Dict:
    """Get combined statistics from memory and feedback for this visitor."""
    memory = get_memory(visitor_id)
    learner = get_feedback_learner(visitor_id)

    mem_stats = memory.get_stats()
    fb_stats = learner.get_stats()

    return {
        "memory": mem_stats,
        "feedback": fb_stats,
        "total_interactions": mem_stats["total_qa"],
        "learning_score": fb_stats["satisfaction_rate"],
        "user_profile": mem_stats.get("user_profile", {}),
        "corrections_available": fb_stats.get("corrections_count", 0)
    }


def get_smart_response(visitor_id: str, query: str) -> Optional[Dict]:
    """
    Main entry point: Get the smartest response for a query, from this
    visitor's own learned corrections/ratings.

    Checks in order:
    1. User corrections (highest priority)
    2. Highly-rated similar responses
    3. Best response for topic

    Returns:
        Dict with 'answer', 'confidence', 'source' or None if nothing found
    """
    topic = detect_topic(query)
    learner = get_feedback_learner(visitor_id)
    memory = get_memory(visitor_id)

    # Get learned response
    learned = learner.get_learned_response(query, topic)

    if learned:
        # Track usage
        learner.increment_usage(query, topic)

        # Update user profile
        memory.update_user_profile(query, topic)

        return learned

    return None


def update_learning_from_feedback(visitor_id: str, question: str, answer: str,
                                   is_positive: bool, correction: str = None):
    """
    Update learning based on user feedback.
    This is the main function to call after user gives feedback.
    """
    topic = detect_topic(question)
    memory = get_memory(visitor_id)
    learner = get_feedback_learner(visitor_id)

    # Record the feedback
    learner.record_feedback(topic, question, answer, is_positive, correction)

    # Update user profile
    memory.update_user_profile(question, topic, was_helpful=is_positive)

    # If positive and topic detected, check if mastered
    if is_positive and topic:
        # Count positive feedbacks for this topic
        good_responses = learner.data.get("good_responses", {}).get(topic, [])
        total_score = sum(r.get("score", 0) for r in good_responses)
        if total_score >= 5:
            memory.mark_topic_mastered(topic)

