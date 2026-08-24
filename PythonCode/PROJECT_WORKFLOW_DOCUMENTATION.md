# 🤖 PyCode AI - Complete Project Workflow Documentation

**Intelligent Python Learning Platform**  
**Version:** 2.0 | **Last Updated:** January 2026  
**Author:** Naveen Kumar Yellared

---

## 📋 Table of Contents

1. [Project Overview](#1-project-overview)
2. [Architecture Overview](#2-architecture-overview)
3. [Module Deep Dive](#3-module-deep-dive)
4. [Data Flow & Workflows](#4-data-flow--workflows)
5. [Feature Workflows](#5-feature-workflows)
6. [Technical Implementation Details](#6-technical-implementation-details)
7. [Configuration & Environment](#7-configuration--environment)
8. [Security Architecture](#8-security-architecture)
9. [Testing Framework](#9-testing-framework)
10. [Deployment & Usage](#10-deployment--usage)

---

## 1. Project Overview

### 1.1 What is PyCode AI?

PyCode AI is an **AI-powered interactive learning platform** for Python programming, test automation, Linux administration, and infrastructure concepts. It provides a comprehensive learning experience through:

- **Practice Mode**: 150+ coding challenges with instant feedback
- **Interview Mode**: Realistic mock technical interviews with voice support
- **AI Chat Assistant**: 175+ concepts with detailed explanations
- **Progress Tracking**: Streaks, achievements, and performance analytics

### 1.2 Technology Stack Summary

| Layer | Technologies |
|-------|-------------|
| **Frontend** | Streamlit 1.28+ |
| **Backend** | Python 3.9+ |
| **AI Services** | Groq API (LLaMA 3.1), Local Pattern Matching |
| **Voice Features** | gTTS, pyttsx3, SpeechRecognition |
| **Code Execution** | Custom Sandbox with Threading |
| **Data Persistence** | JSON Files |
| **PDF Search** | FAISS, Sentence-Transformers |

### 1.3 Project Statistics

```
📊 Codebase Statistics
├── Total Lines of Code: 25,000+
├── Python Modules: 15+
├── Concepts Covered: 175+
├── Practice Problems: 188 (150 Python + 38 automation)
├── Test Coverage: ~90%
└── Knowledge Domains: 5
    ├── Python Core (47 concepts)
    ├── Advanced Python (15 concepts)
    ├── Test Automation (46 concepts)
    ├── Infrastructure (43 concepts)
    └── Linux Administration (24 concepts)
```

---

## 2. Architecture Overview

### 2.1 High-Level System Architecture

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                           USER INTERFACE LAYER                                │
│                          (Streamlit Web App)                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │  Practice   │  │  Interview  │  │  AI Chat    │  │  Progress   │        │
│  │   Mode      │  │    Mode     │  │  Assistant  │  │  Dashboard  │        │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘        │
└─────────┼────────────────┼────────────────┼────────────────┼─────────────────┘
          │                │                │                │
          ▼                ▼                ▼                ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                          APPLICATION LAYER                                    │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                           main.py (2391 lines)                       │   │
│  │  • UI Rendering & Routing                                            │   │
│  │  • Session State Management                                          │   │
│  │  • Mode Switching Logic                                              │   │
│  │  • Event Handling                                                    │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  ┌───────────────┐  ┌────────────────┐  ┌─────────────────┐                │
│  │   questions   │  │ interview_     │  │ builtin_        │                │
│  │   .py         │  │ engine.py      │  │ assistant.py    │                │
│  │ (150+ Probs)  │  │ (Interview AI) │  │ (175+ Concepts) │                │
│  └───────┬───────┘  └───────┬────────┘  └────────┬────────┘                │
└──────────┼──────────────────┼─────────────────────┼──────────────────────────┘
           │                  │                     │
           ▼                  ▼                     ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                           CORE SERVICES LAYER                                 │
│                                                                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │  evaluator  │  │  ai_service │  │ voice_      │  │ persistence │        │
│  │  .py        │  │  .py        │  │ engine.py   │  │ .py         │        │
│  │ (Sandbox)   │  │ (Groq API)  │  │ (TTS/STT)   │  │ (Storage)   │        │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘        │
└─────────┼────────────────┼────────────────┼────────────────┼─────────────────┘
          │                │                │                │
          ▼                ▼                ▼                ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                            DATA LAYER                                         │
│                                                                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │ progress    │  │ interview   │  │ chat_       │  │ PDF         │        │
│  │ .json       │  │ _history    │  │ memory      │  │ Knowledge   │        │
│  │             │  │ .json       │  │ .json       │  │ Base        │        │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 2.2 File Structure & Responsibilities

```
PythonCode/
│
├── 📄 main.py                      # Main Streamlit application (Entry Point)
│   └── Responsibilities:
│       ├── UI layout & styling (Futuristic Neon Cyber Design)
│       ├── Session state management
│       ├── Mode routing (Practice/Interview/Chat)
│       └── User interaction handling
│
├── 🤖 builtin_assistant.py          # AI Chat Engine (8175 lines)
│   └── Responsibilities:
│       ├── 175+ concept explanations
│       ├── Pattern matching for queries
│       ├── Comparison engine (list vs tuple, etc.)
│       ├── Learning memory integration
│       └── Groq API fallback
│
├── 🔒 evaluator.py                  # Code Execution Sandbox (431 lines)
│   └── Responsibilities:
│       ├── Security validation
│       ├── Sandboxed code execution
│       ├── Timeout protection (5 seconds)
│       └── Error message formatting
│
├── 🎤 interview_engine.py           # Mock Interview System (1010 lines)
│   └── Responsibilities:
│       ├── Interview state machine (8 stages)
│       ├── Response analysis & scoring
│       ├── Stage transitions
│       └── Feedback generation
│
├── 🎙️ voice_engine.py               # Voice Features (627 lines)
│   └── Responsibilities:
│       ├── Text-to-Speech (gTTS/pyttsx3)
│       ├── Speech-to-Text
│       ├── Voice interview scripts
│       └── Audio player generation
│
├── 🌐 ai_service.py                 # Groq API Integration (517 lines)
│   └── Responsibilities:
│       ├── API client management
│       ├── Response caching
│       ├── Rate limiting
│       └── Prompt execution
│
├── 💾 persistence.py                # Data Storage (1041 lines)
│   └── Responsibilities:
│       ├── Progress save/load
│       ├── Interview history
│       ├── Streak tracking
│       ├── Achievement system
│       └── Export/Import functionality
│
├── 📝 prompts.py                    # AI Prompt Templates (576 lines)
│   └── Responsibilities:
│       ├── Code review prompts
│       ├── Interview stage prompts
│       ├── Hint generation prompts
│       └── Behavioral question banks
│
├── 📚 questions.py                  # Practice Question Bank
│   └── Contains 150+ questions with:
│       ├── Problem descriptions
│       ├── Test cases
│       ├── Progressive hints
│       ├── Solutions
│       └── Complexity analysis
│
├── 🔧 automation_concepts.py        # Selenium/Robot Framework Concepts
├── 🖥️ infrastructure_concepts.py    # Networking/Server Concepts
├── 🐧 linux_concepts.py             # Linux Administration Concepts
├── 📈 advanced_concepts.py          # Modern Python 3.7+ Concepts
│
├── 🧠 learning_memory.py            # Self-Learning Module
│   └── Tracks user interactions for personalized responses
│
├── 📄 pdf_knowledge_base.py         # PDF Search Integration
│   └── FAISS vector search on PDF documents
│
├── assistant/                       # Helper Modules
│   ├── code_analyzer.py             # Code analysis utilities
│   ├── helpers.py                   # Common helper functions
│   ├── python_concepts.py           # Python concept definitions
│   └── response_generator.py        # Response formatting
│
├── tests/                           # Test Suite
│   ├── conftest.py                  # Pytest fixtures
│   ├── test_evaluator.py            # Evaluator tests
│   ├── test_persistence.py          # Persistence tests
│   └── test_interview_engine.py     # Interview tests
│
├── TextBooks/                       # PDF Knowledge Base
│   └── python-crash-course.pdf
│
└── Data Files
    ├── user_progress.json           # User progress data
    ├── interview_history.json       # Interview records
    └── chat_memory.json             # Conversation history
```

---

## 3. Module Deep Dive

### 3.1 main.py - The Application Hub

The main module serves as the central orchestrator for the entire application.

#### Session State Variables

```python
# Core state variables managed by main.py
st.session_state.stage          # Current difficulty level
st.session_state.q_index        # Current question index
st.session_state.progress       # User progress dictionary
st.session_state.timer_start    # Challenge start time
st.session_state.passed         # Whether current question is solved
st.session_state.chat_history   # AI chat conversation
st.session_state.show_chat      # Whether chat modal is open
st.session_state.interview_active   # Interview in progress flag
st.session_state.interview_engine   # Interview engine instance
```

#### UI Components Flow

```
┌─────────────────────────────────────────────────────────────┐
│                        HEADER BAR                            │
│   [PyCode AI Logo] [Practice] [Interview] [Chat] [Stats]    │
└─────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
┌───────────────────┐ ┌─────────────┐ ┌─────────────────────┐
│   PRACTICE MODE   │ │ INTERVIEW   │ │    AI CHAT MODE     │
│                   │ │    MODE     │ │                     │
│ ┌───────────────┐ │ │             │ │ ┌─────────────────┐ │
│ │ Problem Panel │ │ │ ┌─────────┐ │ │ │ Category Select │ │
│ │ • Difficulty  │ │ │ │ Stage   │ │ │ │ • Python        │ │
│ │ • Question    │ │ │ │ Progress│ │ │ │ • Selenium      │ │
│ │ • Test Cases  │ │ │ │ Indicator│ │ │ │ • Robot         │ │
│ │ • Hints       │ │ │ └─────────┘ │ │ │ • Infrastructure│ │
│ └───────────────┘ │ │             │ │ └─────────────────┘ │
│                   │ │ ┌─────────┐ │ │                     │
│ ┌───────────────┐ │ │ │ Chat    │ │ │ ┌─────────────────┐ │
│ │ Code Editor   │ │ │ │ Area    │ │ │ │ Chat Messages   │ │
│ │ • Syntax HL   │ │ │ │ + Voice │ │ │ │ • User Q        │ │
│ │ • Run/Submit  │ │ │ └─────────┘ │ │ │ • AI Response   │ │
│ │ • Results     │ │ │             │ │ │ • Code Blocks   │ │
│ └───────────────┘ │ │ ┌─────────┐ │ │ └─────────────────┘ │
│                   │ │ │Code Area│ │ │                     │
│                   │ │ └─────────┘ │ │ ┌─────────────────┐ │
│                   │ │             │ │ │ Input + Prompts │ │
│                   │ │ ┌─────────┐ │ │ └─────────────────┘ │
│                   │ │ │ Score   │ │ │                     │
│                   │ │ │ Feedback│ │ │                     │
│                   │ │ └─────────┘ │ │                     │
└───────────────────┘ └─────────────┘ └─────────────────────┘
```

### 3.2 evaluator.py - Secure Code Execution

#### Security Layers

```
┌──────────────────────────────────────────────────────────┐
│                    USER CODE INPUT                        │
└───────────────────────────┬──────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────┐
│              LAYER 1: PATTERN DETECTION                   │
│                                                          │
│  Blocked Patterns:                                       │
│  • import os, sys, subprocess                           │
│  • open(), eval(), exec()                               │
│  • __import__(), compile()                              │
│  • __class__, __bases__, __globals__                    │
│                                                          │
│  → Returns: (is_safe: bool, error_msg: str)             │
└───────────────────────────┬──────────────────────────────┘
                            │ ✅ PASS
                            ▼
┌──────────────────────────────────────────────────────────┐
│            LAYER 2: RESTRICTED BUILTINS                   │
│                                                          │
│  SAFE_BUILTINS = {                                       │
│    # Types: int, str, list, dict, set, tuple, ...       │
│    # Functions: len, max, min, sum, range, ...          │
│    # Modules: math, collections, heapq, itertools, ...  │
│    # Exceptions: ValueError, TypeError, ...             │
│  }                                                       │
│                                                          │
│  Blocked: open, eval, exec, __import__                  │
└───────────────────────────┬──────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────┐
│             LAYER 3: TIMEOUT PROTECTION                   │
│                                                          │
│  def run_with_timeout(func, args, timeout=5):           │
│      thread = Thread(target=func, args=args)            │
│      thread.start()                                      │
│      thread.join(timeout)                                │
│      if thread.is_alive():                              │
│          return TIMEOUT_ERROR                            │
│                                                          │
│  → Prevents infinite loops                               │
└───────────────────────────┬──────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────┐
│              TEST CASE EXECUTION                          │
│                                                          │
│  for (inputs, expected) in test_cases:                  │
│      result = func(*inputs)                             │
│      if result != expected:                             │
│          return format_test_failure(...)                │
│                                                          │
│  return "✅ All tests passed!"                           │
└──────────────────────────────────────────────────────────┘
```

### 3.3 interview_engine.py - Interview State Machine

#### Interview Stages Flow

```
┌────────────────────────────────────────────────────────────────────┐
│                    INTERVIEW STATE MACHINE                          │
│                                                                    │
│  Text Mode Flow:                                                   │
│  ┌──────┐   ┌──────────┐   ┌────────┐   ┌────────────────┐       │
│  │INTRO │ → │APPROACH  │ → │CODING  │ → │OPTIMIZATION    │       │
│  │2 min │   │5 min     │   │15 min  │   │5 min           │       │
│  └──────┘   └──────────┘   └────────┘   └────────────────┘       │
│      │                                           │                 │
│      │                                           ▼                 │
│      │                                    ┌────────────────┐       │
│      │  (If behavioral included)         │BEHAVIORAL      │       │
│      │  ─────────────────────────────────▶│5 min           │       │
│      │                                    └────────────────┘       │
│      │                                           │                 │
│      │                                           ▼                 │
│      │                                    ┌────────────────┐       │
│      └────────────────────────────────────▶│WRAPUP         │       │
│                                           │3 min           │       │
│                                           └────────────────┘       │
│                                                  │                 │
│                                                  ▼                 │
│                                           ┌────────────────┐       │
│                                           │COMPLETED       │       │
│                                           │Final Feedback  │       │
│                                           └────────────────┘       │
│                                                                    │
│  Voice Mode Additional Stages:                                     │
│  ┌──────────┐   ┌────────────┐                                    │
│  │GREETING  │ → │SELF_INTRO  │ → [Text Mode Flow]                 │
│  │Audio play│   │30 sec      │                                    │
│  └──────────┘   └────────────┘                                    │
└────────────────────────────────────────────────────────────────────┘
```

#### Scoring System

```python
@dataclass
class InterviewScores:
    problem_solving: float = 0.0      # 35% weight
    communication: float = 0.0         # 25% weight
    code_quality: float = 0.0          # 25% weight
    complexity_analysis: float = 0.0   # 15% weight
    
    def get_total(self) -> float:
        """Weighted average score calculation"""
        return (
            self.problem_solving * 0.35 +
            self.communication * 0.25 +
            self.code_quality * 0.25 +
            self.complexity_analysis * 0.15
        )
    
    def get_grade(self) -> str:
        """Letter grade based on total"""
        total = self.get_total()
        if total >= 90: return "A"    # Strong Hire
        if total >= 80: return "B"    # Hire
        if total >= 70: return "C"    # Lean Hire
        if total >= 60: return "D"    # Lean No Hire
        return "F"                     # No Hire
```

#### Response Analysis Keywords

```python
# Keywords that trigger score increases

COMPLEXITY_PATTERNS = [
    r'o\([^)]+\)',           # O(n), O(log n), etc.
    r'time complexity',
    r'space complexity', 
    r'linear', r'quadratic',
    r'logarithmic',
    r'n squared', r'n log n'
]

EDGE_CASE_PATTERNS = [
    r'edge case', r'empty',
    r'null', r'none', r'negative',
    r'zero', r'overflow', r'boundary'
]

APPROACH_PATTERNS = [
    r'approach', r'strategy',
    r'first.*then', r'step',
    r'iterate', r'traverse',
    r'algorithm', r'technique'
]
```

### 3.4 builtin_assistant.py - AI Chat Engine

#### Response Generation Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│                     USER QUERY INPUT                         │
│                   "What is a decorator?"                     │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              STEP 1: LEARNED RESPONSE CHECK                  │
│                                                             │
│  • Check learning_memory for previous Q&A                   │
│  • Check for user corrections                               │
│  • If high confidence match found → Return learned response │
└───────────────────────────┬─────────────────────────────────┘
                            │ (No match)
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              STEP 2: COMMAND DETECTION                       │
│                                                             │
│  Slash Commands:                                            │
│  • /help → Show available commands                          │
│  • /compare A B → Trigger comparison engine                 │
│  • /example topic → Get code examples                       │
│  • /hint → Context-aware hint                               │
│  • /clear → Clear chat history                              │
└───────────────────────────┬─────────────────────────────────┘
                            │ (Not a command)
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              STEP 3: COMPARISON DETECTION                    │
│                                                             │
│  Patterns: "X vs Y", "X versus Y", "compare X and Y"        │
│                                                             │
│  Available Comparisons:                                     │
│  • list vs tuple                                            │
│  • list vs dict                                             │
│  • for vs while                                             │
│  • class vs function                                        │
│  • shallow vs deep copy                                     │
│  • == vs is                                                 │
│  • append vs extend                                         │
└───────────────────────────┬─────────────────────────────────┘
                            │ (Not a comparison)
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              STEP 4: CONCEPT MATCHING                        │
│                                                             │
│  CONCEPTS dictionary with 100+ entries:                     │
│  • Python Core: list, dict, class, decorator, ...          │
│  • Advanced: async, dataclass, pathlib, ...                │
│  • Automation: selenium, robot, pytest, ...                │
│  • Infrastructure: tcp, dns, http, ...                     │
│  • Linux: systemd, bash, permissions, ...                  │
│                                                             │
│  Match Strategy:                                            │
│  1. Exact keyword match                                     │
│  2. Partial match with word boundaries                      │
│  3. Synonym expansion                                       │
└───────────────────────────┬─────────────────────────────────┘
                            │ (No local match)
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              STEP 5: GROQ API FALLBACK                       │
│                                                             │
│  If GROQ_API_KEY is set:                                    │
│  • Send query to LLaMA 3.1 70B                             │
│  • Cache response (5 min TTL)                               │
│  • Apply rate limiting (500ms between requests)             │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              STEP 6: FORMAT & STORE                          │
│                                                             │
│  • Format response with markdown                            │
│  • Add code blocks with syntax highlighting                 │
│  • Generate follow-up suggestions                           │
│  • Store Q&A in learning_memory                             │
│  • Return response to UI                                    │
└─────────────────────────────────────────────────────────────┘
```

### 3.5 persistence.py - Data Management

#### Data Structures

```python
# User Progress Structure
progress = {
    "Basic": {
        "completed": {0, 1, 2, 5, 10},  # Set of question indices
        "skipped": {3, 7},
        "times": {
            "0": 45.2,   # Seconds to solve
            "1": 67.8,
            "2": 30.1
        }
    },
    "Intermediate": { ... },
    "Advanced": { ... },
    "Automation": { ... },
    
    # Streak tracking
    "streak": {
        "current": 7,
        "max": 14,
        "last_active": "2026-01-22",
        "history": ["2026-01-15", "2026-01-16", ...]
    },
    
    # Achievements
    "unlocked_achievements": ["first_solve", "streak_3", ...],
    "solved_without_hints": 15,
    "night_solve": True,
    "early_solve": False
}

# Interview History Structure
interview_result = {
    "timestamp": "2026-01-22T10:30:00",
    "difficulty": "mid",
    "interview_type": "technical",
    "problem": "Two Sum",
    "duration_seconds": 1800,
    "scores": {
        "problem_solving": 85,
        "communication": 78,
        "code_quality": 82,
        "complexity_analysis": 70,
        "total": 79.5
    },
    "grade": "B",
    "recommendation": "Hire"
}
```

#### Achievement System

```
┌────────────────────────────────────────────────────────┐
│                  ACHIEVEMENT CATEGORIES                 │
├────────────────────────────────────────────────────────┤
│                                                        │
│  🏆 MILESTONES                                         │
│  ├── 🩸 First Blood - Solve first problem             │
│  ├── 🌱 Getting Started - Solve 10 problems           │
│  ├── 🎯 Quarter Century - Solve 25 problems           │
│  ├── 🏅 Half Way Hero - Solve 50 problems             │
│  ├── 💯 Century Club - Solve 100 problems             │
│  └── 🏆 Completionist - Solve all 150 problems        │
│                                                        │
│  ⭐ DIFFICULTY MASTERS                                 │
│  ├── 🌟 Basic Master - Complete all Basic             │
│  ├── ⭐ Intermediate Master - Complete all Intermediate│
│  └── 🌠 Advanced Master - Complete all Advanced       │
│                                                        │
│  🔥 STREAK ACHIEVEMENTS                                │
│  ├── 🔥 On Fire - 3-day streak                        │
│  ├── ⚔️ Week Warrior - 7-day streak                   │
│  ├── 🛡️ Fortnight Fighter - 14-day streak            │
│  └── 👑 Monthly Master - 30-day streak                │
│                                                        │
│  ⚡ SPEED ACHIEVEMENTS                                 │
│  ├── ⚡ Speed Demon - Solve in under 30 seconds       │
│  └── 💨 Lightning Fast - 5 problems under 1 minute    │
│                                                        │
│  🎭 SPECIAL ACHIEVEMENTS                               │
│  ├── 🧠 Self Reliant - 10 problems without hints      │
│  ├── 🔄 Comeback Kid - Return after break             │
│  ├── 🦉 Night Owl - Solve between midnight-5AM        │
│  └── 🐦 Early Bird - Solve between 5AM-7AM            │
│                                                        │
└────────────────────────────────────────────────────────┘
```

### 3.6 voice_engine.py - Voice Features

#### TTS/STT Architecture

```
┌────────────────────────────────────────────────────────────┐
│                   TEXT-TO-SPEECH FLOW                       │
│                                                            │
│  Input Text                                                │
│      │                                                     │
│      ▼                                                     │
│  ┌─────────────────────────────────────────────────┐      │
│  │        ENGINE SELECTION (AUTO MODE)              │      │
│  │                                                  │      │
│  │  1. Try gTTS (Google TTS) - Online              │      │
│  │     ├── High quality                            │      │
│  │     ├── Requires internet                       │      │
│  │     └── Returns MP3 bytes                       │      │
│  │                                                  │      │
│  │  2. Fallback to pyttsx3 - Offline               │      │
│  │     ├── Medium quality                          │      │
│  │     ├── Works without internet                  │      │
│  │     └── Uses system voices                      │      │
│  └─────────────────────────────────────────────────┘      │
│      │                                                     │
│      ▼                                                     │
│  Audio Bytes → Base64 Encode → HTML Audio Element          │
│      │                                                     │
│      ▼                                                     │
│  Streamlit st.markdown() → Browser Audio Player            │
│                                                            │
└────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────┐
│                   SPEECH-TO-TEXT FLOW                       │
│                                                            │
│  Option 1: Browser Audio Recorder                          │
│  ┌──────────────────────────────────────────────┐         │
│  │  audio-recorder-streamlit component           │         │
│  │      │                                        │         │
│  │      ▼                                        │         │
│  │  WAV Bytes → SpeechRecognition library        │         │
│  │      │                                        │         │
│  │      ▼                                        │         │
│  │  Google Speech Recognition API (free tier)    │         │
│  │      │                                        │         │
│  │      ▼                                        │         │
│  │  Transcribed Text                             │         │
│  └──────────────────────────────────────────────┘         │
│                                                            │
│  Option 2: Direct Microphone (requires PyAudio)            │
│  ┌──────────────────────────────────────────────┐         │
│  │  sr.Microphone() → sr.Recognizer.listen()     │         │
│  │      │                                        │         │
│  │      ▼                                        │         │
│  │  recognize_google() → Transcribed Text        │         │
│  └──────────────────────────────────────────────┘         │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

---

## 4. Data Flow & Workflows

### 4.1 Practice Mode Workflow

```
┌─────────────────────────────────────────────────────────────────────┐
│                    PRACTICE MODE DATA FLOW                           │
│                                                                     │
│  1. USER SELECTS DIFFICULTY                                         │
│     │                                                               │
│     ▼                                                               │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  st.session_state.stage = "Basic" | "Intermediate" | ...    │   │
│  │  questions = QUESTIONS[stage]                                │   │
│  │  Load progress for stage                                     │   │
│  └─────────────────────────────────────────────────────────────┘   │
│     │                                                               │
│     ▼                                                               │
│  2. USER SELECTS QUESTION                                           │
│     │                                                               │
│     ▼                                                               │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  st.session_state.q_index = selected_index                   │   │
│  │  st.session_state.timer_start = time.time()                  │   │
│  │  Display: question, test_cases, hints                        │   │
│  └─────────────────────────────────────────────────────────────┘   │
│     │                                                               │
│     ▼                                                               │
│  3. USER WRITES CODE                                                │
│     │                                                               │
│     ├──▶ [REQUEST HINT]                                            │
│     │    ├── Show progressive hints (1 → 2 → 3)                   │
│     │    └── If Groq available: get_smart_hint()                  │
│     │                                                               │
│     ├──▶ [RUN CODE]                                                │
│     │    │                                                         │
│     │    ▼                                                         │
│     │    ┌────────────────────────────────────────────────────┐   │
│     │    │  evaluator.evaluate_user_code(                      │   │
│     │    │      code, function_name, test_cases[:3]  # Sample  │   │
│     │    │  )                                                  │   │
│     │    │                                                      │   │
│     │    │  Returns: (passed: bool, message: str)              │   │
│     │    └────────────────────────────────────────────────────┘   │
│     │    │                                                         │
│     │    ├── If FAILED: Show error + AI bug hint                  │
│     │    └── If PASSED: Show success + "Ready to submit"          │
│     │                                                               │
│     └──▶ [SUBMIT CODE]                                             │
│          │                                                         │
│          ▼                                                         │
│          ┌────────────────────────────────────────────────────┐   │
│          │  evaluator.evaluate_user_code(                      │   │
│          │      code, function_name, ALL_test_cases            │   │
│          │  )                                                  │   │
│          │                                                      │   │
│          │  If PASSED:                                         │   │
│          │  • Calculate time taken                             │   │
│          │  • Update progress.completed.add(q_index)           │   │
│          │  • Save best time                                   │   │
│          │  • Update streak                                    │   │
│          │  • Check achievements                               │   │
│          │  • Show AI code review                              │   │
│          │  • save_progress()                                  │   │
│          └────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 4.2 Interview Mode Workflow

```
┌─────────────────────────────────────────────────────────────────────┐
│                    INTERVIEW MODE DATA FLOW                          │
│                                                                     │
│  1. INTERVIEW SETUP                                                 │
│     │                                                               │
│     ▼                                                               │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  User selects:                                               │   │
│  │  • Difficulty: Junior | Mid | Senior                        │   │
│  │  • Type: Technical | Behavioral | Mixed                     │   │
│  │  • Time limit: 30 minutes (default)                         │   │
│  │  • Mode: Text Only | Voice Enabled                          │   │
│  │                                                              │   │
│  │  engine = create_interview_engine(config)                    │   │
│  └─────────────────────────────────────────────────────────────┘   │
│     │                                                               │
│     ▼                                                               │
│  2. INTERVIEW START                                                 │
│     │                                                               │
│     ├──▶ [TEXT MODE]                                               │
│     │    ├── Show introduction message                             │
│     │    └── Start timer                                           │
│     │                                                               │
│     └──▶ [VOICE MODE]                                              │
│          ├── Play greeting audio                                   │
│          ├── Wait for user ready                                   │
│          ├── Request self-introduction (30 sec)                    │
│          ├── Analyze introduction for experience level             │
│          └── Proceed to technical portion                          │
│     │                                                               │
│     ▼                                                               │
│  3. INTERVIEW STAGES (Loop)                                         │
│     │                                                               │
│     ▼                                                               │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  For each stage:                                             │   │
│  │                                                              │   │
│  │  ┌──────────────────────────────────────────────────────┐   │   │
│  │  │  USER RESPONSE                                        │   │   │
│  │  │  • Text message via chat input                       │   │   │
│  │  │  • Code via code editor (coding stage)               │   │   │
│  │  │  • Voice via audio recorder (voice mode)             │   │   │
│  │  └──────────────────────────────────────────────────────┘   │   │
│  │           │                                                  │   │
│  │           ▼                                                  │   │
│  │  ┌──────────────────────────────────────────────────────┐   │   │
│  │  │  engine.process_response(user_message, user_code)     │   │   │
│  │  │                                                       │   │   │
│  │  │  1. Add message to conversation history               │   │   │
│  │  │  2. Analyze response for keywords                     │   │   │
│  │  │     • Complexity patterns → +score                    │   │   │
│  │  │     • Edge case mentions → +score                     │   │   │
│  │  │     • Clarifying questions → +score                   │   │   │
│  │  │  3. Evaluate code quality (if coding stage)           │   │   │
│  │  │  4. Generate stage-appropriate response               │   │   │
│  │  │  5. Check for stage transition                        │   │   │
│  │  └──────────────────────────────────────────────────────┘   │   │
│  │           │                                                  │   │
│  │           ▼                                                  │   │
│  │  ┌──────────────────────────────────────────────────────┐   │   │
│  │  │  INTERVIEWER RESPONSE                                 │   │   │
│  │  │  • Follow-up questions                               │   │   │
│  │  │  • Probing questions based on what's missing         │   │   │
│  │  │  • Hints if stuck (junior level)                     │   │   │
│  │  │  • Voice playback (voice mode)                       │   │   │
│  │  └──────────────────────────────────────────────────────┘   │   │
│  │                                                              │   │
│  │  Continue until: WRAPUP stage reached OR time expires        │   │
│  └─────────────────────────────────────────────────────────────┘   │
│     │                                                               │
│     ▼                                                               │
│  4. INTERVIEW COMPLETION                                            │
│     │                                                               │
│     ▼                                                               │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  engine._generate_final_feedback()                           │   │
│  │                                                              │   │
│  │  Output:                                                     │   │
│  │  ┌────────────────────────────────────────────────────┐     │   │
│  │  │  📊 Interview Feedback                              │     │   │
│  │  │                                                    │     │   │
│  │  │  Overall Score: 83/100 (Grade: B)                  │     │   │
│  │  │  Recommendation: Hire                              │     │   │
│  │  │                                                    │     │   │
│  │  │  Score Breakdown:                                  │     │   │
│  │  │  • Problem Solving: 85/100                        │     │   │
│  │  │  • Communication: 87/100                          │     │   │
│  │  │  • Code Quality: 82/100                           │     │   │
│  │  │  • Complexity: 78/100                             │     │   │
│  │  │                                                    │     │   │
│  │  │  Strengths:                                        │     │   │
│  │  │  ✓ Clear approach explanation                     │     │   │
│  │  │  ✓ Good edge case awareness                       │     │   │
│  │  │                                                    │     │   │
│  │  │  Areas to Improve:                                 │     │   │
│  │  │  • Practice complexity analysis                   │     │   │
│  │  │  • Ask more clarifying questions                  │     │   │
│  │  └────────────────────────────────────────────────────┘     │   │
│  │                                                              │   │
│  │  Save to interview_history.json                              │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 4.3 AI Chat Workflow

```
┌─────────────────────────────────────────────────────────────────────┐
│                      AI CHAT DATA FLOW                               │
│                                                                     │
│  USER MESSAGE: "What is a decorator in Python?"                     │
│     │                                                               │
│     ▼                                                               │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                 RESPONSE PRIORITY CHAIN                      │   │
│  │                                                              │   │
│  │  1️⃣ CHECK LEARNED RESPONSES                                  │   │
│  │     ├── Query learning_memory for similar questions          │   │
│  │     ├── Check for user corrections                           │   │
│  │     └── If confidence > 0.8 → Return learned response        │   │
│  │                                                              │   │
│  │  2️⃣ CHECK SLASH COMMANDS                                     │   │
│  │     ├── /help → Return command list                          │   │
│  │     ├── /compare X Y → Trigger comparison engine             │   │
│  │     └── /clear → Clear chat history                          │   │
│  │                                                              │   │
│  │  3️⃣ CHECK COMPARISONS                                        │   │
│  │     ├── Detect "X vs Y" pattern                              │   │
│  │     └── Lookup in TOPIC_COMPARISONS dictionary               │   │
│  │                                                              │   │
│  │  4️⃣ CHECK FOLLOW-UP CONTEXT                                  │   │
│  │     ├── "tell me more", "show example"                       │   │
│  │     └── Use conversation history for context                 │   │
│  │                                                              │   │
│  │  5️⃣ MATCH LOCAL CONCEPTS                                     │   │
│  │     ├── Search CONCEPTS dictionary (8000+ lines)             │   │
│  │     ├── Search automation_concepts                           │   │
│  │     ├── Search infrastructure_concepts                       │   │
│  │     └── Search linux_concepts                                │   │
│  │                                                              │   │
│  │  6️⃣ PDF KNOWLEDGE BASE (if available)                        │   │
│  │     ├── Vectorize query with sentence-transformers           │   │
│  │     ├── FAISS similarity search                              │   │
│  │     └── Return relevant PDF excerpts                         │   │
│  │                                                              │   │
│  │  7️⃣ GROQ API (if GROQ_API_KEY set)                           │   │
│  │     ├── Check cache (5 min TTL)                              │   │
│  │     ├── Rate limit (500ms between requests)                  │   │
│  │     ├── Send to LLaMA 3.1 70B                               │   │
│  │     └── Cache response                                       │   │
│  │                                                              │   │
│  │  8️⃣ FALLBACK RESPONSE                                        │   │
│  │     └── Generic helpful message with suggestions             │   │
│  └─────────────────────────────────────────────────────────────┘   │
│     │                                                               │
│     ▼                                                               │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                   RESPONSE FORMATTING                        │   │
│  │                                                              │   │
│  │  • Add markdown headers & formatting                         │   │
│  │  • Syntax highlight code blocks                              │   │
│  │  • Add comparison tables                                     │   │
│  │  • Include complexity information                            │   │
│  │  • Generate follow-up suggestions                            │   │
│  └─────────────────────────────────────────────────────────────┘   │
│     │                                                               │
│     ▼                                                               │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    LEARNING & STORAGE                        │   │
│  │                                                              │   │
│  │  • store_qa_interaction(question, answer, topic)             │   │
│  │  • Update conversation history                               │   │
│  │  • Detect topic for future queries                           │   │
│  └─────────────────────────────────────────────────────────────┘   │
│     │                                                               │
│     ▼                                                               │
│  RESPONSE DISPLAYED + FOLLOW-UP SUGGESTIONS                         │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  💬 [Response with formatted explanation]                    │   │
│  │                                                              │   │
│  │  Follow-ups:                                                 │   │
│  │  [Show me an example] [Common mistakes] [Best practices]     │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 5. Feature Workflows

### 5.1 Code Execution Security Flow

```
┌──────────────────────────────────────────────────────────────────┐
│                   SECURE CODE EXECUTION                           │
│                                                                  │
│  INPUT: User code string                                         │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  STEP 1: Pattern-Based Security Scan                       │ │
│  │                                                            │ │
│  │  DANGEROUS_PATTERNS = [                                    │ │
│  │      (r'\bimport\s+os\b', "os import blocked"),           │ │
│  │      (r'\bimport\s+sys\b', "sys import blocked"),         │ │
│  │      (r'\bopen\s*\(', "file operations blocked"),         │ │
│  │      (r'\beval\s*\(', "eval blocked"),                    │ │
│  │      (r'\bexec\s*\(', "exec blocked"),                    │ │
│  │      (r'\.__globals__', "__globals__ access blocked"),    │ │
│  │      ...                                                  │ │
│  │  ]                                                        │ │
│  │                                                            │ │
│  │  for pattern, message in DANGEROUS_PATTERNS:              │ │
│  │      if re.search(pattern, code):                         │ │
│  │          return False, f"🔒 Security: {message}"          │ │
│  └────────────────────────────────────────────────────────────┘ │
│                          │ PASS                                  │
│                          ▼                                       │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  STEP 2: Create Sandboxed Environment                      │ │
│  │                                                            │ │
│  │  safe_env = {'__builtins__': SAFE_BUILTINS.copy()}        │ │
│  │                                                            │ │
│  │  SAFE_BUILTINS includes:                                   │ │
│  │  ✅ Types: int, str, list, dict, set, tuple               │ │
│  │  ✅ Functions: len, max, min, sum, range, sorted          │ │
│  │  ✅ Modules: math, collections, heapq, itertools          │ │
│  │  ✅ Exceptions: ValueError, TypeError, IndexError         │ │
│  │                                                            │ │
│  │  ❌ Blocked: open, eval, exec, __import__, getattr        │ │
│  └────────────────────────────────────────────────────────────┘ │
│                          │                                       │
│                          ▼                                       │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  STEP 3: Compile & Execute                                 │ │
│  │                                                            │ │
│  │  compiled = compile(code, '<user_code>', 'exec')          │ │
│  │  exec(compiled, safe_env, safe_env)                       │ │
│  │                                                            │ │
│  │  Catches:                                                  │ │
│  │  • SyntaxError → format_syntax_error()                    │ │
│  │  • IndentationError → helpful indentation message         │ │
│  │  • Other exceptions → descriptive error                   │ │
│  └────────────────────────────────────────────────────────────┘ │
│                          │                                       │
│                          ▼                                       │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  STEP 4: Run Tests with Timeout                            │ │
│  │                                                            │ │
│  │  for (inputs, expected) in test_cases:                    │ │
│  │      result, success, error = run_with_timeout(           │ │
│  │          func, inputs, timeout=5                          │ │
│  │      )                                                     │ │
│  │                                                            │ │
│  │      if not success:                                       │ │
│  │          # Handle: timeout, runtime errors                 │ │
│  │          return False, format_runtime_error(...)          │ │
│  │                                                            │ │
│  │      if result != expected:                                │ │
│  │          return False, format_test_failure(...)           │ │
│  │                                                            │ │
│  │  return True, "✅ All tests passed!"                       │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 5.2 Progress & Achievement System

```
┌──────────────────────────────────────────────────────────────────┐
│               PROGRESS & ACHIEVEMENT TRACKING                     │
│                                                                  │
│  ON SUCCESSFUL SOLVE:                                            │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  1. Update Progress                                        │ │
│  │                                                            │ │
│  │  progress[stage]["completed"].add(q_index)                │ │
│  │  progress[stage]["times"][str(q_index)] = time_taken      │ │
│  │  progress[stage]["skipped"].discard(q_index)              │ │
│  └────────────────────────────────────────────────────────────┘ │
│                          │                                       │
│                          ▼                                       │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  2. Update Streak                                          │ │
│  │                                                            │ │
│  │  today = datetime.now().date().isoformat()                │ │
│  │  yesterday = (today - 1 day).isoformat()                  │ │
│  │                                                            │ │
│  │  if last_active == today:                                 │ │
│  │      pass  # No change                                     │ │
│  │  elif last_active == yesterday:                           │ │
│  │      streak["current"] += 1  # Continue streak            │ │
│  │  else:                                                     │ │
│  │      streak["current"] = 1  # Restart streak              │ │
│  │      if last_active: progress["comeback"] = True          │ │
│  │                                                            │ │
│  │  streak["max"] = max(streak["max"], streak["current"])    │ │
│  └────────────────────────────────────────────────────────────┘ │
│                          │                                       │
│                          ▼                                       │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  3. Check Achievements                                     │ │
│  │                                                            │ │
│  │  stats = get_stats(progress)                              │ │
│  │  old_achievements = progress.get("unlocked_achievements")  │ │
│  │  new_achievements = []                                     │ │
│  │                                                            │ │
│  │  for ach_id, ach in ACHIEVEMENTS.items():                 │ │
│  │      if ach["condition"](stats):                          │ │
│  │          if ach_id not in old_achievements:               │ │
│  │              new_achievements.append(ach)                  │ │
│  │              🎉 Show achievement notification              │ │
│  │                                                            │ │
│  │  progress["unlocked_achievements"] += new_achievement_ids  │ │
│  └────────────────────────────────────────────────────────────┘ │
│                          │                                       │
│                          ▼                                       │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  4. Record Special Achievements                            │ │
│  │                                                            │ │
│  │  if not used_hint:                                        │ │
│  │      progress["solved_without_hints"] += 1                │ │
│  │                                                            │ │
│  │  hour = datetime.now().hour                               │ │
│  │  if 0 <= hour < 5:                                        │ │
│  │      progress["night_solve"] = True  # 🦉 Night Owl       │ │
│  │  elif 5 <= hour < 7:                                      │ │
│  │      progress["early_solve"] = True  # 🐦 Early Bird      │ │
│  └────────────────────────────────────────────────────────────┘ │
│                          │                                       │
│                          ▼                                       │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  5. Save Progress                                          │ │
│  │                                                            │ │
│  │  save_progress(progress)                                  │ │
│  │  → user_progress.json                                      │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 6. Technical Implementation Details

### 6.1 Streamlit Session State Management

```python
# Session state initialization in main.py

def init_session_state():
    """Initialize all session state variables"""
    
    # Core navigation
    if 'stage' not in st.session_state:
        st.session_state.stage = "Basic"
    if 'q_index' not in st.session_state:
        st.session_state.q_index = 0
    
    # Progress tracking
    if 'progress' not in st.session_state:
        st.session_state.progress = load_progress() or get_default_progress()
    
    # Timer and challenge state
    if 'timer_start' not in st.session_state:
        st.session_state.timer_start = None
    if 'passed' not in st.session_state:
        st.session_state.passed = False
    if 'hint_count' not in st.session_state:
        st.session_state.hint_count = 0
    
    # Chat state
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'show_chat' not in st.session_state:
        st.session_state.show_chat = False
    
    # Interview state
    if 'interview_active' not in st.session_state:
        st.session_state.interview_active = False
    if 'interview_engine' not in st.session_state:
        st.session_state.interview_engine = None
    if 'interview_conversation' not in st.session_state:
        st.session_state.interview_conversation = []
    
    # Voice mode state
    if 'voice_mode' not in st.session_state:
        st.session_state.voice_mode = False
    if 'voice_interviewer' not in st.session_state:
        st.session_state.voice_interviewer = None
```

### 6.2 Groq API Integration Details

```python
# ai_service.py - API Configuration

DEFAULT_MODEL = "llama-3.1-70b-versatile"  # Primary model
FAST_MODEL = "llama-3.1-8b-instant"        # For quick completions

# Caching configuration
_response_cache: Dict[str, tuple] = {}
CACHE_TTL = 300  # 5 minutes

# Rate limiting
MIN_REQUEST_INTERVAL = 0.5  # 500ms between requests

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
    Main API call function with:
    - Response caching (5 min TTL)
    - Rate limiting (500ms minimum interval)
    - Exponential backoff retry (2^attempt seconds)
    - Conversation history support
    """
```

### 6.3 Knowledge Base Organization

```
┌──────────────────────────────────────────────────────────────────┐
│                     CONCEPT KNOWLEDGE BASE                        │
│                                                                  │
│  builtin_assistant.py                                            │
│  ├── CONCEPTS (8000+ lines)                                      │
│  │   ├── Python Core (47 concepts)                              │
│  │   │   ├── list, tuple, dict, set, string                    │
│  │   │   ├── if/else, for, while, comprehensions               │
│  │   │   ├── functions, lambda, decorators                     │
│  │   │   ├── classes, inheritance, OOP                         │
│  │   │   ├── exceptions, context managers                       │
│  │   │   └── file I/O, modules, packages                       │
│  │   │                                                          │
│  │   └── Advanced Python (15 concepts)                          │
│  │       ├── async/await, asyncio                              │
│  │       ├── dataclasses, type hints                           │
│  │       ├── pathlib, functools                                │
│  │       └── metaclasses, descriptors                          │
│  │                                                              │
│  └── TOPIC_COMPARISONS (7 comparisons)                          │
│      ├── list vs tuple                                          │
│      ├── list vs dict                                           │
│      ├── for vs while                                           │
│      ├── class vs function                                      │
│      ├── shallow vs deep copy                                   │
│      ├── == vs is                                               │
│      └── append vs extend                                       │
│                                                                  │
│  automation_concepts.py                                          │
│  ├── SELENIUM_CONCEPTS (25 concepts)                            │
│  │   ├── WebDriver setup & configuration                       │
│  │   ├── Locator strategies (ID, XPath, CSS)                   │
│  │   ├── Waits (implicit, explicit, fluent)                    │
│  │   ├── Actions API (mouse, keyboard)                         │
│  │   └── Page Object Model                                      │
│  │                                                              │
│  ├── ROBOT_CONCEPTS (12 concepts)                               │
│  │   ├── Keywords & Libraries                                   │
│  │   ├── Variables & Data Types                                │
│  │   └── Test organization                                      │
│  │                                                              │
│  └── PYTEST_CONCEPTS (9 concepts)                               │
│      ├── Fixtures & Scope                                       │
│      ├── Markers & Parameters                                   │
│      └── Plugins & Reporting                                    │
│                                                                  │
│  infrastructure_concepts.py                                      │
│  └── 43 concepts covering:                                       │
│      ├── Networking (TCP/IP, DNS, HTTP)                        │
│      ├── Servers (web, app, database)                          │
│      ├── Storage (SAN, NAS, RAID)                              │
│      └── Nutanix HCI Platform                                   │
│                                                                  │
│  linux_concepts.py                                               │
│  └── 24 concepts covering:                                       │
│      ├── System boot & systemd                                  │
│      ├── File permissions & users                               │
│      ├── Shell scripting                                        │
│      ├── Docker & containers                                    │
│      └── Network configuration                                  │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 7. Configuration & Environment

### 7.1 Environment Variables

```bash
# Required: None (works offline with built-in assistant)

# Optional: AI Enhancement
export GROQ_API_KEY="gsk_xxxxxxxxxxxxx"
# Get free key at: https://console.groq.com

# The application auto-detects API availability:
GROQ_AVAILABLE = bool(os.environ.get("GROQ_API_KEY"))
```

### 7.2 Dependencies (requirements.txt)

```
# Core Framework
streamlit>=1.28.0

# AI Service (Optional)
groq>=0.4.0
python-dotenv>=1.0.0

# Visualizations
plotly>=5.18.0

# PDF Knowledge Base
pymupdf>=1.23.0
sentence-transformers>=2.2.0
faiss-cpu>=1.7.4
numpy>=1.24.0

# Voice Features
gTTS>=2.5.0
pyttsx3>=2.90
SpeechRecognition>=3.10.0
audio-recorder-streamlit>=0.0.8
pydub>=0.25.1

# Testing
pytest>=7.4.0
pytest-cov>=4.1.0
```

### 7.3 Configuration Constants

```python
# evaluator.py
TIMEOUT_SECONDS = 5        # Code execution timeout

# ai_service.py
CACHE_TTL = 300            # Response cache (5 minutes)
MIN_REQUEST_INTERVAL = 0.5 # Rate limit (500ms)
DEFAULT_MODEL = "llama-3.1-70b-versatile"
FAST_MODEL = "llama-3.1-8b-instant"

# interview_engine.py
DEFAULT_TIME_LIMIT = 30    # Interview duration (minutes)
SELF_INTRO_DURATION = 30   # Voice mode intro (seconds)

# persistence.py
MAX_INTERVIEW_HISTORY = 100  # Keep last 100 interviews
MAX_BACKUP_FILES = 10        # Keep last 10 backups
```

---

## 8. Security Architecture

### 8.1 Code Execution Security

| Layer | Protection | Implementation |
|-------|-----------|----------------|
| **Pattern Detection** | Block dangerous imports | Regex patterns for os, sys, subprocess, etc. |
| **Restricted Builtins** | Whitelist safe functions | Custom `SAFE_BUILTINS` dictionary |
| **Blocked Functions** | Prevent code injection | Remove open, eval, exec, \_\_import\_\_ |
| **Attribute Access** | Block reflection attacks | Block \_\_class\_\_, \_\_globals\_\_, etc. |
| **Timeout Protection** | Prevent infinite loops | 5-second thread timeout |

### 8.2 Input Validation

```python
# Function name validation
if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', function_name):
    return False, "Invalid function name"

# Code length validation
if len(code) > 10000:
    return False, "Code too long (max 10,000 characters)"

# Test case validation
if not isinstance(test_cases, list):
    return False, "Invalid test case format"
```

### 8.3 Data Privacy

- ✅ **Local-first**: All data stored in local JSON files
- ✅ **No telemetry**: No usage tracking or analytics
- ✅ **No authentication**: No user accounts (privacy by design)
- ✅ **Opt-in API**: Groq API only used if key is explicitly set
- ✅ **Secure execution**: All user code runs in sandboxed environment

---

## 9. Testing Framework

### 9.1 Test Structure

```
tests/
├── conftest.py              # Shared fixtures
│   ├── default_progress     # Fresh progress structure
│   ├── sample_progress      # Pre-populated progress
│   ├── simple_code          # Test code sample
│   ├── simple_test_cases    # Basic test cases
│   └── interview_engine     # Configured engine
│
├── test_evaluator.py        # ~95% coverage
│   ├── test_valid_code_execution
│   ├── test_security_blocks_dangerous_imports
│   ├── test_timeout_protection
│   ├── test_syntax_error_handling
│   └── test_test_case_validation
│
├── test_persistence.py      # ~92% coverage
│   ├── test_save_load_progress
│   ├── test_streak_tracking
│   ├── test_achievement_unlock
│   ├── test_export_import
│   └── test_backup_restore
│
└── test_interview_engine.py # ~88% coverage
    ├── test_interview_start
    ├── test_stage_transitions
    ├── test_response_analysis
    ├── test_score_calculation
    └── test_feedback_generation
```

### 9.2 Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_evaluator.py

# Run specific test
pytest tests/test_evaluator.py::test_valid_code_execution

# Verbose output
pytest -v
```

### 9.3 Sample Test Cases

```python
# test_evaluator.py
def test_valid_code_execution():
    code = "def add(a, b):\n    return a + b"
    ok, msg = evaluate_user_code(code, "add", [((2, 3), 5)])
    assert ok == True
    assert "passed" in msg.lower()

def test_security_blocks_os_import():
    code = "import os\ndef test(): return os.getcwd()"
    ok, msg = evaluate_user_code(code, "test", [])
    assert ok == False
    assert "not allowed" in msg.lower()

def test_timeout_for_infinite_loop():
    code = "def infinite():\n    while True: pass"
    ok, msg = evaluate_user_code(code, "infinite", [((), None)])
    assert ok == False
    assert "timeout" in msg.lower() or "exceeded" in msg.lower()
```

---

## 10. Deployment & Usage

### 10.1 Installation Steps

```bash
# 1. Clone repository
git clone https://github.com/ANGRAJAKARNA/Build-codingLogic-AI.git
cd Build-codingLogic-AI/PythonCode

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. (Optional) Set up Groq API
export GROQ_API_KEY="your-api-key"

# 5. Run application
streamlit run main.py
```

### 10.2 Access Points

```
Local URL:      http://localhost:8501
Network URL:    http://192.168.x.x:8501
```

### 10.3 Usage Guide

#### Practice Mode
1. Select difficulty: Basic → Intermediate → Advanced → Automation
2. Choose a problem from the list
3. Read the problem statement and test cases
4. Write your solution in the code editor
5. Click **Run** to test against sample cases
6. Click **Submit** for full evaluation
7. View code review and move to next problem

#### Interview Mode
1. Click **Interview** in the header
2. Configure: Difficulty, Type, Time limit
3. Choose **Text Mode** or **Voice Mode**
4. Click **Start Interview**
5. Respond to interviewer prompts
6. Write code in coding stage
7. Receive detailed feedback at end

#### AI Chat
1. Click **Chat** button
2. Ask questions about Python, Selenium, etc.
3. Use slash commands: `/help`, `/compare list tuple`
4. Click follow-up suggestions for more info

### 10.4 Troubleshooting

| Issue | Solution |
|-------|----------|
| App won't start | Check Python version (3.9+), reinstall dependencies |
| Groq not working | Verify GROQ_API_KEY is set correctly |
| Voice mode issues | Install gTTS and SpeechRecognition |
| Code execution fails | Check for syntax errors in your code |
| Progress not saving | Check file permissions for user_progress.json |

---

## 📊 Summary Statistics

| Category | Count/Value |
|----------|-------------|
| **Total Python Modules** | 15+ |
| **Lines of Code** | 25,000+ |
| **Practice Problems** | 150+ |
| **Concepts Explained** | 175+ |
| **Interview Stages** | 8 |
| **Achievement Types** | 20+ |
| **Test Coverage** | ~90% |
| **Supported Platforms** | Windows, macOS, Linux |

---

## 🔗 Quick Reference Links

| Resource | Location |
|----------|----------|
| Main Application | `main.py` |
| Question Bank | `questions.py` |
| AI Assistant | `builtin_assistant.py` |
| Interview Engine | `interview_engine.py` |
| Code Evaluator | `evaluator.py` |
| Voice Features | `voice_engine.py` |
| Progress Storage | `persistence.py` |
| Tests | `tests/` |

---

**Document Generated:** January 2026  
**Project Repository:** [github.com/ANGRAJAKARNA/Build-codingLogic-AI](https://github.com/ANGRAJAKARNA/Build-codingLogic-AI)  
**Author:** Naveen Kumar Yellared

---

*This documentation provides a complete technical reference for the PyCode AI platform, covering architecture, data flows, security, and implementation details.*

