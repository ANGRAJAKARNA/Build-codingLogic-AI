# voice_engine.py
"""
Voice Engine for Interview Mode
Handles Text-to-Speech and Speech-to-Text functionality for PyCode interviews.

Features:
- Text-to-Speech with gTTS (online) and pyttsx3 (offline) fallback
- Speech-to-Text using SpeechRecognition library
- Audio recorder integration for Streamlit
- Voice scripts for all interview stages
"""

import os
import io
import time
import tempfile
import base64
from typing import Optional, Tuple, Dict, List
from pathlib import Path
from dataclasses import dataclass, field
from enum import Enum

# TTS imports with availability flags
GTTS_AVAILABLE = False
try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    pass

PYTTSX3_AVAILABLE = False
try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except ImportError:
    pass

# STT imports
SR_AVAILABLE = False
try:
    import speech_recognition as sr
    SR_AVAILABLE = True
except ImportError:
    pass


class VoiceMode(Enum):
    """Voice mode options for interview."""
    TEXT_ONLY = "text"
    VOICE_ENABLED = "voice"


class TTSEngine(Enum):
    """Available TTS engines."""
    GTTS = "gtts"           # Google TTS (requires internet, better quality)
    PYTTSX3 = "pyttsx3"     # Offline TTS (works without internet)
    AUTO = "auto"           # Auto-select best available


@dataclass
class VoiceConfig:
    """Configuration for voice features."""
    mode: VoiceMode = VoiceMode.TEXT_ONLY
    tts_engine: TTSEngine = TTSEngine.AUTO
    speech_rate: float = 1.0
    voice_lang: str = "en"
    listen_timeout: int = 10
    self_intro_duration: int = 30
    pause_after_greeting: float = 3.0
    
    # Voice personality settings
    interviewer_name: str = "Alex"
    interviewer_tone: str = "professional"  # professional, friendly, strict


class TextToSpeech:
    """
    Text-to-Speech handler with automatic fallback.
    Tries gTTS first (better quality), falls back to pyttsx3 (offline).
    """
    
    def __init__(self, engine: TTSEngine = TTSEngine.AUTO, lang: str = "en"):
        self.engine = engine
        self.lang = lang
        self._pyttsx_engine = None
        
    def _get_pyttsx_engine(self):
        """Lazy initialization of pyttsx3 engine."""
        if self._pyttsx_engine is None and PYTTSX3_AVAILABLE:
            try:
                self._pyttsx_engine = pyttsx3.init()
                # Try to configure a better voice
                voices = self._pyttsx_engine.getProperty('voices')
                if voices:
                    # Try to find a female voice for variety
                    for voice in voices:
                        if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                            self._pyttsx_engine.setProperty('voice', voice.id)
                            break
                self._pyttsx_engine.setProperty('rate', 150)  # Words per minute
                self._pyttsx_engine.setProperty('volume', 0.9)
            except Exception as e:
                print(f"pyttsx3 init error: {e}")
                self._pyttsx_engine = None
        return self._pyttsx_engine
    
    def is_available(self) -> bool:
        """Check if any TTS engine is available."""
        return GTTS_AVAILABLE or PYTTSX3_AVAILABLE
    
    def synthesize(self, text: str) -> Optional[bytes]:
        """
        Convert text to speech audio bytes.
        Returns MP3 audio data or None if failed.
        
        Uses auto-fallback: gTTS (online) -> pyttsx3 (offline)
        """
        if not text or not text.strip():
            return None
        
        # Determine which engine to use
        if self.engine == TTSEngine.GTTS and GTTS_AVAILABLE:
            return self._synthesize_gtts(text)
        elif self.engine == TTSEngine.PYTTSX3 and PYTTSX3_AVAILABLE:
            return self._synthesize_pyttsx(text)
        elif self.engine == TTSEngine.AUTO:
            # Try gTTS first, fallback to pyttsx3
            if GTTS_AVAILABLE:
                result = self._synthesize_gtts(text)
                if result:
                    return result
            if PYTTSX3_AVAILABLE:
                return self._synthesize_pyttsx(text)
        
        return None
    
    def _synthesize_gtts(self, text: str) -> Optional[bytes]:
        """Use Google TTS (requires internet)."""
        try:
            tts = gTTS(text=text, lang=self.lang, slow=False)
            audio_buffer = io.BytesIO()
            tts.write_to_fp(audio_buffer)
            audio_buffer.seek(0)
            return audio_buffer.read()
        except Exception as e:
            print(f"gTTS error: {e}")
            return None
    
    def _synthesize_pyttsx(self, text: str) -> Optional[bytes]:
        """Use pyttsx3 (offline)."""
        try:
            engine = self._get_pyttsx_engine()
            if not engine:
                return None
            
            # Save to temp file and read back
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
                temp_path = f.name
            
            engine.save_to_file(text, temp_path)
            engine.runAndWait()
            
            # Read the audio file
            if os.path.exists(temp_path):
                with open(temp_path, 'rb') as f:
                    audio_data = f.read()
                os.unlink(temp_path)
                return audio_data
            return None
        except Exception as e:
            print(f"pyttsx3 error: {e}")
            return None
    
    def get_audio_html(self, audio_bytes: bytes, autoplay: bool = True) -> str:
        """Generate HTML audio element for Streamlit embedding."""
        if not audio_bytes:
            return ""
        audio_b64 = base64.b64encode(audio_bytes).decode()
        autoplay_attr = "autoplay" if autoplay else ""
        return f'''
        <audio {autoplay_attr} controls style="width:100%;height:40px;">
            <source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3">
            Your browser does not support the audio element.
        </audio>
        '''


