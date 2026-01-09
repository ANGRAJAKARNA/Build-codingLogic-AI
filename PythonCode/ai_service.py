# ai_service.py
"""
AI Service module for Groq API integration.
Handles all AI-powered features including code review, hints, chat, and more.
"""

import os
import time
import hashlib
from typing import Optional, List, Dict, Any
from functools import lru_cache
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from .env file
load_dotenv()

# Initialize Groq client
# Set GROQ_API_KEY environment variable before running
_client = None

# Simple response cache (in-memory)
_response_cache: Dict[str, tuple] = {}  # key -> (response, timestamp)
CACHE_TTL = 300  # Cache responses for 5 minutes

# Rate limiting
_last_request_time = 0
MIN_REQUEST_INTERVAL = 0.5  # Minimum 500ms between requests

def get_client() -> Groq:
    """Get or create Groq client."""
    global _client
    if _client is None:
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            raise ValueError(
                "GROQ_API_KEY environment variable not set. "
                "Get your free API key at https://console.groq.com"
            )
        _client = Groq(api_key=api_key)
    return _client


def is_ai_available() -> bool:
    """Check if AI service is available."""
    return os.environ.get("GROQ_API_KEY") is not None


# Model configuration
DEFAULT_MODEL = "llama-3.1-70b-versatile"
FAST_MODEL = "llama-3.1-8b-instant"


def _get_cache_key(prompt: str, system_prompt: str, model: str) -> str:
    """Generate a cache key for a request."""
    content = f"{prompt}|{system_prompt or ''}|{model}"
    return hashlib.md5(content.encode()).hexdigest()


def _rate_limit():
    """Enforce rate limiting between requests."""
    global _last_request_time
    elapsed = time.time() - _last_request_time
    if elapsed < MIN_REQUEST_INTERVAL:
        time.sleep(MIN_REQUEST_INTERVAL - elapsed)
    _last_request_time = time.time()


def get_ai_response(
    prompt: str,
    system_prompt: str = None,
    model: str = DEFAULT_MODEL,
    temperature: float = 0.7,
    max_tokens: int = 1024,
    conversation_history: List[Dict] = None,
    use_cache: bool = True,
    max_retries: int = 3
) -> str:
    """
    Get AI response from Groq with retry logic and caching.
    
    Args:
        prompt: User message/prompt
        system_prompt: System instructions for the AI
        model: Model to use (default: llama-3.1-70b-versatile)
        temperature: Creativity level (0-1)
        max_tokens: Maximum response length
        conversation_history: Previous messages for context
        use_cache: Whether to use response caching
        max_retries: Maximum number of retry attempts
    
    Returns:
        AI response text
    """
    # Check cache first (only for requests without conversation history)
    cache_key = None
    if use_cache and not conversation_history:
        cache_key = _get_cache_key(prompt, system_prompt, model)
        if cache_key in _response_cache:
            cached_response, cached_time = _response_cache[cache_key]
            if time.time() - cached_time < CACHE_TTL:
                return cached_response
    
    # Apply rate limiting
    _rate_limit()
    
    last_error = None
    for attempt in range(max_retries):
        try:
            client = get_client()
            
            messages = []
            
            # Add system prompt if provided
            if system_prompt:
                messages.append({
                    "role": "system",
                    "content": system_prompt
                })
            
            # Add conversation history if provided
            if conversation_history:
                messages.extend(conversation_history)
            
            # Add current prompt
            messages.append({
                "role": "user",
                "content": prompt
            })
            
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            result = response.choices[0].message.content
            
            # Cache the response
            if cache_key:
                _response_cache[cache_key] = (result, time.time())
                # Clean old cache entries
                _clean_cache()
            
            return result
        
        except Exception as e:
            last_error = e
            if attempt < max_retries - 1:
                # Exponential backoff
                time.sleep(2 ** attempt)
                continue
    
    return f"AI Error: {str(last_error)}"


def _clean_cache():
    """Remove expired cache entries."""
    global _response_cache
    current_time = time.time()
    expired_keys = [
        key for key, (_, timestamp) in _response_cache.items()
        if current_time - timestamp > CACHE_TTL
    ]
    for key in expired_keys:
        del _response_cache[key]


