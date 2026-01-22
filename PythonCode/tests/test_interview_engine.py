# tests/test_interview_engine.py
"""
Unit tests for the interview engine module.
Tests interview flow, scoring, and feedback generation.
"""

import pytest
import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from interview_engine import (
    InterviewEngine, InterviewState, InterviewConfig,
    InterviewDifficulty, InterviewType, InterviewStage,
    InterviewScores, create_interview_engine
)


class TestInterviewScores:
    """Tests for interview scoring."""
    
    def test_initial_scores(self):
        """Test initial scores are zero."""
        scores = InterviewScores()
        
        assert scores.problem_solving == 0.0
        assert scores.communication == 0.0
        assert scores.code_quality == 0.0
        assert scores.complexity_analysis == 0.0
    
    def test_get_total(self):
        """Test total score calculation."""
        scores = InterviewScores()
        scores.problem_solving = 100
        scores.communication = 100
        scores.code_quality = 100
        scores.complexity_analysis = 100
        
        # Total should be 100 (max)
        assert scores.get_total() == 100
    
    def test_get_total_weighted(self):
        """Test weighted score calculation."""
        scores = InterviewScores()
        # Only problem solving (weight: 0.35)
        scores.problem_solving = 100
        
        assert scores.get_total() == 35.0
    
    def test_get_grade_a(self):
        """Test A grade (>= 90)."""
        scores = InterviewScores()
        scores.problem_solving = 100
        scores.communication = 100
        scores.code_quality = 100
        scores.complexity_analysis = 100
        
        assert scores.get_grade() == "A"
    
    def test_get_grade_b(self):
        """Test B grade (80-89)."""
        scores = InterviewScores()
        scores.problem_solving = 80
        scores.communication = 80
        scores.code_quality = 80
        scores.complexity_analysis = 80
        
        # 80 total = B
        assert scores.get_grade() == "B"
    
    def test_get_hiring_recommendation_strong_hire(self):
        """Test Strong Hire recommendation (>= 85)."""
        scores = InterviewScores()
        scores.problem_solving = 100
        scores.communication = 100
        scores.code_quality = 100
        scores.complexity_analysis = 100
        
        assert scores.get_hiring_recommendation() == "Strong Hire"
    
    def test_get_hiring_recommendation_no_hire(self):
        """Test No Hire recommendation (< 40)."""
        scores = InterviewScores()
        # All zeros
        assert scores.get_hiring_recommendation() == "No Hire"


class TestInterviewConfig:
    """Tests for interview configuration."""
    
    def test_default_config(self):
        """Test default configuration values."""
        config = InterviewConfig()
        
        assert config.difficulty == InterviewDifficulty.MID
        assert config.interview_type == InterviewType.TECHNICAL
        assert config.time_limit_minutes == 30
    
    def test_custom_config(self):
        """Test custom configuration."""
        config = InterviewConfig(
            difficulty=InterviewDifficulty.SENIOR,
            interview_type=InterviewType.MIXED,
            time_limit_minutes=45
        )
        
        assert config.difficulty == InterviewDifficulty.SENIOR
        assert config.interview_type == InterviewType.MIXED
        assert config.time_limit_minutes == 45
    
    def test_stage_time_allocation_technical(self):
        """Test time allocation for technical interview."""
        config = InterviewConfig(
            interview_type=InterviewType.TECHNICAL,
            time_limit_minutes=30
        )
        allocation = config.get_stage_time_allocation()
        
        assert InterviewStage.INTRO in allocation
        assert InterviewStage.APPROACH in allocation
        assert InterviewStage.CODING in allocation
        assert InterviewStage.OPTIMIZATION in allocation
    
    def test_stage_time_allocation_behavioral(self):
        """Test time allocation for behavioral interview."""
        config = InterviewConfig(
            interview_type=InterviewType.BEHAVIORAL,
            time_limit_minutes=30
        )
        allocation = config.get_stage_time_allocation()
        
        assert InterviewStage.BEHAVIORAL in allocation


class TestInterviewState:
    """Tests for interview state management."""
    
    def test_start_interview(self):
        """Test starting a new interview."""
        state = InterviewState()
        state.start_interview("Two Sum", "two_sum")
        
        assert state.problem_name == "Two Sum"
        assert state.function_name == "two_sum"
        assert state.current_stage == InterviewStage.INTRO
        assert state.start_time is not None
    
    def test_advance_stage(self):
        """Test advancing through stages."""
        state = InterviewState()
        state.start_interview("Test Problem", "test_func")
        
        assert state.current_stage == InterviewStage.INTRO
        
        state.advance_stage()
        assert state.current_stage == InterviewStage.APPROACH
        
        state.advance_stage()
        assert state.current_stage == InterviewStage.CODING
    
    def test_add_message(self):
        """Test adding messages to history."""
        state = InterviewState()
        state.start_interview("Test", "test")
        
        state.add_message("user", "Hello")
        state.add_message("assistant", "Hi there!")
        
        assert len(state.conversation_history) == 2
        assert state.conversation_history[0]["role"] == "user"
        assert state.conversation_history[1]["role"] == "assistant"
    
    def test_elapsed_time(self):
        """Test elapsed time calculation."""
        state = InterviewState()
        state.start_interview("Test", "test")
        
        # Should be very small elapsed time
        elapsed = state.get_elapsed_time()
        assert elapsed >= 0
        assert elapsed < 5  # Less than 5 seconds
    
    def test_remaining_time(self):
        """Test remaining time calculation."""
        state = InterviewState()
        state.config.time_limit_minutes = 30
        state.start_interview("Test", "test")
        
        remaining = state.get_remaining_time()
        assert remaining > 0
        assert remaining <= 30 * 60  # 30 minutes in seconds


