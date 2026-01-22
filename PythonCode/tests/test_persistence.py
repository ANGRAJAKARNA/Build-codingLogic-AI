# tests/test_persistence.py
"""
Unit tests for the persistence module.
Tests progress saving, loading, streaks, achievements, and export/import.
"""

import pytest
import json
import sys
from pathlib import Path
from datetime import datetime, timedelta
import tempfile

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from persistence import (
    save_progress, load_progress, get_default_progress,
    save_question_time, get_best_time, format_time, get_stats,
    _serialize_progress, _deserialize_progress,
    update_streak, get_streak_info, check_achievements,
    export_progress, import_progress, merge_progress,
    ACHIEVEMENTS
)


class TestProgressSerialization:
    """Tests for progress serialization/deserialization."""
    
    def test_serialize_progress(self):
        """Test that progress with sets is serialized correctly."""
        progress = {
            "Basic": {"completed": {0, 1, 2}, "skipped": {3}, "times": {"0": 30.5}}
        }
        serialized = _serialize_progress(progress)
        
        assert serialized["Basic"]["completed"] == [0, 1, 2]
        assert serialized["Basic"]["skipped"] == [3]
        assert serialized["Basic"]["times"]["0"] == 30.5
    
    def test_deserialize_progress(self):
        """Test that serialized progress is deserialized correctly."""
        data = {
            "Basic": {"completed": [0, 1, 2], "skipped": [3], "times": {"0": 30.5}}
        }
        progress = _deserialize_progress(data)
        
        assert progress["Basic"]["completed"] == {0, 1, 2}
        assert progress["Basic"]["skipped"] == {3}
        assert progress["Basic"]["times"]["0"] == 30.5
    
    def test_roundtrip_serialization(self):
        """Test that serialize -> deserialize returns original structure."""
        original = {
            "Basic": {"completed": {0, 1, 2}, "skipped": {3}, "times": {"0": 30.5}},
            "Intermediate": {"completed": set(), "skipped": set(), "times": {}},
            "Advanced": {"completed": {0}, "skipped": set(), "times": {"0": 120.0}}
        }
        
        serialized = _serialize_progress(original)
        restored = _deserialize_progress(serialized)
        
        for stage in original:
            assert restored[stage]["completed"] == original[stage]["completed"]
            assert restored[stage]["skipped"] == original[stage]["skipped"]
            assert restored[stage]["times"] == original[stage]["times"]


class TestProgressFileOperations:
    """Tests for file-based progress operations."""
    
    def test_save_and_load_progress(self):
        """Test saving and loading progress to file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = Path(f.name)
        
        try:
            progress = {
                "Basic": {"completed": {0, 1}, "skipped": set(), "times": {"0": 25.0}},
                "Intermediate": {"completed": set(), "skipped": set(), "times": {}},
                "Advanced": {"completed": set(), "skipped": set(), "times": {}}
            }
            
            # Save
            result = save_progress(progress, temp_path)
            assert result == True
            
            # Load
            loaded = load_progress(temp_path)
            assert loaded["Basic"]["completed"] == {0, 1}
            assert loaded["Basic"]["times"]["0"] == 25.0
        finally:
            temp_path.unlink(missing_ok=True)
    
    def test_load_nonexistent_file(self):
        """Test loading from non-existent file returns None."""
        result = load_progress(Path("/nonexistent/path.json"))
        assert result is None
    
    def test_get_default_progress(self):
        """Test default progress structure."""
        progress = get_default_progress()
        
        assert "Basic" in progress
        assert "Intermediate" in progress
        assert "Advanced" in progress
        
        for stage in progress:
            assert isinstance(progress[stage]["completed"], set)
            assert isinstance(progress[stage]["skipped"], set)
            assert isinstance(progress[stage]["times"], dict)


class TestQuestionTimes:
    """Tests for question time tracking."""
    
    def test_save_question_time_new(self):
        """Test saving time for new question."""
        progress = get_default_progress()
        progress = save_question_time(progress, "Basic", 0, 45.5)
        
        assert progress["Basic"]["times"]["0"] == 45.5
    
    def test_save_question_time_better(self):
        """Test that better time replaces old time."""
        progress = get_default_progress()
        progress = save_question_time(progress, "Basic", 0, 60.0)
        progress = save_question_time(progress, "Basic", 0, 30.0)  # Better time
        
        assert progress["Basic"]["times"]["0"] == 30.0
    
    def test_save_question_time_worse(self):
        """Test that worse time doesn't replace better time."""
        progress = get_default_progress()
        progress = save_question_time(progress, "Basic", 0, 30.0)
        progress = save_question_time(progress, "Basic", 0, 60.0)  # Worse time
        
        assert progress["Basic"]["times"]["0"] == 30.0
    
    def test_get_best_time(self):
        """Test getting best time for question."""
        progress = get_default_progress()
        progress = save_question_time(progress, "Basic", 0, 45.5)
        
        best = get_best_time(progress, "Basic", 0)
        assert best == 45.5
    
    def test_get_best_time_nonexistent(self):
        """Test getting time for unsolved question returns None."""
        progress = get_default_progress()
        best = get_best_time(progress, "Basic", 0)
        assert best is None


class TestFormatTime:
    """Tests for time formatting."""
    
    def test_format_seconds(self):
        """Test formatting seconds only."""
        assert format_time(45.0) == "45s"
        assert format_time(0.0) == "0s"
    
    def test_format_minutes_seconds(self):
        """Test formatting minutes and seconds."""
        assert format_time(90.0) == "1m 30s"
        assert format_time(125.0) == "2m 5s"
    
    def test_format_hours_minutes_seconds(self):
        """Test formatting hours, minutes, and seconds."""
        assert format_time(3661.0) == "1h 1m 1s"
        assert format_time(7200.0) == "2h 0m 0s"