def get_code_review(
    code: str,
    problem: str,
    function_name: str,
    time_taken: float = None
) -> str:
    """
    Get AI code review for submitted solution.
    
    Args:
        code: User's submitted code
        problem: Problem description
        function_name: Expected function name
        time_taken: Time taken to solve (optional)
    
    Returns:
        Code review feedback
    """
    from prompts import CODE_REVIEW_PROMPT
    
    prompt = CODE_REVIEW_PROMPT.format(
        problem=problem,
        function_name=function_name,
        code=code,
        time_taken=f"{time_taken:.1f} seconds" if time_taken else "N/A"
    )
    
    return get_ai_response(prompt, temperature=0.5, max_tokens=512)


def get_bug_detection(
    code: str,
    problem: str,
    function_name: str,
    error_message: str,
    test_input: Any = None,
    expected: Any = None,
    actual: Any = None
) -> str:
    """
    Get AI bug detection and fix suggestions.
    
    Args:
        code: User's code
        problem: Problem description
        function_name: Expected function name
        error_message: Error or failure message
        test_input: Input that caused failure
        expected: Expected output
        actual: Actual output
    
    Returns:
        Bug analysis and suggestions
    """
    from prompts import BUG_DETECTION_PROMPT
    
    prompt = BUG_DETECTION_PROMPT.format(
        problem=problem,
        function_name=function_name,
        code=code,
        error_message=error_message,
        test_input=test_input,
        expected=expected,
        actual=actual
    )
    
    return get_ai_response(prompt, temperature=0.3, max_tokens=512)


def get_smart_hint(
    code: str,
    problem: str,
    function_name: str,
    static_hints: List[str],
    hint_number: int
) -> str:
    """
    Get personalized hint based on user's current code.
    
    Args:
        code: User's current code attempt
        problem: Problem description
        function_name: Expected function name
        static_hints: Original static hints
        hint_number: Which hint number (1, 2, 3...)
    
    Returns:
        Personalized hint
    """
    from prompts import SMART_HINT_PROMPT
    
    prompt = SMART_HINT_PROMPT.format(
        problem=problem,
        function_name=function_name,
        code=code,
        static_hints="\n".join(f"- {h}" for h in static_hints),
        hint_number=hint_number
    )
    
    return get_ai_response(prompt, temperature=0.6, max_tokens=256)


def get_tutor_response(
    message: str,
    problem: str,
    function_name: str,
    user_code: str,
    conversation_history: List[Dict],
    interview_mode: bool = False
) -> str:
    """
    Get AI tutor chat response.
    
    Args:
        message: User's message
        problem: Current problem description
        function_name: Expected function name
        user_code: User's current code
        conversation_history: Previous chat messages
        interview_mode: Whether in interview prep mode
    
    Returns:
        Tutor response
    """
    from prompts import TUTOR_SYSTEM_PROMPT, INTERVIEW_SYSTEM_PROMPT
    
    system = INTERVIEW_SYSTEM_PROMPT if interview_mode else TUTOR_SYSTEM_PROMPT
    system = system.format(
        problem=problem,
        function_name=function_name,
        user_code=user_code
    )
    
    return get_ai_response(
        message,
        system_prompt=system,
        conversation_history=conversation_history,
        temperature=0.7,
        max_tokens=512
    )


def get_code_explanation(
    code: str,
    problem: str,
    function_name: str
) -> str:
    """
    Get detailed explanation of solution code.
    
    Args:
        code: Solution code to explain
        problem: Problem description
        function_name: Function name
    
    Returns:
        Detailed explanation
    """
    from prompts import EXPLANATION_PROMPT
    
    prompt = EXPLANATION_PROMPT.format(
        problem=problem,
        function_name=function_name,
        code=code
    )
    
    return get_ai_response(prompt, temperature=0.5, max_tokens=768)


