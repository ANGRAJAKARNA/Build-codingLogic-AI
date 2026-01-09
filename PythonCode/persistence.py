# persistence.py
"""
Data persistence module for saving and loading user progress.
Stores data in JSON format for easy debugging and portability.
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Set, Any, Optional, List

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


# =============================================================================
# INTERVIEW HISTORY PERSISTENCE
# =============================================================================

INTERVIEW_HISTORY_FILE = Path(__file__).parent / "interview_history.json"


def save_interview_history(result: Dict[str, Any], file_path: Optional[Path] = None) -> bool:
    """
    Save an interview result to the history file.
    
    Args:
        result: Dict containing interview result with scores, grade, etc.
        file_path: Optional custom file path
    
    Returns:
        True if save successful, False otherwise
    """
    path = file_path or INTERVIEW_HISTORY_FILE
    
    try:
        # Load existing history
        history = load_interview_history(path) or []
        
        # Add timestamp if not present
        if 'timestamp' not in result:
            result['timestamp'] = datetime.now().isoformat()
        elif isinstance(result['timestamp'], float):
            result['timestamp'] = datetime.fromtimestamp(result['timestamp']).isoformat()
        
        # Add result to history
        history.append(result)
        
        # Keep only last 100 interviews
        if len(history) > 100:
            history = history[-100:]
        
        # Save to file
        with open(path, 'w', encoding='utf-8') as f:
            json.dump({
                "version": "1.0",
                "last_updated": datetime.now().isoformat(),
                "interviews": history
            }, f, indent=2, ensure_ascii=False)
        
        return True
    
    except Exception as e:
        print(f"Error saving interview history: {e}")
        return False


def load_interview_history(file_path: Optional[Path] = None) -> Optional[list]:
    """
    Load interview history from file.
    
    Args:
        file_path: Optional custom file path
    
    Returns:
        List of interview results if file exists, None otherwise
    """
    path = file_path or INTERVIEW_HISTORY_FILE
    
    if not path.exists():
        return None
    
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if "interviews" in data:
            return data["interviews"]
        else:
            # Legacy format - direct list
            return data
    
    except Exception as e:
        print(f"Error loading interview history: {e}")
        return None


def get_interview_stats() -> Dict[str, Any]:
    """
    Calculate statistics from interview history.
    
    Returns:
        Dict with interview statistics including average scores,
        improvement trends, and breakdown by difficulty/type.
    """
    history = load_interview_history() or []
    
    if not history:
        return {
            "total_interviews": 0,
            "average_score": 0,
            "best_score": 0,
            "improvement_trend": 0,
            "by_difficulty": {},
            "by_type": {},
            "recent_grades": [],
        }
    
    # Calculate basic stats
    scores = [h.get('scores', {}).get('total', 0) for h in history]
    grades = [h.get('grade', 'N/A') for h in history]
    
    # Group by difficulty
    by_difficulty = {}
    for h in history:
        diff = h.get('difficulty', 'unknown')
        if diff not in by_difficulty:
            by_difficulty[diff] = {'count': 0, 'total_score': 0, 'scores': []}
        by_difficulty[diff]['count'] += 1
        score = h.get('scores', {}).get('total', 0)
        by_difficulty[diff]['total_score'] += score
        by_difficulty[diff]['scores'].append(score)
    
    for diff in by_difficulty:
        count = by_difficulty[diff]['count']
        by_difficulty[diff]['average'] = by_difficulty[diff]['total_score'] / count if count > 0 else 0
    
    # Group by type
    by_type = {}
    for h in history:
        itype = h.get('interview_type', 'unknown')
        if itype not in by_type:
            by_type[itype] = {'count': 0, 'total_score': 0}
        by_type[itype]['count'] += 1
        by_type[itype]['total_score'] += h.get('scores', {}).get('total', 0)
    
    for itype in by_type:
        count = by_type[itype]['count']
        by_type[itype]['average'] = by_type[itype]['total_score'] / count if count > 0 else 0
    
    # Calculate improvement trend (last 5 vs previous 5)
    improvement_trend = 0
    if len(scores) >= 10:
        recent_avg = sum(scores[-5:]) / 5
        previous_avg = sum(scores[-10:-5]) / 5
        improvement_trend = recent_avg - previous_avg
    elif len(scores) >= 4:
        half = len(scores) // 2
        recent_avg = sum(scores[half:]) / len(scores[half:])
        previous_avg = sum(scores[:half]) / half
        improvement_trend = recent_avg - previous_avg
    
    # Score breakdown averages
    score_categories = ['problem_solving', 'communication', 'code_quality', 'complexity_analysis']
    category_averages = {}
    for cat in score_categories:
        cat_scores = [h.get('scores', {}).get(cat, 0) for h in history]
        category_averages[cat] = sum(cat_scores) / len(cat_scores) if cat_scores else 0
    
    return {
        "total_interviews": len(history),
        "average_score": sum(scores) / len(scores) if scores else 0,
        "best_score": max(scores) if scores else 0,
        "improvement_trend": improvement_trend,
        "by_difficulty": by_difficulty,
        "by_type": by_type,
        "recent_grades": grades[-10:],
        "category_averages": category_averages,
    }


def get_recent_interviews(count: int = 5) -> list:
    """
    Get the most recent interview results.
    
    Args:
        count: Number of recent interviews to return
    
    Returns:
        List of recent interview results (newest first)
    """
    history = load_interview_history() or []
    return list(reversed(history[-count:]))


def clear_interview_history(file_path: Optional[Path] = None) -> bool:
    """
    Clear all interview history.
    
    Returns:
        True if cleared successfully, False otherwise
    """
    path = file_path or INTERVIEW_HISTORY_FILE
    
    try:
        if path.exists():
            path.unlink()
        return True
    except Exception as e:
        print(f"Error clearing interview history: {e}")
        return False


# =============================================================================
# STREAKS & ACHIEVEMENTS SYSTEM
# =============================================================================

# Achievement definitions
ACHIEVEMENTS = {
    # First milestones
    "first_solve": {
        "name": "First Blood",
        "description": "Solve your first problem",
        "icon": "🩸",
        "category": "milestone",
        "condition": lambda stats: stats["total_completed"] >= 1
    },
    "first_10": {
        "name": "Getting Started",
        "description": "Solve 10 problems",
        "icon": "🌱",
        "category": "milestone",
        "condition": lambda stats: stats["total_completed"] >= 10
    },
    "first_25": {
        "name": "Quarter Century",
        "description": "Solve 25 problems",
        "icon": "🎯",
        "category": "milestone",
        "condition": lambda stats: stats["total_completed"] >= 25
    },
    "first_50": {
        "name": "Half Way Hero",
        "description": "Solve 50 problems",
        "icon": "🏅",
        "category": "milestone",
        "condition": lambda stats: stats["total_completed"] >= 50
    },
    "first_100": {
        "name": "Century Club",
        "description": "Solve 100 problems",
        "icon": "💯",
        "category": "milestone",
        "condition": lambda stats: stats["total_completed"] >= 100
    },
    "completionist": {
        "name": "Completionist",
        "description": "Solve all 150 problems",
        "icon": "🏆",
        "category": "milestone",
        "condition": lambda stats: stats["total_completed"] >= 150
    },
    
    # Difficulty achievements
    "basic_master": {
        "name": "Basic Master",
        "description": "Complete all Basic problems",
        "icon": "🌟",
        "category": "difficulty",
        "condition": lambda stats: stats["by_stage"].get("Basic", {}).get("completed", 0) >= stats["by_stage"].get("Basic", {}).get("total", 60)
    },
    "intermediate_master": {
        "name": "Intermediate Master",
        "description": "Complete all Intermediate problems",
        "icon": "⭐",
        "category": "difficulty",
        "condition": lambda stats: stats["by_stage"].get("Intermediate", {}).get("completed", 0) >= stats["by_stage"].get("Intermediate", {}).get("total", 50)
    },
    "advanced_master": {
        "name": "Advanced Master",
        "description": "Complete all Advanced problems",
        "icon": "🌠",
        "category": "difficulty",
        "condition": lambda stats: stats["by_stage"].get("Advanced", {}).get("completed", 0) >= stats["by_stage"].get("Advanced", {}).get("total", 40)
    },
    
    # Streak achievements
    "streak_3": {
        "name": "On Fire",
        "description": "Maintain a 3-day streak",
        "icon": "🔥",
        "category": "streak",
        "condition": lambda stats: stats.get("current_streak", 0) >= 3
    },
    "streak_7": {
        "name": "Week Warrior",
        "description": "Maintain a 7-day streak",
        "icon": "⚔️",
        "category": "streak",
        "condition": lambda stats: stats.get("current_streak", 0) >= 7
    },
    "streak_14": {
        "name": "Fortnight Fighter",
        "description": "Maintain a 14-day streak",
        "icon": "🛡️",
        "category": "streak",
        "condition": lambda stats: stats.get("current_streak", 0) >= 14
    },
    "streak_30": {
        "name": "Monthly Master",
        "description": "Maintain a 30-day streak",
        "icon": "👑",
        "category": "streak",
        "condition": lambda stats: stats.get("current_streak", 0) >= 30
    },
    
    # Speed achievements
    "speed_demon": {
        "name": "Speed Demon",
        "description": "Solve a problem in under 30 seconds",
        "icon": "⚡",
        "category": "speed",
        "condition": lambda stats: any(t < 30 for times in stats.get("all_times", {}).values() for t in times.values())
    },
    "lightning_fast": {
        "name": "Lightning Fast",
        "description": "Solve 5 problems in under 1 minute each",
        "icon": "💨",
        "category": "speed",
        "condition": lambda stats: sum(1 for times in stats.get("all_times", {}).values() for t in times.values() if t < 60) >= 5
    },
    
    # Special achievements
    "no_hints": {
        "name": "Self Reliant",
        "description": "Solve 10 problems without using hints",
        "icon": "🧠",
        "category": "special",
        "condition": lambda stats: stats.get("solved_without_hints", 0) >= 10
    },
    "comeback_kid": {
        "name": "Comeback Kid",
        "description": "Return after a break and solve a problem",
        "icon": "🔄",
        "category": "special",
        "condition": lambda stats: stats.get("comeback", False)
    },
    "night_owl": {
        "name": "Night Owl",
        "description": "Solve a problem between midnight and 5 AM",
        "icon": "🦉",
        "category": "special",
        "condition": lambda stats: stats.get("night_solve", False)
    },
    "early_bird": {
        "name": "Early Bird",
        "description": "Solve a problem between 5 AM and 7 AM",
        "icon": "🐦",
        "category": "special",
        "condition": lambda stats: stats.get("early_solve", False)
    },
}


def update_streak(progress: Dict) -> Dict:
    """
    Update daily coding streak.
    
    Args:
        progress: Current progress dict
        
    Returns:
        Updated progress with streak info
    """
    from datetime import timedelta
    
    today = datetime.now().date().isoformat()
    yesterday = (datetime.now().date() - timedelta(days=1)).isoformat()
    
    # Initialize streak fields if not present
    if "streak" not in progress:
        progress["streak"] = {
            "current": 0,
            "max": 0,
            "last_active": None,
            "history": []  # Track last 30 days
        }
    
    streak = progress["streak"]
    last_active = streak.get("last_active")
    
    if last_active == today:
        # Already active today, no change
        pass
    elif last_active == yesterday:
        # Continuing streak
        streak["current"] = streak.get("current", 0) + 1
        streak["last_active"] = today
    else:
        # Streak broken or first day
        if last_active and streak.get("current", 0) > 0:
            # Was a break - mark comeback
            progress["comeback"] = True
        streak["current"] = 1
        streak["last_active"] = today
    
    # Update max streak
    streak["max"] = max(streak.get("max", 0), streak.get("current", 0))
    
    # Track history (last 30 days of activity)
    history = streak.get("history", [])
    if today not in history:
        history.append(today)
        # Keep only last 30 days
        history = history[-30:]
        streak["history"] = history
    
    progress["streak"] = streak
    return progress


def get_streak_info(progress: Dict) -> Dict[str, Any]:
    """
    Get formatted streak information.
    
    Returns:
        Dict with current streak, max streak, and activity calendar
    """
    streak = progress.get("streak", {"current": 0, "max": 0, "history": []})
    
    return {
        "current_streak": streak.get("current", 0),
        "max_streak": streak.get("max", 0),
        "last_active": streak.get("last_active"),
        "active_days": len(streak.get("history", [])),
        "history": streak.get("history", [])
    }


def check_achievements(progress: Dict) -> List[Dict]:
    """
    Check which achievements have been unlocked.
    
    Args:
        progress: Current progress dict
        
    Returns:
        List of unlocked achievement dicts
    """
    stats = get_stats(progress)
    
    # Add streak info to stats
    streak_info = get_streak_info(progress)
    stats["current_streak"] = streak_info["current_streak"]
    stats["max_streak"] = streak_info["max_streak"]
    
    # Add all times for speed achievements
    stats["all_times"] = {stage: data.get("times", {}) for stage, data in progress.items() if isinstance(data, dict) and "times" in data}
    
    # Add special flags
    stats["solved_without_hints"] = progress.get("solved_without_hints", 0)
    stats["comeback"] = progress.get("comeback", False)
    stats["night_solve"] = progress.get("night_solve", False)
    stats["early_solve"] = progress.get("early_solve", False)
    
    unlocked = []
    for ach_id, ach in ACHIEVEMENTS.items():
        try:
            if ach["condition"](stats):
                unlocked.append({
                    "id": ach_id,
                    "name": ach["name"],
                    "description": ach["description"],
                    "icon": ach["icon"],
                    "category": ach["category"]
                })
        except Exception:
            pass  # Skip achievements that fail to evaluate
    
    return unlocked


def get_new_achievements(progress: Dict, old_achievements: List[str]) -> List[Dict]:
    """
    Check for newly unlocked achievements.
    
    Args:
        progress: Current progress dict
        old_achievements: List of previously unlocked achievement IDs
        
    Returns:
        List of newly unlocked achievement dicts
    """
    current = check_achievements(progress)
    current_ids = set(a["id"] for a in current)
    old_ids = set(old_achievements)
    
    new_ids = current_ids - old_ids
    return [a for a in current if a["id"] in new_ids]


def save_achievement_progress(progress: Dict, file_path: Optional[Path] = None) -> bool:
    """
    Save which achievements have been unlocked to avoid re-notifying.
    """
    unlocked = check_achievements(progress)
    unlocked_ids = [a["id"] for a in unlocked]
    
    if "unlocked_achievements" not in progress:
        progress["unlocked_achievements"] = []
    
    progress["unlocked_achievements"] = unlocked_ids
    return save_progress(progress, file_path)


def record_solve(progress: Dict, used_hint: bool = False) -> Dict:
    """
    Record a successful solve with metadata for achievements.
    
    Args:
        progress: Current progress dict
        used_hint: Whether hints were used
        
    Returns:
        Updated progress dict
    """
    # Update streak
    progress = update_streak(progress)
    
    # Track hint-free solves
    if not used_hint:
        progress["solved_without_hints"] = progress.get("solved_without_hints", 0) + 1
    
    # Check time of day for special achievements
    current_hour = datetime.now().hour
    if 0 <= current_hour < 5:
        progress["night_solve"] = True
    elif 5 <= current_hour < 7:
        progress["early_solve"] = True
    
    return progress


# =============================================================================
# EXPORT/IMPORT PROGRESS
# =============================================================================

def export_progress(progress: Dict, include_achievements: bool = True) -> str:
    """
    Export progress as base64 encoded JSON for sharing/backup.
    
    Args:
        progress: Progress dict to export
        include_achievements: Whether to include achievement data
        
    Returns:
        Base64 encoded string that can be shared
    """
    import base64
    import zlib
    
    export_data = {
        "version": "2.0",
        "exported_at": datetime.now().isoformat(),
        "progress": _serialize_progress(progress)
    }
    
    if include_achievements:
        export_data["streak"] = progress.get("streak", {})
        export_data["achievements"] = progress.get("unlocked_achievements", [])
        export_data["solved_without_hints"] = progress.get("solved_without_hints", 0)
    
    # Serialize, compress, and encode
    json_str = json.dumps(export_data, separators=(',', ':'))
    compressed = zlib.compress(json_str.encode('utf-8'))
    encoded = base64.b64encode(compressed).decode('ascii')
    
    return encoded


def import_progress(encoded: str, merge_with_existing: bool = False) -> Optional[Dict]:
    """
    Import progress from base64 encoded string.
    
    Args:
        encoded: Base64 encoded progress string
        merge_with_existing: If True, merge with existing progress (keep best times)
        
    Returns:
        Progress dict if valid, None otherwise
    """
    import base64
    import zlib
    
    try:
        # Decode and decompress
        compressed = base64.b64decode(encoded.encode('ascii'))
        json_str = zlib.decompress(compressed).decode('utf-8')
        data = json.loads(json_str)
        
        # Validate version
        version = data.get("version", "1.0")
        if not version.startswith(("1.", "2.")):
            return None
        
        # Extract progress
        imported = _deserialize_progress(data.get("progress", {}))
        
        # Restore additional data
        if "streak" in data:
            imported["streak"] = data["streak"]
        if "achievements" in data:
            imported["unlocked_achievements"] = data["achievements"]
        if "solved_without_hints" in data:
            imported["solved_without_hints"] = data["solved_without_hints"]
        
        if merge_with_existing:
            existing = load_progress()
            if existing:
                imported = merge_progress(existing, imported)
        
        return imported
    
    except Exception as e:
        print(f"Error importing progress: {e}")
        return None


def merge_progress(existing: Dict, imported: Dict) -> Dict:
    """
    Merge two progress dicts, keeping best times and combining completed sets.
    
    Args:
        existing: Existing progress
        imported: Imported progress to merge
        
    Returns:
        Merged progress dict
    """
    merged = {}
    
    for stage in ["Basic", "Intermediate", "Advanced"]:
        ex_data = existing.get(stage, {"completed": set(), "skipped": set(), "times": {}})
        im_data = imported.get(stage, {"completed": set(), "skipped": set(), "times": {}})
        
        # Combine completed (union)
        merged_completed = set(ex_data.get("completed", set())) | set(im_data.get("completed", set()))
        
        # Combine skipped (remove those now completed)
        merged_skipped = (set(ex_data.get("skipped", set())) | set(im_data.get("skipped", set()))) - merged_completed
        
        # Merge times (keep best)
        merged_times = {}
        all_keys = set(ex_data.get("times", {}).keys()) | set(im_data.get("times", {}).keys())
        for key in all_keys:
            ex_time = ex_data.get("times", {}).get(key)
            im_time = im_data.get("times", {}).get(key)
            if ex_time is not None and im_time is not None:
                merged_times[key] = min(ex_time, im_time)
            else:
                merged_times[key] = ex_time if ex_time is not None else im_time
        
        merged[stage] = {
            "completed": merged_completed,
            "skipped": merged_skipped,
            "times": merged_times
        }
    
    # Merge streak (keep better)
    ex_streak = existing.get("streak", {"current": 0, "max": 0})
    im_streak = imported.get("streak", {"current": 0, "max": 0})
    merged["streak"] = {
        "current": max(ex_streak.get("current", 0), im_streak.get("current", 0)),
        "max": max(ex_streak.get("max", 0), im_streak.get("max", 0)),
        "last_active": ex_streak.get("last_active") or im_streak.get("last_active"),
        "history": list(set(ex_streak.get("history", []) + im_streak.get("history", [])))[-30:]
    }
    
    # Merge achievements (union)
    ex_ach = set(existing.get("unlocked_achievements", []))
    im_ach = set(imported.get("unlocked_achievements", []))
    merged["unlocked_achievements"] = list(ex_ach | im_ach)
    
    # Keep max solved_without_hints
    merged["solved_without_hints"] = max(
        existing.get("solved_without_hints", 0),
        imported.get("solved_without_hints", 0)
    )
    
    return merged


def create_backup(progress: Dict, backup_dir: Optional[Path] = None) -> Optional[Path]:
    """
    Create a timestamped backup of progress.
    
    Args:
        progress: Progress to backup
        backup_dir: Directory for backups (default: ./backups)
        
    Returns:
        Path to backup file if successful, None otherwise
    """
    if backup_dir is None:
        backup_dir = Path(__file__).parent / "backups"
    
    try:
        backup_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = backup_dir / f"progress_backup_{timestamp}.json"
        
        save_progress(progress, backup_file)
        
        # Keep only last 10 backups
        backups = sorted(backup_dir.glob("progress_backup_*.json"))
        for old_backup in backups[:-10]:
            old_backup.unlink()
        
        return backup_file
    
    except Exception as e:
        print(f"Error creating backup: {e}")
        return None


def restore_from_backup(backup_file: Path) -> Optional[Dict]:
    """
    Restore progress from a backup file.
    
    Args:
        backup_file: Path to backup file
        
    Returns:
        Restored progress dict if successful, None otherwise
    """
    return load_progress(backup_file)


def list_backups(backup_dir: Optional[Path] = None) -> List[Dict]:
    """
    List available backup files.
    
    Args:
        backup_dir: Directory to search (default: ./backups)
        
    Returns:
        List of backup info dicts with path, date, and size
    """
    if backup_dir is None:
        backup_dir = Path(__file__).parent / "backups"
    
    if not backup_dir.exists():
        return []
    
    backups = []
    for f in sorted(backup_dir.glob("progress_backup_*.json"), reverse=True):
        try:
            stat = f.stat()
            backups.append({
                "path": f,
                "filename": f.name,
                "date": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "size_kb": round(stat.st_size / 1024, 2)
            })
        except Exception:
            pass
    
    return backups
