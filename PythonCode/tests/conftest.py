# tests/conftest.py
"""
Pytest configuration and shared fixtures.
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture
def default_progress():
    """Provide default progress structure."""
    from persistence import get_default_progress
    return get_default_progress()


@pytest.fixture
def sample_progress():
    """Provide sample progress with some data."""
    return {
        "Basic": {
            "completed": {0, 1, 2, 3, 4},
            "skipped": {5},
            "times": {"0": 30.0, "1": 45.0, "2": 60.0, "3": 25.0, "4": 55.0}
        },
        "Intermediate": {
            "completed": {0, 1},
            "skipped": set(),
            "times": {"0": 120.0, "1": 180.0}
        },
        "Advanced": {
            "completed": set(),
            "skipped": set(),
            "times": {}
        }
    }


@pytest.fixture
def simple_code():
    """Provide simple addition code."""
    return "def add(a, b):\n    return a + b"


@pytest.fixture
def simple_test_cases():
    """Provide simple test cases for addition."""
    return [((2, 3), 5), ((10, 20), 30), ((-1, 1), 0)]


@pytest.fixture
def interview_engine():
    """Provide configured interview engine."""
    from interview_engine import create_interview_engine
    return create_interview_engine(
        difficulty="mid",
        interview_type="technical",
        time_limit=30
    )