class SpeechToText:
    """
    Speech-to-Text handler using SpeechRecognition library.
    Supports microphone input and audio file transcription.
    """
    
    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.recognizer = sr.Recognizer() if SR_AVAILABLE else None
        
        # Configure recognizer settings
        if self.recognizer:
            self.recognizer.energy_threshold = 300
            self.recognizer.dynamic_energy_threshold = True
            self.recognizer.pause_threshold = 0.8
        
    def is_available(self) -> bool:
        """Check if STT is available."""
        return SR_AVAILABLE and self.recognizer is not None
    
    def listen_from_microphone(self, duration: int = None) -> Tuple[bool, str]:
        """
        Listen from microphone and transcribe.
        
        Note: This method requires PyAudio to be installed. If PyAudio is not available,
        use the browser-based audio recorder and call transcribe_audio_bytes() instead.
        
        Args:
            duration: Maximum listening duration in seconds
            
        Returns:
            Tuple of (success, text_or_error_message)
        """
        if not self.is_available():
            return False, "Speech recognition not available. Please install SpeechRecognition."
        
        duration = duration or self.timeout
        
        try:
            # Check if PyAudio/Microphone is available
            try:
                with sr.Microphone() as source:
                    # Adjust for ambient noise
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    
                    # Listen with timeout
                    audio = self.recognizer.listen(
                        source,
                        timeout=duration,
                        phrase_time_limit=duration
                    )
                    
                    # Recognize using Google Speech Recognition (free tier)
                    text = self.recognizer.recognize_google(audio)
                    return True, text
            except (AttributeError, OSError) as e:
                # PyAudio not installed or microphone not accessible
                return False, "Direct microphone access not available. Please use the browser-based recorder instead."
                
        except sr.WaitTimeoutError:
            return False, "Listening timed out - no speech detected"
        except sr.UnknownValueError:
            return False, "Could not understand audio - please speak more clearly"
        except sr.RequestError as e:
            return False, f"Speech recognition service error: {e}"
        except Exception as e:
            return False, f"Error: {e}"
    
    def transcribe_audio_file(self, audio_path: str) -> Tuple[bool, str]:
        """
        Transcribe an audio file.
        
        Args:
            audio_path: Path to the audio file (WAV format preferred)
            
        Returns:
            Tuple of (success, text_or_error_message)
        """
        if not self.is_available():
            return False, "Speech recognition not available"
        
        if not os.path.exists(audio_path):
            return False, f"Audio file not found: {audio_path}"
        
        try:
            with sr.AudioFile(audio_path) as source:
                audio = self.recognizer.record(source)
                text = self.recognizer.recognize_google(audio)
                return True, text
        except sr.UnknownValueError:
            return False, "Could not understand audio in file"
        except sr.RequestError as e:
            return False, f"Speech recognition service error: {e}"
        except Exception as e:
            return False, f"Error transcribing: {e}"
    
    def transcribe_audio_bytes(self, audio_bytes: bytes, sample_rate: int = 16000) -> Tuple[bool, str]:
        """
        Transcribe audio from bytes (useful for streamlit audio recorder).
        
        Args:
            audio_bytes: Raw audio data
            sample_rate: Audio sample rate
            
        Returns:
            Tuple of (success, text_or_error_message)
        """
        if not self.is_available():
            return False, "Speech recognition not available"
        
        try:
            # Save to temp file first
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
                f.write(audio_bytes)
                temp_path = f.name
            
            # Transcribe the file
            result = self.transcribe_audio_file(temp_path)
            
            # Clean up
            if os.path.exists(temp_path):
                os.unlink(temp_path)
            
            return result
        except Exception as e:
            return False, f"Error processing audio: {e}"


