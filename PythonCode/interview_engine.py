# interview_engine.py
"""
Interview Engine Module for PyCode.
Manages interview state, stages, scoring, and context-aware question generation.
Supports both text-only and voice-enabled interview modes.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import random
import re

# Voice engine imports (optional - graceful fallback if not available)
VOICE_AVAILABLE = False
try:
    from voice_engine import (
        VoiceConfig, VoiceMode, VoiceInterviewer, 
        VOICE_SCRIPTS, get_voice_capabilities, TTSEngine
    )
    VOICE_AVAILABLE = True
except ImportError:
    # Voice features not available
    pass


class InterviewStage(Enum):
    """Stages of a mock interview."""
    GREETING = "greeting"           # Voice mode: Initial greeting
    SELF_INTRO = "self_intro"       # Voice mode: User self-introduction
    INTRO = "intro"                 # Problem introduction
    APPROACH = "approach"           # Solution approach discussion
    CODING = "coding"               # Implementation phase
    OPTIMIZATION = "optimization"   # Complexity analysis
    BEHAVIORAL = "behavioral"       # Behavioral questions
    WRAPUP = "wrapup"              # Final questions
    COMPLETED = "completed"         # Interview finished


class InterviewDifficulty(Enum):
    """Interview difficulty levels."""
    JUNIOR = "junior"
    MID = "mid"
    SENIOR = "senior"


class InterviewType(Enum):
    """Types of interview focus."""
    TECHNICAL = "technical"
    BEHAVIORAL = "behavioral"
    MIXED = "mixed"


@dataclass
class InterviewScores:
    """Tracks scores across different categories."""
    problem_solving: float = 0.0
    communication: float = 0.0
    code_quality: float = 0.0
    complexity_analysis: float = 0.0
    
    # Track what has been evaluated
    evaluated_aspects: Dict[str, bool] = field(default_factory=lambda: {
        "explained_approach": False,
        "mentioned_edge_cases": False,
        "discussed_complexity": False,
        "asked_clarifying_questions": False,
        "wrote_working_code": False,
        "optimized_solution": False,
    })
    
    def get_total(self) -> float:
        """Calculate total score out of 100."""
        weights = {
            "problem_solving": 0.35,
            "communication": 0.25,
            "code_quality": 0.25,
            "complexity_analysis": 0.15,
        }
        total = (
            self.problem_solving * weights["problem_solving"] +
            self.communication * weights["communication"] +
            self.code_quality * weights["code_quality"] +
            self.complexity_analysis * weights["complexity_analysis"]
        )
        return min(100, total)
    
    def get_grade(self) -> str:
        """Get letter grade based on total score."""
        total = self.get_total()
        if total >= 90:
            return "A"
        elif total >= 80:
            return "B"
        elif total >= 70:
            return "C"
        elif total >= 60:
            return "D"
        return "F"
    
    def get_hiring_recommendation(self) -> str:
        """Get hiring recommendation based on performance."""
        total = self.get_total()
        if total >= 85:
            return "Strong Hire"
        elif total >= 70:
            return "Hire"
        elif total >= 55:
            return "Lean Hire"
        elif total >= 40:
            return "Lean No Hire"
        return "No Hire"


@dataclass
class InterviewConfig:
    """Configuration for an interview session."""
    difficulty: InterviewDifficulty = InterviewDifficulty.MID
    interview_type: InterviewType = InterviewType.TECHNICAL
    time_limit_minutes: int = 30
    show_live_score: bool = False
    include_behavioral: bool = True
    
    # Voice mode settings
    voice_enabled: bool = False
    voice_config: Any = None  # VoiceConfig when voice is enabled
    self_intro_duration: int = 30  # seconds for self-introduction
    greeting_pause: float = 3.0    # seconds to pause after greeting
    
    def get_stage_time_allocation(self) -> Dict[InterviewStage, int]:
        """Get recommended time in minutes for each stage."""
        total = self.time_limit_minutes
        if self.interview_type == InterviewType.BEHAVIORAL:
            return {
                InterviewStage.INTRO: 2,
                InterviewStage.BEHAVIORAL: total - 4,
                InterviewStage.WRAPUP: 2,
            }
        elif self.interview_type == InterviewType.MIXED:
            return {
                InterviewStage.INTRO: 2,
                InterviewStage.APPROACH: int(total * 0.15),
                InterviewStage.CODING: int(total * 0.35),
                InterviewStage.OPTIMIZATION: int(total * 0.15),
                InterviewStage.BEHAVIORAL: int(total * 0.25),
                InterviewStage.WRAPUP: 2,
            }
        else:  # TECHNICAL
            return {
                InterviewStage.INTRO: 2,
                InterviewStage.APPROACH: int(total * 0.2),
                InterviewStage.CODING: int(total * 0.45),
                InterviewStage.OPTIMIZATION: int(total * 0.25),
                InterviewStage.WRAPUP: 2,
            }


@dataclass
class InterviewState:
    """Tracks the current state of an interview session."""
    config: InterviewConfig = field(default_factory=InterviewConfig)
    current_stage: InterviewStage = InterviewStage.INTRO
    scores: InterviewScores = field(default_factory=InterviewScores)
    
    # Timing
    start_time: Optional[datetime] = None
    stage_start_time: Optional[datetime] = None
    
    # Conversation tracking
    conversation_history: List[Dict[str, str]] = field(default_factory=list)
    stage_history: Dict[InterviewStage, List[Dict[str, str]]] = field(default_factory=dict)
    
    # What has been asked/discussed
    asked_questions: List[str] = field(default_factory=list)
    topics_covered: List[str] = field(default_factory=list)
    
    # User's responses tracking
    user_mentioned_complexity: bool = False
    user_mentioned_edge_cases: bool = False
    user_asked_clarifying: bool = False
    user_explained_approach: bool = False
    code_attempts: int = 0
    
    # Problem context
    problem_name: str = ""
    function_name: str = ""
    
    # Voice mode state
    voice_enabled: bool = False
    self_introduction: str = ""
    greeting_completed: bool = False
    self_intro_completed: bool = False
    current_voice_prompt: str = ""
    detected_experience_level: str = ""  # Detected from self-intro
    detected_expertise_areas: List[str] = field(default_factory=list)
    
    def start_interview(self, problem: str, function: str):
        """Initialize a new interview session."""
        self.start_time = datetime.now()
        self.stage_start_time = datetime.now()
        
        # Set initial stage based on voice mode
        if self.config.voice_enabled:
            self.current_stage = InterviewStage.GREETING
            self.voice_enabled = True
        else:
            self.current_stage = InterviewStage.INTRO
            self.voice_enabled = False
        
        self.problem_name = problem
        self.function_name = function
        self.conversation_history = []
        self.stage_history = {stage: [] for stage in InterviewStage}
        self.asked_questions = []
        self.topics_covered = []
        self.scores = InterviewScores()
        
        # Reset voice state
        self.self_introduction = ""
        self.greeting_completed = False
        self.self_intro_completed = False
        self.current_voice_prompt = ""
        self.detected_experience_level = ""
        self.detected_expertise_areas = []
        
    def advance_stage(self) -> InterviewStage:
        """Move to the next interview stage."""
        # Build stage order based on mode
        if self.voice_enabled:
            # Voice mode includes greeting and self-intro stages
            stage_order = [
                InterviewStage.GREETING,
                InterviewStage.SELF_INTRO,
                InterviewStage.INTRO,
                InterviewStage.APPROACH,
                InterviewStage.CODING,
                InterviewStage.OPTIMIZATION,
                InterviewStage.BEHAVIORAL,
                InterviewStage.WRAPUP,
                InterviewStage.COMPLETED,
            ]
        else:
            # Text-only mode
            stage_order = [
                InterviewStage.INTRO,
                InterviewStage.APPROACH,
                InterviewStage.CODING,
                InterviewStage.OPTIMIZATION,
                InterviewStage.BEHAVIORAL,
                InterviewStage.WRAPUP,
                InterviewStage.COMPLETED,
            ]
        
        # Skip behavioral if not included
        if not self.config.include_behavioral:
            if InterviewStage.BEHAVIORAL in stage_order:
                stage_order.remove(InterviewStage.BEHAVIORAL)
        
        # Skip behavioral for pure technical
        if self.config.interview_type == InterviewType.TECHNICAL:
            if InterviewStage.BEHAVIORAL in stage_order:
                stage_order.remove(InterviewStage.BEHAVIORAL)
        
        # Find current position and advance
        try:
            current_idx = stage_order.index(self.current_stage)
            if current_idx < len(stage_order) - 1:
                self.current_stage = stage_order[current_idx + 1]
                self.stage_start_time = datetime.now()
        except ValueError:
            # Current stage not in order, go to INTRO or first stage
            self.current_stage = stage_order[0]
            self.stage_start_time = datetime.now()
        
        return self.current_stage
    
    def get_elapsed_time(self) -> int:
        """Get elapsed time in seconds."""
        if self.start_time is None:
            return 0
        return int((datetime.now() - self.start_time).total_seconds())
    
    def get_remaining_time(self) -> int:
        """Get remaining time in seconds."""
        elapsed = self.get_elapsed_time()
        total = self.config.time_limit_minutes * 60
        return max(0, total - elapsed)
    
    def is_time_up(self) -> bool:
        """Check if interview time has expired."""
        return self.get_remaining_time() <= 0
    
    def add_message(self, role: str, content: str):
        """Add a message to conversation history."""
        msg = {"role": role, "content": content, "stage": self.current_stage.value}
        self.conversation_history.append(msg)
        
        if self.current_stage not in self.stage_history:
            self.stage_history[self.current_stage] = []
        self.stage_history[self.current_stage].append(msg)


class InterviewEngine:
    """Main engine for conducting mock interviews."""
    
    def __init__(self, state: Optional[InterviewState] = None):
        self.state = state or InterviewState()
        self.voice_interviewer = None  # VoiceInterviewer instance when voice mode enabled
    
    # =========================================================================
    # VOICE MODE METHODS
    # =========================================================================
    
    def enable_voice_mode(self, voice_config: Any = None) -> bool:
        """
        Enable voice mode for the interview.
        
        Args:
            voice_config: VoiceConfig instance (optional)
            
        Returns:
            True if voice mode enabled successfully, False if not available
        """
        if not VOICE_AVAILABLE:
            return False
        
        try:
            # Create voice interviewer
            from voice_engine import VoiceInterviewer, VoiceConfig, VoiceMode
            
            if voice_config is None:
                voice_config = VoiceConfig(mode=VoiceMode.VOICE_ENABLED)
            
            self.voice_interviewer = VoiceInterviewer(voice_config)
            self.state.config.voice_enabled = True
            self.state.config.voice_config = voice_config
            self.state.voice_enabled = True
            
            return True
        except Exception as e:
            print(f"Failed to enable voice mode: {e}")
            return False
    
    def is_voice_enabled(self) -> bool:
        """Check if voice mode is enabled."""
        return self.state.voice_enabled and self.voice_interviewer is not None
    
    def get_voice_prompt(self, stage: InterviewStage = None) -> Tuple[str, Optional[bytes]]:
        """
        Get the voice prompt (text and audio) for a stage.
        
        Args:
            stage: Interview stage (uses current stage if None)
            
        Returns:
            Tuple of (prompt_text, audio_bytes or None)
        """
        if stage is None:
            stage = self.state.current_stage
        
        # Get the text prompt for the stage
        text = self._get_stage_voice_text(stage)
        self.state.current_voice_prompt = text
        
        # Generate audio if voice mode is enabled
        audio = None
        if self.is_voice_enabled() and self.voice_interviewer:
            audio = self.voice_interviewer.speak(text, cache_key=stage.value)
        
        return text, audio
    
    def _get_stage_voice_text(self, stage: InterviewStage) -> str:
        """Get the voice text for a specific stage."""
        if VOICE_AVAILABLE:
            try:
                from voice_engine import VOICE_SCRIPTS
                
                stage_scripts = {
                    InterviewStage.GREETING: VOICE_SCRIPTS.get("greeting", "Hi, please settle down for the interview."),
                    InterviewStage.SELF_INTRO: VOICE_SCRIPTS.get("intro_request", "Please introduce yourself. You have about 30 seconds."),
                    InterviewStage.INTRO: f"Here is your problem: {self.state.problem_name}",
                    InterviewStage.APPROACH: VOICE_SCRIPTS.get("approach_request", "Please explain your approach to solving this problem."),
                    InterviewStage.CODING: VOICE_SCRIPTS.get("coding_start", "Go ahead and implement your solution."),
                    InterviewStage.OPTIMIZATION: VOICE_SCRIPTS.get("optimization_request", "What's the time and space complexity of your solution?"),
                    InterviewStage.BEHAVIORAL: VOICE_SCRIPTS.get("behavioral_intro", "Let's discuss some behavioral questions."),
                    InterviewStage.WRAPUP: VOICE_SCRIPTS.get("wrapup", "We're coming to the end. Do you have any questions for me?"),
                    InterviewStage.COMPLETED: VOICE_SCRIPTS.get("goodbye", "Thank you for your time today."),
                }
                return stage_scripts.get(stage, "")
            except ImportError:
                pass
        
        # Fallback text prompts
        fallback_scripts = {
            InterviewStage.GREETING: "Hi, please settle down for the interview.",
            InterviewStage.SELF_INTRO: "Please introduce yourself. You have about 30 seconds.",
            InterviewStage.INTRO: f"Here is your problem: {self.state.problem_name}",
            InterviewStage.APPROACH: "Please explain your approach to solving this problem.",
            InterviewStage.CODING: "Go ahead and implement your solution.",
            InterviewStage.OPTIMIZATION: "What's the time and space complexity of your solution?",
            InterviewStage.BEHAVIORAL: "Let's discuss some behavioral questions.",
            InterviewStage.WRAPUP: "We're coming to the end. Do you have any questions for me?",
            InterviewStage.COMPLETED: "Thank you for your time today.",
        }
        return fallback_scripts.get(stage, "")
    
    def process_self_introduction(self, intro_text: str) -> str:
        """
        Process the user's self-introduction.
        
        Args:
            intro_text: Transcribed text of user's self-introduction
            
        Returns:
            Response message to show user
        """
        self.state.self_introduction = intro_text
        self.state.self_intro_completed = True
        
        # Analyze the introduction
        self._analyze_self_introduction(intro_text)
        
        # Add to conversation history
        self.state.add_message("user", f"[Self Introduction] {intro_text}")
        
        # Generate response
        if VOICE_AVAILABLE:
            try:
                from voice_engine import VOICE_SCRIPTS
                response = VOICE_SCRIPTS.get("intro_followup", "Thank you for that introduction.")
            except ImportError:
                response = "Thank you for that introduction."
        else:
            response = "Thank you for that introduction."
        
        self.state.add_message("assistant", response)
        
        # Award communication points for self-intro
        self.state.scores.communication = min(100, self.state.scores.communication + 10)
        
        return response
    
    def _analyze_self_introduction(self, intro: str):
        """
        Analyze self-introduction to personalize the interview.
        Detects experience level and areas of expertise.
        """
        intro_lower = intro.lower()
        
        # Detect experience level
        senior_keywords = ['senior', 'lead', 'architect', 'principal', 'staff', 
                          '10 years', '8 years', '7 years', 'decade', 'manager']
        junior_keywords = ['junior', 'intern', 'graduate', 'student', 'learning',
                          'entry', 'fresher', 'new grad', 'bootcamp', '1 year']
        
        if any(kw in intro_lower for kw in senior_keywords):
            self.state.detected_experience_level = "senior"
            # Consider upgrading difficulty for senior candidates
            if self.state.config.difficulty == InterviewDifficulty.MID:
                self.state.config.difficulty = InterviewDifficulty.SENIOR
        elif any(kw in intro_lower for kw in junior_keywords):
            self.state.detected_experience_level = "junior"
            # Consider downgrading difficulty for junior candidates
            if self.state.config.difficulty == InterviewDifficulty.MID:
                self.state.config.difficulty = InterviewDifficulty.JUNIOR
        else:
            self.state.detected_experience_level = "mid"
        
        # Detect areas of expertise for tailored follow-up questions
        expertise_mapping = {
            'web': ['web', 'frontend', 'backend', 'api', 'rest', 'react', 'angular', 'vue', 'django', 'flask'],
            'data': ['data', 'analytics', 'machine learning', 'ml', 'ai', 'pandas', 'numpy', 'tensorflow'],
            'automation': ['automation', 'testing', 'qa', 'selenium', 'robot', 'pytest', 'test'],
            'devops': ['devops', 'cloud', 'aws', 'azure', 'kubernetes', 'docker', 'ci/cd', 'jenkins'],
            'mobile': ['mobile', 'android', 'ios', 'flutter', 'react native', 'swift', 'kotlin'],
            'systems': ['systems', 'linux', 'networking', 'infrastructure', 'sre', 'reliability'],
        }
        
        detected_areas = []
        for area, keywords in expertise_mapping.items():
            if any(kw in intro_lower for kw in keywords):
                detected_areas.append(area)
        
        self.state.detected_expertise_areas = detected_areas
        
        # Add detected areas to topics for context
        self.state.topics_covered.extend(detected_areas)
    
    def complete_greeting(self):
        """Mark the greeting stage as completed."""
        self.state.greeting_completed = True
    
    def get_voice_feedback(self, response_text: str) -> Optional[bytes]:
        """
        Generate voice audio for an interview response.
        
        Args:
            response_text: Text to convert to speech
            
        Returns:
            Audio bytes or None if voice not enabled
        """
        if not self.is_voice_enabled() or not self.voice_interviewer:
            return None
        
        return self.voice_interviewer.speak(response_text)
    
    # =========================================================================
    # STANDARD INTERVIEW METHODS
    # =========================================================================
    
    def start_new_interview(
        self,
        problem: str,
        function_name: str,
        config: Optional[InterviewConfig] = None
    ) -> str:
        """Start a new interview session and return opening message."""
        if config:
            self.state.config = config
        
        self.state.start_interview(problem, function_name)
        
        # Return appropriate opening based on mode
        if self.state.voice_enabled:
            return self._get_stage_voice_text(InterviewStage.GREETING)
        else:
            return self._get_intro_message()
    
    def _get_intro_message(self) -> str:
        """Generate the opening interview message."""
        difficulty = self.state.config.difficulty
        
        intros = {
            InterviewDifficulty.JUNIOR: [
                f"Hi! Welcome to your interview. I'm excited to work through a coding problem with you today. "
                f"We'll be working on: **{self.state.problem_name}**\n\n"
                f"Don't worry about getting everything perfect - I'm here to see how you think through problems. "
                f"Feel free to ask clarifying questions. Ready to begin?",
            ],
            InterviewDifficulty.MID: [
                f"Hello! Thanks for joining. Today we'll be tackling: **{self.state.problem_name}**\n\n"
                f"I'd like to see your problem-solving approach, so please think out loud as you work. "
                f"Before you start coding, walk me through how you'd approach this. "
                f"What questions do you have about the problem?",
            ],
            InterviewDifficulty.SENIOR: [
                f"Good to meet you. Let's dive into a technical problem: **{self.state.problem_name}**\n\n"
                f"I'll be evaluating your approach, code quality, and ability to optimize. "
                f"Start by clarifying any ambiguities, then outline your solution before coding. "
                f"What's your initial assessment of this problem?",
            ],
        }
        
        return random.choice(intros.get(difficulty, intros[InterviewDifficulty.MID]))
    
    def process_response(self, user_message: str, user_code: str = "") -> str:
        """Process user response and generate appropriate interviewer reply."""
        # Add user message to history
        self.state.add_message("user", user_message)
        
        # Analyze user response
        self._analyze_response(user_message, user_code)
        
        # Generate response based on current stage
        response = self._generate_stage_response(user_message, user_code)
        
        # Add response to history
        self.state.add_message("assistant", response)
        
        return response
    
    def _analyze_response(self, message: str, code: str):
        """Analyze user's response to update scores and state."""
        msg_lower = message.lower()
        
        # Check for complexity mentions
        complexity_patterns = [
            r'o\([^)]+\)', r'time complexity', r'space complexity',
            r'linear', r'quadratic', r'logarithmic', r'constant time',
            r'n squared', r'n log n', r'big o'
        ]
        if any(re.search(p, msg_lower) for p in complexity_patterns):
            self.state.user_mentioned_complexity = True
            self.state.scores.complexity_analysis = min(100, self.state.scores.complexity_analysis + 25)
            self.state.scores.evaluated_aspects["discussed_complexity"] = True
        
        # Check for edge case awareness
        edge_case_patterns = [
            r'edge case', r'empty', r'null', r'none', r'negative',
            r'zero', r'overflow', r'boundary', r'corner case', r'what if'
        ]
        if any(re.search(p, msg_lower) for p in edge_case_patterns):
            self.state.user_mentioned_edge_cases = True
            self.state.scores.problem_solving = min(100, self.state.scores.problem_solving + 15)
            self.state.scores.evaluated_aspects["mentioned_edge_cases"] = True
        
        # Check for clarifying questions
        if '?' in message and self.state.current_stage in [InterviewStage.INTRO, InterviewStage.APPROACH]:
            self.state.user_asked_clarifying = True
            self.state.scores.communication = min(100, self.state.scores.communication + 10)
            self.state.scores.evaluated_aspects["asked_clarifying_questions"] = True
        
        # Check for approach explanation
        approach_patterns = [
            r'approach', r'strategy', r'plan', r'first.*then',
            r'step', r'iterate', r'traverse', r'algorithm', r'technique'
        ]
        if any(re.search(p, msg_lower) for p in approach_patterns):
            self.state.user_explained_approach = True
            self.state.scores.communication = min(100, self.state.scores.communication + 15)
            self.state.scores.problem_solving = min(100, self.state.scores.problem_solving + 10)
            self.state.scores.evaluated_aspects["explained_approach"] = True
        
        # Evaluate code if present
        if code and len(code.strip()) > 50:
            self.state.code_attempts += 1
            self._evaluate_code_quality(code)
    
    def _evaluate_code_quality(self, code: str):
        """Evaluate the quality of submitted code."""
        score_delta = 0
        
        # Check for function definition
        if f"def {self.state.function_name}" in code:
            score_delta += 10
        
        # Check for docstring
        if '"""' in code or "'''" in code:
            score_delta += 10
        
        # Check for proper returns
        if 'return ' in code:
            score_delta += 10
        
        # Penalize bare pass statements
        if code.strip().endswith('pass'):
            score_delta -= 20
        
        # Check for comments
        if '#' in code:
            score_delta += 5
        
        # Update code quality score
        self.state.scores.code_quality = min(100, max(0, self.state.scores.code_quality + score_delta))
    
    def _generate_stage_response(self, user_message: str, user_code: str) -> str:
        """Generate response appropriate for the current interview stage."""
        stage = self.state.current_stage
        
        if stage == InterviewStage.GREETING:
            return self._handle_greeting_stage(user_message)
        elif stage == InterviewStage.SELF_INTRO:
            return self._handle_self_intro_stage(user_message)
        elif stage == InterviewStage.INTRO:
            return self._handle_intro_stage(user_message)
        elif stage == InterviewStage.APPROACH:
            return self._handle_approach_stage(user_message)
        elif stage == InterviewStage.CODING:
            return self._handle_coding_stage(user_message, user_code)
        elif stage == InterviewStage.OPTIMIZATION:
            return self._handle_optimization_stage(user_message, user_code)
        elif stage == InterviewStage.BEHAVIORAL:
            return self._handle_behavioral_stage(user_message)
        elif stage == InterviewStage.WRAPUP:
            return self._handle_wrapup_stage(user_message)
        else:
            return self._handle_completed_stage()
    
    def _handle_greeting_stage(self, message: str) -> str:
        """Handle greeting stage (voice mode only)."""
        # Greeting is typically auto-advanced after audio plays
        # This handles any user response during greeting
        self.state.greeting_completed = True
        self.state.advance_stage()
        return self._get_stage_voice_text(InterviewStage.SELF_INTRO)
    
    def _handle_self_intro_stage(self, message: str) -> str:
        """Handle self-introduction stage (voice mode only)."""
        # Process the self-introduction
        if message and not self.state.self_intro_completed:
            return self.process_self_introduction(message)
        
        # If already processed, move to intro
        self.state.advance_stage()
        return self._get_intro_message()
    
    def _handle_intro_stage(self, message: str) -> str:
        """Handle intro stage responses."""
        msg_lower = message.lower()
        
        # If they asked clarifying questions, answer and move to approach
        if '?' in message:
            self.state.advance_stage()
            return (
                "Great question! That shows good problem-solving instincts. "
                "For this problem, you can assume standard constraints apply. "
                "Now, before you start coding, can you walk me through your approach? "
                "How would you break down this problem?"
            )
        
        # If they're ready, move to approach
        ready_patterns = ['ready', 'yes', 'let\'s', 'sure', 'ok', 'okay', 'go ahead', 'start']
        if any(p in msg_lower for p in ready_patterns):
            self.state.advance_stage()
            return (
                "Great! Before diving into code, I'd like to hear your approach. "
                "How would you solve this problem? What data structures or algorithms come to mind?"
            )
        
        # Otherwise, prompt them
        return (
            "Take a moment to read through the problem. "
            "When you're ready, let me know if you have any questions, "
            "or start by explaining how you'd approach this."
        )
    
    def _handle_approach_stage(self, message: str) -> str:
        """Handle approach discussion stage."""
        responses = []
        
        # Check what they've mentioned
        if self.state.user_explained_approach:
            responses.append("Good approach!")
        
        if not self.state.user_mentioned_edge_cases:
            responses.append("What edge cases should we consider?")
        elif not self.state.user_mentioned_complexity:
            responses.append("What's the expected time complexity of your approach?")
        else:
            # They've covered the basics, move to coding
            self.state.advance_stage()
            responses.append(
                "Solid analysis. Go ahead and implement your solution. "
                "Talk through your code as you write it."
            )
            return " ".join(responses)
        
        # Add follow-up based on what's missing
        if len(self.state.stage_history.get(InterviewStage.APPROACH, [])) > 4:
            # They've been in this stage a while, move on
            self.state.advance_stage()
            responses.append("Let's move to implementation. Start coding your solution.")
        
        return " ".join(responses)
    
    def _handle_coding_stage(self, message: str, code: str) -> str:
        """Handle coding stage responses."""
        msg_lower = message.lower()
        
        # Check if they're asking for help
        help_patterns = ['stuck', 'hint', 'help', 'not sure', 'confused']
        if any(p in msg_lower for p in help_patterns):
            return (
                "Let's break it down. What's the first thing you need to do? "
                "Think about the input and what transformation needs to happen."
            )
        
        # Check code progress
        if code and len(code.strip()) > 100:
            # They have substantial code
            if 'return' in code and 'def ' in code:
                self.state.scores.code_quality = min(100, self.state.scores.code_quality + 20)
                self.state.scores.evaluated_aspects["wrote_working_code"] = True
                
                # Probe their implementation
                probing_questions = [
                    f"Walk me through what your `{self.state.function_name}` function does step by step.",
                    "What happens when we trace through this with a simple example?",
                    "Are there any cases where this might not work as expected?",
                ]
                
                # Check if we should move to optimization
                if len(self.state.stage_history.get(InterviewStage.CODING, [])) > 6:
                    self.state.advance_stage()
                    return (
                        "Your solution looks functional. Let's talk about optimization. "
                        "What's the current time and space complexity? Can we do better?"
                    )
                
                return random.choice(probing_questions)
        
        # Encourage progress
        encouragements = [
            "Keep going. What's the next step in your implementation?",
            "Good progress. How will you handle the core logic?",
            "Think about what data structure would work best here.",
        ]
        return random.choice(encouragements)
    
    def _handle_optimization_stage(self, message: str, code: str) -> str:
        """Handle optimization discussion stage."""
        
        if self.state.user_mentioned_complexity:
            self.state.scores.complexity_analysis = min(100, self.state.scores.complexity_analysis + 20)
            
            # Follow up on their complexity analysis
            followups = [
                "Can we reduce the space complexity?",
                "Is there a way to avoid that nested loop?",
                "What if we used a different data structure?",
            ]
            
            # Check if we should move on
            if len(self.state.stage_history.get(InterviewStage.OPTIMIZATION, [])) > 4:
                if self.state.config.include_behavioral and self.state.config.interview_type != InterviewType.TECHNICAL:
                    self.state.advance_stage()
                    return (
                        "Good optimization discussion. Let's switch gears. "
                        "Tell me about a challenging technical problem you've solved recently."
                    )
                else:
                    self.state.advance_stage()
                    return self._get_wrapup_intro()
            
            return random.choice(followups)
        
        # They haven't discussed complexity yet
        return (
            "Let's analyze your solution. What's the time complexity? "
            "And what about space complexity?"
        )
    
    def _handle_behavioral_stage(self, message: str) -> str:
        """Handle behavioral questions stage."""
        behavioral_questions = [
            "Tell me about a time you had to debug a difficult issue. How did you approach it?",
            "Describe a project where you had to learn a new technology quickly.",
            "How do you handle disagreements about technical decisions with teammates?",
            "What's a piece of code you're particularly proud of? Why?",
            "Tell me about a time you had to meet a tight deadline. How did you prioritize?",
        ]
        
        # Filter out already asked questions
        available = [q for q in behavioral_questions if q not in self.state.asked_questions]
        
        if not available or len(self.state.stage_history.get(InterviewStage.BEHAVIORAL, [])) > 4:
            self.state.advance_stage()
            return self._get_wrapup_intro()
        
        # Score their response
        if len(message) > 100:
            self.state.scores.communication = min(100, self.state.scores.communication + 15)
        
        # Ask next behavioral question
        next_q = random.choice(available)
        self.state.asked_questions.append(next_q)
        
        return f"Thanks for sharing that. {next_q}"
    
    def _handle_wrapup_stage(self, message: str) -> str:
        """Handle wrapup stage."""
        if len(self.state.stage_history.get(InterviewStage.WRAPUP, [])) > 2:
            self.state.advance_stage()
            return self._generate_final_feedback()
        
        return (
            "Do you have any questions for me about the role or team? "
            "This is your chance to learn more about the opportunity."
        )
    
    def _get_wrapup_intro(self) -> str:
        """Get the introduction to wrapup stage."""
        return (
            "We're coming to the end of our time. "
            "Overall, you've done well. Any questions for me?"
        )
    
    def _handle_completed_stage(self) -> str:
        """Handle completed interview."""
        return self._generate_final_feedback()
    
    def _generate_final_feedback(self) -> str:
        """Generate comprehensive interview feedback."""
        scores = self.state.scores
        total = scores.get_total()
        grade = scores.get_grade()
        recommendation = scores.get_hiring_recommendation()
        
        # Build strengths and improvements lists
        strengths = []
        improvements = []
        
        if scores.evaluated_aspects["explained_approach"]:
            strengths.append("Clear problem-solving approach")
        else:
            improvements.append("Explain your approach before coding")
        
        if scores.evaluated_aspects["mentioned_edge_cases"]:
            strengths.append("Good edge case awareness")
        else:
            improvements.append("Consider edge cases more thoroughly")
        
        if scores.evaluated_aspects["discussed_complexity"]:
            strengths.append("Strong complexity analysis")
        else:
            improvements.append("Practice analyzing time/space complexity")
        
        if scores.evaluated_aspects["asked_clarifying_questions"]:
            strengths.append("Asked good clarifying questions")
        else:
            improvements.append("Ask more clarifying questions upfront")
        
        if scores.evaluated_aspects["wrote_working_code"]:
            strengths.append("Produced working code")
        else:
            improvements.append("Focus on getting to working code faster")
        
        feedback = f"""## 📊 Interview Feedback

**Overall Score:** {total:.0f}/100 (Grade: {grade})
**Recommendation:** {recommendation}

### Score Breakdown
- **Problem Solving:** {scores.problem_solving:.0f}/100
- **Communication:** {scores.communication:.0f}/100
- **Code Quality:** {scores.code_quality:.0f}/100
- **Complexity Analysis:** {scores.complexity_analysis:.0f}/100

### Strengths
{chr(10).join(f'✓ {s}' for s in strengths) if strengths else '• Keep practicing!'}

### Areas to Improve
{chr(10).join(f'• {i}' for i in improvements) if improvements else '✓ Great job overall!'}

### Tips for Next Time
1. Always clarify requirements before starting
2. Think out loud - communication matters as much as code
3. Consider edge cases early in your approach
4. Analyze complexity before and after optimization

Good luck with your interviews! 🚀"""
        
        return feedback
    
    def force_end_interview(self) -> str:
        """Force end the interview (e.g., time's up)."""
        self.state.current_stage = InterviewStage.COMPLETED
        return self._generate_final_feedback()
    
    def get_stage_progress(self) -> Dict[str, Any]:
        """Get current progress through interview stages."""
        stages = list(InterviewStage)
        current_idx = stages.index(self.state.current_stage)
        
        return {
            "current_stage": self.state.current_stage.value,
            "stage_index": current_idx,
            "total_stages": len(stages) - 1,  # Exclude COMPLETED
            "progress_percent": (current_idx / (len(stages) - 1)) * 100,
            "elapsed_time": self.state.get_elapsed_time(),
            "remaining_time": self.state.get_remaining_time(),
            "is_time_up": self.state.is_time_up(),
        }