def get_recommendations(
    completed_questions: List[Dict],
    skipped_questions: List[Dict],
    performance_data: Dict,
    available_questions: List[Dict]
) -> List[Dict]:
    """
    Get smart problem recommendations.
    
    Args:
        completed_questions: Questions user has solved
        skipped_questions: Questions user has skipped
        performance_data: User's performance metrics
        available_questions: All available questions
    
    Returns:
        List of recommended questions with reasons
    """
    from prompts import RECOMMENDATION_PROMPT
    
    # Build context
    completed_summary = []
    for q in completed_questions[-10:]:  # Last 10
        completed_summary.append(f"- {q['question']} (tags: {', '.join(q.get('tags', []))})")
    
    skipped_summary = []
    for q in skipped_questions[-5:]:  # Last 5
        skipped_summary.append(f"- {q['question']} (tags: {', '.join(q.get('tags', []))})")
    
    available_summary = []
    for q in available_questions[:20]:  # First 20 unsolved
        available_summary.append(f"- {q['question']} (tags: {', '.join(q.get('tags', []))})")
    
    prompt = RECOMMENDATION_PROMPT.format(
        completed="\n".join(completed_summary) or "None yet",
        skipped="\n".join(skipped_summary) or "None",
        weak_topics=", ".join(performance_data.get('weak_topics', [])) or "None identified",
        average_time=performance_data.get('average_time', 'N/A'),
        available="\n".join(available_summary)
    )
    
    response = get_ai_response(prompt, temperature=0.5, max_tokens=512)
    
    # Parse recommendations (simple approach)
    recommendations = []
    lines = response.split('\n')
    for line in lines:
        line = line.strip()
        if line and not line.startswith('#'):
            # Try to match question names from available
            for q in available_questions:
                if q['question'].lower() in line.lower():
                    recommendations.append({
                        'question': q,
                        'reason': line
                    })
                    break
        if len(recommendations) >= 3:
            break
    
    return recommendations


def get_code_suggestion(
    partial_code: str,
    problem: str,
    function_name: str
) -> str:
    """
    Get code completion suggestion.
    
    Args:
        partial_code: User's partial code
        problem: Problem description
        function_name: Expected function name
    
    Returns:
        Code suggestion (just the completion part)
    """
    from prompts import CODE_SUGGESTION_PROMPT
    
    prompt = CODE_SUGGESTION_PROMPT.format(
        problem=problem,
        function_name=function_name,
        partial_code=partial_code
    )
    
    return get_ai_response(
        prompt,
        model=FAST_MODEL,  # Use faster model for suggestions
        temperature=0.3,
        max_tokens=128
    )


def analyze_performance(
    progress_data: Dict,
    questions_data: Dict
) -> Dict:
    """
    Analyze user performance for difficulty calibration.
    
    Args:
        progress_data: User's progress from persistence
        questions_data: All questions data
    
    Returns:
        Performance analysis with weak topics, skill level, etc.
    """
    analysis = {
        'total_solved': 0,
        'total_skipped': 0,
        'average_time': None,
        'weak_topics': [],
        'strong_topics': [],
        'skill_level': 'beginner',
        'recommended_difficulty': 'Basic'
    }
    
    topic_stats = {}  # tag -> {solved: 0, skipped: 0, total_time: 0}
    all_times = []
    
    for stage, data in progress_data.items():
        completed = data.get('completed', set())
        skipped = data.get('skipped', set())
        times = data.get('times', {})
        
        analysis['total_solved'] += len(completed)
        analysis['total_skipped'] += len(skipped)
        
        questions = questions_data.get(stage, [])
        
        for q_idx in completed:
            if q_idx < len(questions):
                q = questions[q_idx]
                for tag in q.get('tags', []):
                    if tag not in topic_stats:
                        topic_stats[tag] = {'solved': 0, 'skipped': 0}
                    topic_stats[tag]['solved'] += 1
                
                time_key = str(q_idx)
                if time_key in times:
                    all_times.append(times[time_key])
        
        for q_idx in skipped:
            if q_idx < len(questions):
                q = questions[q_idx]
                for tag in q.get('tags', []):
                    if tag not in topic_stats:
                        topic_stats[tag] = {'solved': 0, 'skipped': 0}
                    topic_stats[tag]['skipped'] += 1
    
    # Calculate average time
    if all_times:
        analysis['average_time'] = sum(all_times) / len(all_times)
    
    # Identify weak and strong topics
    for tag, stats in topic_stats.items():
        total = stats['solved'] + stats['skipped']
        if total >= 2:  # Need at least 2 attempts
            success_rate = stats['solved'] / total
            if success_rate < 0.5:
                analysis['weak_topics'].append(tag)
            elif success_rate >= 0.8:
                analysis['strong_topics'].append(tag)
    
    # Determine skill level
    total_solved = analysis['total_solved']
    if total_solved >= 50:
        analysis['skill_level'] = 'advanced'
        analysis['recommended_difficulty'] = 'Advanced'
    elif total_solved >= 20:
        analysis['skill_level'] = 'intermediate'
        analysis['recommended_difficulty'] = 'Intermediate'
    else:
        analysis['skill_level'] = 'beginner'
        analysis['recommended_difficulty'] = 'Basic'
    
    return analysis