class VoiceInterviewer:
    """
    Voice-enabled interviewer that manages TTS/STT interactions.
    Orchestrates the voice interview experience.
    """
    
    def __init__(self, config: VoiceConfig = None):
        self.config = config or VoiceConfig()
        
        # Determine TTS engine based on config
        tts_engine = self.config.tts_engine
        if tts_engine == TTSEngine.AUTO:
            if GTTS_AVAILABLE:
                tts_engine = TTSEngine.GTTS
            elif PYTTSX3_AVAILABLE:
                tts_engine = TTSEngine.PYTTSX3
        
        self.tts = TextToSpeech(
            engine=tts_engine,
            lang=self.config.voice_lang
        )
        self.stt = SpeechToText(timeout=self.config.listen_timeout)
        
        # Conversation state
        self.is_speaking = False
        self.is_listening = False
        self.last_spoken_text = ""
        self.last_heard_text = ""
        self.audio_cache: Dict[str, bytes] = {}
        
    def is_voice_available(self) -> bool:
        """Check if voice features are available."""
        return self.tts.is_available()
    
    def speak(self, text: str, cache_key: str = None) -> Optional[bytes]:
        """
        Generate speech audio for text.
        
        Args:
            text: Text to speak
            cache_key: Optional key to cache the audio
            
        Returns:
            Audio bytes or None if failed
        """
        if not text:
            return None
        
        # Check cache first
        if cache_key and cache_key in self.audio_cache:
            return self.audio_cache[cache_key]
        
        self.is_speaking = True
        self.last_spoken_text = text
        
        audio = self.tts.synthesize(text)
        
        # Cache the result
        if cache_key and audio:
            self.audio_cache[cache_key] = audio
        
        self.is_speaking = False
        return audio
    
    def listen(self, duration: int = None) -> Tuple[bool, str]:
        """
        Listen for user speech.
        
        Args:
            duration: Listening duration in seconds
            
        Returns:
            Tuple of (success, transcribed_text_or_error)
        """
        self.is_listening = True
        duration = duration or self.config.listen_timeout
        
        success, text = self.stt.listen_from_microphone(duration)
        
        if success:
            self.last_heard_text = text
        
        self.is_listening = False
        return success, text
    
    def transcribe_recorded_audio(self, audio_bytes: bytes) -> Tuple[bool, str]:
        """
        Transcribe audio recorded by user.
        
        Args:
            audio_bytes: Recorded audio data
            
        Returns:
            Tuple of (success, transcribed_text_or_error)
        """
        success, text = self.stt.transcribe_audio_bytes(audio_bytes)
        
        if success:
            self.last_heard_text = text
        
        return success, text
    
    def get_greeting(self) -> str:
        """Get the initial greeting based on config."""
        greetings = {
            "professional": "Hi, please settle down for the interview. Take a moment to get comfortable.",
            "friendly": "Hey there! Welcome to your interview. Take a deep breath and relax.",
            "strict": "Hello. Your interview begins now. Please be prepared."
        }
        return greetings.get(self.config.interviewer_tone, greetings["professional"])
    
    def get_intro_request(self) -> str:
        """Get the self-introduction request."""
        requests = {
            "professional": "Now, please introduce yourself. Tell me about your background, experience, and what brings you here today. You have about 30 seconds.",
            "friendly": "I'd love to hear about you! Tell me a bit about yourself and your journey so far. Take your time, about 30 seconds.",
            "strict": "State your name, background, and relevant experience. You have 30 seconds."
        }
        return requests.get(self.config.interviewer_tone, requests["professional"])
    
    def get_intro_followup(self) -> str:
        """Get the response after self-introduction."""
        followups = {
            "professional": "Thank you for that introduction. Let's proceed with the technical portion.",
            "friendly": "That's great! Thanks for sharing. Now let's dive into some coding!",
            "strict": "Noted. Moving on to technical questions."
        }
        return followups.get(self.config.interviewer_tone, followups["professional"])
    
    def clear_cache(self):
        """Clear the audio cache."""
        self.audio_cache.clear()