# Behavioral questions pool for different levels
BEHAVIORAL_QUESTIONS = {
    InterviewDifficulty.JUNIOR: [
        "Tell me about a project you worked on in school or personally that you're proud of.",
        "How do you approach learning a new programming concept?",
        "Describe a time when you had to ask for help. How did you go about it?",
        "What interests you most about software development?",
    ],
    InterviewDifficulty.MID: [
        "Tell me about a challenging bug you had to solve. What was your process?",
        "Describe a time when you had to work with a difficult team member.",
        "How do you prioritize when you have multiple deadlines?",
        "Tell me about a time you had to push back on a requirement.",
    ],
    InterviewDifficulty.SENIOR: [
        "Describe a system you designed from scratch. What were the key decisions?",
        "Tell me about a time you had to mentor a junior developer.",
        "How do you handle technical debt in your projects?",
        "Describe a time when you had to make a difficult tradeoff.",
    ],
}


def create_interview_engine(
    difficulty: str = "mid",
    interview_type: str = "technical",
    time_limit: int = 30,
    show_live_score: bool = False
) -> InterviewEngine:
    """Factory function to create a configured interview engine."""
    
    difficulty_map = {
        "junior": InterviewDifficulty.JUNIOR,
        "mid": InterviewDifficulty.MID,
        "senior": InterviewDifficulty.SENIOR,
    }
    
    type_map = {
        "technical": InterviewType.TECHNICAL,
        "behavioral": InterviewType.BEHAVIORAL,
        "mixed": InterviewType.MIXED,
    }
    
    config = InterviewConfig(
        difficulty=difficulty_map.get(difficulty.lower(), InterviewDifficulty.MID),
        interview_type=type_map.get(interview_type.lower(), InterviewType.TECHNICAL),
        time_limit_minutes=time_limit,
        show_live_score=show_live_score,
        include_behavioral=(interview_type.lower() != "technical"),
    )
    
    state = InterviewState(config=config)
    return InterviewEngine(state)