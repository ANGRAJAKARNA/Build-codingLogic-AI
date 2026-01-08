# persistence.py
"""
Data persistence module for saving and loading user progress.
Stores data in JSON format for easy debugging and portability.
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Set, Any, Optional

# Default file path for progress data
PROGRESS_FILE = Path(__file__).parent / "user_progress.json"

# Default progress structure
DEFAULT_PROGRESS = {
    "Basic": {"completed": [], "skipped": [], "times": {}},
    "Intermediate": {"completed": [], "skipped": [], "times": {}},
    "Advanced": {"completed": [], "skipped": [], "times": {}}
}


def _serialize_progress(progress: Dict) -> Dict:
    """
    Convert progress dict with sets to JSON-serializable format.
    Sets are converted to sorted lists.
    """
    serialized = {}
    for stage, data in progress.items():
        serialized[stage] = {
            "completed": sorted(list(data.get("completed", set()))),
            "skipped": sorted(list(data.get("skipped", set()))),
            "times": data.get("times", {})
        }
    return serialized


def _deserialize_progress(data: Dict) -> Dict:
    """
    Convert loaded JSON data back to progress dict with sets.
    Lists are converted to sets for completed/skipped.
    """
    progress = {}
    for stage, stage_data in data.items():
        progress[stage] = {
            "completed": set(stage_data.get("completed", [])),
            "skipped": set(stage_data.get("skipped", [])),
            "times": stage_data.get("times", {})
        }
    return progress


def save_progress(progress: Dict, file_path: Optional[Path] = None) -> bool:
    """
    Save progress to JSON file.
    
    Args:
        progress: Dict with structure {stage: {completed: set, skipped: set, times: dict}}
        file_path: Optional custom file path (uses default if not specified)
    
    Returns:
        True if save successful, False otherwise
    """
    path = file_path or PROGRESS_FILE
    
    try:
        serialized = _serialize_progress(progress)
        
        # Add metadata
        save_data = {
            "version": "1.0",
            "last_saved": datetime.now().isoformat(),
            "progress": serialized
        }
        
        # Write to file with pretty formatting
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, indent=2, ensure_ascii=False)
        
        return True
    
    except Exception as e:
        print(f"Error saving progress: {e}")
        return False


def load_progress(file_path: Optional[Path] = None) -> Optional[Dict]:
    """
    Load progress from JSON file.
    
    Args:
        file_path: Optional custom file path (uses default if not specified)
    
    Returns:
        Progress dict if file exists and is valid, None otherwise
    """
    path = file_path or PROGRESS_FILE
    
    if not path.exists():
        return None
    
    try:
        with open(path, 'r', encoding='utf-8') as f:
            save_data = json.load(f)
        
        # Handle both old and new format
        if "progress" in save_data:
            return _deserialize_progress(save_data["progress"])
        else:
            # Legacy format - direct progress data
            return _deserialize_progress(save_data)
    
    except Exception as e:
        print(f"Error loading progress: {e}")
        return None


def get_default_progress() -> Dict:
    """
    Get a fresh default progress structure with sets.
    """
    return {
        "Basic": {"completed": set(), "skipped": set(), "times": {}},
        "Intermediate": {"completed": set(), "skipped": set(), "times": {}},
        "Advanced": {"completed": set(), "skipped": set(), "times": {}}
    }


def save_question_time(
    progress: Dict,
    stage: str,
    question_index: int,
    time_seconds: float
) -> Dict:
    """
    Save completion time for a question.
    Only saves if it's a new best time.
    
    Args:
        progress: Current progress dict
        stage: Difficulty level (Basic/Intermediate/Advanced)
        question_index: Question index (0-based)
        time_seconds: Time taken in seconds
    
    Returns:
        Updated progress dict
    """
    key = str(question_index)
    current_best = progress[stage]["times"].get(key)
    
    if current_best is None or time_seconds < current_best:
        progress[stage]["times"][key] = round(time_seconds, 2)
    
    return progress


def get_best_time(progress: Dict, stage: str, question_index: int) -> Optional[float]:
    """
    Get the best completion time for a question.
    
    Returns:
        Time in seconds if exists, None otherwise
    """
    return progress[stage]["times"].get(str(question_index))


def format_time(seconds: float) -> str:
    """
    Format seconds into human-readable string.
    
    Examples:
        45.5 -> "45s"
        90.0 -> "1m 30s"
        3661.0 -> "1h 1m 1s"
    """
    if seconds < 60:
        return f"{int(seconds)}s"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes}m {secs}s"
    else:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        return f"{hours}h {minutes}m {secs}s"


def get_stats(progress: Dict) -> Dict[str, Any]:
    """
    Calculate overall statistics from progress.
    
    Returns:
        Dict with total_completed, total_skipped, total_questions,
        completion_rate, and per-stage stats.
    """
    stats = {
        "total_completed": 0,
        "total_skipped": 0,
        "total_questions": 0,
        "by_stage": {}
    }
    
    # Get actual question counts dynamically from questions module
    try:
        from questions import QUESTIONS
        question_counts = {stage: len(questions) for stage, questions in QUESTIONS.items()}
    except ImportError:
        # Fallback to defaults if questions module not available
        question_counts = {"Basic": 30, "Intermediate": 25, "Advanced": 20}
    
    for stage, data in progress.items():
        completed = len(data.get("completed", set()))
        skipped = len(data.get("skipped", set()))
        total = question_counts.get(stage, 10)
        times = data.get("times", {})
        
        stats["total_completed"] += completed
        stats["total_skipped"] += skipped
        stats["total_questions"] += total
        
        # Calculate average time for completed questions
        if times:
            avg_time = sum(times.values()) / len(times)
        else:
            avg_time = None
        
        stats["by_stage"][stage] = {
            "completed": completed,
            "skipped": skipped,
            "total": total,
            "completion_rate": (completed / total * 100) if total > 0 else 0,
            "average_time": avg_time,
            "best_times": times
        }
    
    # Overall completion rate
    if stats["total_questions"] > 0:
        stats["completion_rate"] = (stats["total_completed"] / stats["total_questions"]) * 100
    else:
        stats["completion_rate"] = 0
    
    return stats


def reset_progress(stage: Optional[str] = None, file_path: Optional[Path] = None) -> Dict:
    """
    Reset progress for a specific stage or all stages.
    
    Args:
        stage: Stage to reset (None = reset all)
        file_path: Optional custom file path
    
    Returns:
        Fresh progress dict
    """
    if stage:
        # Reset only specific stage
        progress = load_progress(file_path) or get_default_progress()
        progress[stage] = {"completed": set(), "skipped": set(), "times": {}}
    else:
        # Reset everything
        progress = get_default_progress()
    
    save_progress(progress, file_path)
    return progress


def delete_progress_file(file_path: Optional[Path] = None) -> bool:
    """
    Delete the progress file entirely.
    
    Returns:
        True if deleted successfully, False otherwise
    """
    path = file_path or PROGRESS_FILE
    
    try:
        if path.exists():
            path.unlink()
        return True
    except Exception as e:
        print(f"Error deleting progress file: {e}")
        return False