# Voice scripts for all interview stages
VOICE_SCRIPTS = {
    # Greeting and Introduction
    "greeting": "Hi, please settle down for the interview.",
    "intro_request": "Now, please introduce yourself. You have about 30 seconds.",
    "intro_followup": "Thank you for that introduction.",
    
    # Problem Presentation
    "problem_intro": "Let's move on to the technical portion. I'll present you with a coding problem.",
    "problem_read": "Here is your problem: {problem}",
    "clarification_prompt": "Do you have any questions about the problem before we proceed?",
    
    # Approach Discussion
    "approach_request": "Before you start coding, please explain your approach to solving this problem.",
    "approach_followup": "Good thinking. What data structures will you use?",
    "edge_cases_prompt": "What edge cases should we consider?",
    "complexity_prompt": "What's the expected time complexity of your approach?",
    
    # Coding Stage
    "coding_start": "Great, go ahead and implement your solution. Talk through your code as you write it.",
    "coding_progress": "Good progress. Keep going.",
    "coding_stuck": "Let's break it down. What's the first thing you need to do?",
    "coding_complete": "Your solution looks functional. Let's discuss it.",
    
    # Optimization
    "optimization_request": "Can you analyze the time and space complexity of your solution?",
    "optimization_followup": "Is there a way to improve this further?",
    
    # Behavioral
    "behavioral_intro": "Now let's discuss some behavioral questions.",
    "behavioral_question": "Tell me about a time when {scenario}",
    
    # Wrap-up
    "wrapup": "We're coming to the end of the interview. Do you have any questions for me?",
    "goodbye": "Thank you for your time today. We'll be in touch soon. Good luck!",
    
    # Feedback Phrases
    "positive_feedback": [
        "Good thinking.",
        "That's a solid approach.",
        "I like how you're thinking about this.",
        "Nice work.",
        "Excellent observation."
    ],
    "encouragement": [
        "Take your time.",
        "You're on the right track.",
        "Keep going.",
        "That's okay, let's work through it.",
    ],
    "clarification": [
        "Could you explain that a bit more?",
        "What do you mean by that?",
        "Can you elaborate?",
        "Walk me through your reasoning.",
    ],
    "transition": [
        "Let's move on to the next part.",
        "Good, let's continue.",
        "Alright, moving forward.",
    ]
}


def get_voice_capabilities() -> Dict[str, any]:
    """
    Check what voice capabilities are available on the system.
    
    Returns:
        Dict with availability flags and recommendations
    """
    capabilities = {
        "tts_gtts": GTTS_AVAILABLE,
        "tts_pyttsx3": PYTTSX3_AVAILABLE,
        "stt": SR_AVAILABLE,
        "tts_available": GTTS_AVAILABLE or PYTTSX3_AVAILABLE,
        "voice_mode_available": GTTS_AVAILABLE or PYTTSX3_AVAILABLE,
        "full_voice_available": (GTTS_AVAILABLE or PYTTSX3_AVAILABLE) and SR_AVAILABLE,
    }
    
    # Determine recommended TTS engine
    if GTTS_AVAILABLE:
        capabilities["recommended_tts"] = "gtts"
        capabilities["tts_quality"] = "high"
    elif PYTTSX3_AVAILABLE:
        capabilities["recommended_tts"] = "pyttsx3"
        capabilities["tts_quality"] = "medium"
    else:
        capabilities["recommended_tts"] = None
        capabilities["tts_quality"] = None
    
    # Build status message
    status_parts = []
    if capabilities["tts_gtts"]:
        status_parts.append("gTTS (online)")
    if capabilities["tts_pyttsx3"]:
        status_parts.append("pyttsx3 (offline)")
    if capabilities["stt"]:
        status_parts.append("Speech Recognition")
    
    capabilities["status_message"] = ", ".join(status_parts) if status_parts else "No voice features available"
    
    return capabilities


def create_voice_interviewer(
    tone: str = "professional",
    listen_timeout: int = 10,
    self_intro_duration: int = 30
) -> VoiceInterviewer:
    """
    Factory function to create a configured voice interviewer.
    
    Args:
        tone: Interviewer tone (professional, friendly, strict)
        listen_timeout: Default listening timeout in seconds
        self_intro_duration: Duration for self-introduction in seconds
        
    Returns:
        Configured VoiceInterviewer instance
    """
    config = VoiceConfig(
        mode=VoiceMode.VOICE_ENABLED,
        tts_engine=TTSEngine.AUTO,
        listen_timeout=listen_timeout,
        self_intro_duration=self_intro_duration,
        interviewer_tone=tone
    )
    
    return VoiceInterviewer(config)


# Utility functions for Streamlit integration

def get_audio_player_html(audio_bytes: bytes, autoplay: bool = True, hidden: bool = False) -> str:
    """
    Generate HTML for audio player in Streamlit.
    
    Args:
        audio_bytes: Audio data to play
        autoplay: Whether to autoplay
        hidden: Whether to hide the player controls
        
    Returns:
        HTML string for the audio player
    """
    if not audio_bytes:
        return ""
    
    audio_b64 = base64.b64encode(audio_bytes).decode()
    autoplay_attr = "autoplay" if autoplay else ""
    style = "display:none;" if hidden else "width:100%;height:40px;"
    
    return f'''
    <audio {autoplay_attr} controls style="{style}">
        <source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3">
        Your browser does not support audio playback.
    </audio>
    '''


def estimate_speech_duration(text: str, words_per_minute: int = 150) -> float:
    """
    Estimate how long it will take to speak the given text.
    
    Args:
        text: Text to be spoken
        words_per_minute: Average speaking rate
        
    Returns:
        Estimated duration in seconds
    """
    if not text:
        return 0.0
    
    word_count = len(text.split())
    return (word_count / words_per_minute) * 60