class TestInterviewEngine:
    """Tests for interview engine functionality."""
    
    def test_start_new_interview(self):
        """Test starting a new interview session."""
        engine = InterviewEngine()
        intro = engine.start_new_interview("Two Sum", "two_sum")
        
        assert intro is not None
        assert len(intro) > 0
        assert "Two Sum" in intro
    
    def test_process_response_intro(self):
        """Test processing response in intro stage."""
        engine = InterviewEngine()
        engine.start_new_interview("Test", "test")
        
        response = engine.process_response("Yes, I'm ready!")
        
        assert response is not None
        assert len(response) > 0
        # Should advance to approach stage
        assert engine.state.current_stage in [InterviewStage.INTRO, InterviewStage.APPROACH]
    
    def test_process_response_with_question(self):
        """Test processing response with clarifying question."""
        engine = InterviewEngine()
        engine.start_new_interview("Test", "test")
        
        response = engine.process_response("What are the constraints?")
        
        # Should recognize clarifying question
        assert engine.state.user_asked_clarifying == True
    
    def test_complexity_detection(self):
        """Test detection of complexity discussion."""
        engine = InterviewEngine()
        engine.start_new_interview("Test", "test")
        
        # Advance to approach stage first
        engine.state.current_stage = InterviewStage.APPROACH
        
        response = engine.process_response(
            "The time complexity is O(n) and space is O(1)"
        )
        
        assert engine.state.user_mentioned_complexity == True
        assert engine.state.scores.complexity_analysis > 0
    
    def test_edge_case_detection(self):
        """Test detection of edge case awareness."""
        engine = InterviewEngine()
        engine.start_new_interview("Test", "test")
        
        response = engine.process_response(
            "What if the input is empty or has negative numbers?"
        )
        
        assert engine.state.user_mentioned_edge_cases == True
    
    def test_force_end_interview(self):
        """Test forcing interview to end."""
        engine = InterviewEngine()
        engine.start_new_interview("Test", "test")
        
        feedback = engine.force_end_interview()
        
        assert engine.state.current_stage == InterviewStage.COMPLETED
        assert "Interview Feedback" in feedback
        assert "Score" in feedback
    
    def test_final_feedback_content(self):
        """Test content of final feedback."""
        engine = InterviewEngine()
        engine.start_new_interview("Test", "test")
        
        # Set some scores
        engine.state.scores.problem_solving = 80
        engine.state.scores.communication = 70
        engine.state.scores.code_quality = 60
        engine.state.scores.complexity_analysis = 50
        
        feedback = engine.force_end_interview()
        
        assert "Problem Solving" in feedback
        assert "Communication" in feedback
        assert "Code Quality" in feedback
        assert "Complexity Analysis" in feedback
    
    def test_get_stage_progress(self):
        """Test getting stage progress information."""
        engine = InterviewEngine()
        engine.start_new_interview("Test", "test")
        
        progress = engine.get_stage_progress()
        
        assert "current_stage" in progress
        assert "progress_percent" in progress
        assert "elapsed_time" in progress
        assert "remaining_time" in progress


class TestCreateInterviewEngine:
    """Tests for interview engine factory function."""
    
    def test_create_junior_technical(self):
        """Test creating junior technical interview."""
        engine = create_interview_engine(
            difficulty="junior",
            interview_type="technical",
            time_limit=20
        )
        
        assert engine.state.config.difficulty == InterviewDifficulty.JUNIOR
        assert engine.state.config.interview_type == InterviewType.TECHNICAL
        assert engine.state.config.time_limit_minutes == 20
    
    def test_create_senior_mixed(self):
        """Test creating senior mixed interview."""
        engine = create_interview_engine(
            difficulty="senior",
            interview_type="mixed",
            time_limit=45
        )
        
        assert engine.state.config.difficulty == InterviewDifficulty.SENIOR
        assert engine.state.config.interview_type == InterviewType.MIXED
    
    def test_create_with_invalid_difficulty(self):
        """Test creating with invalid difficulty defaults to MID."""
        engine = create_interview_engine(difficulty="invalid")
        
        assert engine.state.config.difficulty == InterviewDifficulty.MID


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