class TestStats:
    """Tests for statistics calculation."""
    
    def test_get_stats_empty(self):
        """Test stats for empty progress."""
        progress = get_default_progress()
        stats = get_stats(progress)
        
        assert stats["total_completed"] == 0
        assert stats["total_skipped"] == 0
        assert stats["completion_rate"] == 0
    
    def test_get_stats_with_progress(self):
        """Test stats with some progress."""
        progress = get_default_progress()
        progress["Basic"]["completed"] = {0, 1, 2}
        progress["Basic"]["skipped"] = {3}
        progress["Basic"]["times"] = {"0": 30.0, "1": 45.0, "2": 60.0}
        
        stats = get_stats(progress)
        
        assert stats["total_completed"] == 3
        assert stats["total_skipped"] == 1
        assert stats["by_stage"]["Basic"]["completed"] == 3
        assert stats["by_stage"]["Basic"]["average_time"] == 45.0


class TestStreaks:
    """Tests for streak tracking."""
    
    def test_new_streak(self):
        """Test starting a new streak."""
        progress = get_default_progress()
        progress = update_streak(progress)
        
        assert progress["streak"]["current"] == 1
        assert progress["streak"]["max"] == 1
        assert progress["streak"]["last_active"] == datetime.now().date().isoformat()
    
    def test_streak_continuation(self):
        """Test continuing a streak."""
        progress = get_default_progress()
        yesterday = (datetime.now().date() - timedelta(days=1)).isoformat()
        
        progress["streak"] = {
            "current": 5,
            "max": 5,
            "last_active": yesterday,
            "history": [yesterday]
        }
        
        progress = update_streak(progress)
        
        assert progress["streak"]["current"] == 6
        assert progress["streak"]["max"] == 6
    
    def test_streak_break(self):
        """Test streak breaking after gap."""
        progress = get_default_progress()
        two_days_ago = (datetime.now().date() - timedelta(days=2)).isoformat()
        
        progress["streak"] = {
            "current": 10,
            "max": 10,
            "last_active": two_days_ago,
            "history": []
        }
        
        progress = update_streak(progress)
        
        assert progress["streak"]["current"] == 1  # Reset
        assert progress["streak"]["max"] == 10  # Max preserved
    
    def test_get_streak_info(self):
        """Test getting streak information."""
        progress = get_default_progress()
        progress["streak"] = {
            "current": 7,
            "max": 14,
            "last_active": datetime.now().date().isoformat(),
            "history": ["2024-01-01", "2024-01-02"]
        }
        
        info = get_streak_info(progress)
        
        assert info["current_streak"] == 7
        assert info["max_streak"] == 14
        assert info["active_days"] == 2


class TestAchievements:
    """Tests for achievement checking."""
    
    def test_first_solve_achievement(self):
        """Test first solve achievement."""
        progress = get_default_progress()
        progress["Basic"]["completed"] = {0}
        
        achievements = check_achievements(progress)
        achievement_ids = [a["id"] for a in achievements]
        
        assert "first_solve" in achievement_ids
    
    def test_multiple_achievements(self):
        """Test multiple achievements at once."""
        progress = get_default_progress()
        progress["Basic"]["completed"] = set(range(10))  # 10 problems
        
        achievements = check_achievements(progress)
        achievement_ids = [a["id"] for a in achievements]
        
        assert "first_solve" in achievement_ids
        assert "first_10" in achievement_ids
    
    def test_streak_achievement(self):
        """Test streak-based achievement."""
        progress = get_default_progress()
        progress["streak"] = {"current": 7, "max": 7, "history": []}
        
        achievements = check_achievements(progress)
        achievement_ids = [a["id"] for a in achievements]
        
        assert "streak_3" in achievement_ids
        assert "streak_7" in achievement_ids


class TestExportImport:
    """Tests for export/import functionality."""
    
    def test_export_import_roundtrip(self):
        """Test that export -> import returns equivalent progress."""
        progress = get_default_progress()
        progress["Basic"]["completed"] = {0, 1, 2}
        progress["Basic"]["times"] = {"0": 30.0, "1": 45.0, "2": 60.0}
        progress["streak"] = {"current": 5, "max": 10, "history": []}
        
        exported = export_progress(progress)
        imported = import_progress(exported)
        
        assert imported["Basic"]["completed"] == progress["Basic"]["completed"]
        assert imported["Basic"]["times"] == progress["Basic"]["times"]
        assert imported["streak"]["current"] == progress["streak"]["current"]
    
    def test_import_invalid_data(self):
        """Test importing invalid data returns None."""
        result = import_progress("invalid_base64_data!")
        assert result is None
    
    def test_merge_progress(self):
        """Test merging two progress objects."""
        existing = get_default_progress()
        existing["Basic"]["completed"] = {0, 1}
        existing["Basic"]["times"] = {"0": 60.0, "1": 30.0}
        
        imported = get_default_progress()
        imported["Basic"]["completed"] = {1, 2}
        imported["Basic"]["times"] = {"1": 45.0, "2": 50.0}
        
        merged = merge_progress(existing, imported)
        
        # Completed should be union
        assert merged["Basic"]["completed"] == {0, 1, 2}
        
        # Times should keep best
        assert merged["Basic"]["times"]["0"] == 60.0  # Only in existing
        assert merged["Basic"]["times"]["1"] == 30.0  # Best of 30 vs 45
        assert merged["Basic"]["times"]["2"] == 50.0  # Only in imported


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

