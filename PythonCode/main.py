# main.py
"""
PyCode - AI-Powered Python Coding Challenge Platform
Phone-Style UI with Practice, Interview, and AI Chat
"""

import streamlit as st
import time
import os
import random
from questions import QUESTIONS, ALL_TAGS, count_questions_by_tag
from evaluator import evaluate_user_code
from persistence import (
    save_progress, load_progress, get_default_progress,
    save_question_time, get_best_time, format_time, get_stats,
    save_interview_history, load_interview_history,
    update_streak, check_achievements, get_new_achievements,
    get_streak_info, record_solve, export_progress, import_progress
)

# Import Interview Engine
from interview_engine import (
    InterviewEngine, InterviewState, InterviewConfig,
    InterviewDifficulty, InterviewType, InterviewStage,
    create_interview_engine
)

# AI Services
GROQ_AVAILABLE = bool(os.environ.get("GROQ_API_KEY"))

if GROQ_AVAILABLE:
    try:
        from ai_service import (
            get_code_review as groq_code_review,
            get_bug_detection as groq_bug_detection,
            get_smart_hint as groq_smart_hint,
            get_tutor_response as groq_tutor_response,
        )
    except ImportError:
        GROQ_AVAILABLE = False

from builtin_assistant import (
    generate_response as builtin_chat,
    get_code_review as builtin_code_review,
    get_bug_hint as builtin_bug_hint,
    get_smart_hint as builtin_smart_hint,
)

st.set_page_config(page_title="PyCode AI", page_icon="🤖", layout="wide", initial_sidebar_state="collapsed")

# CSS Styles
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg: #0c1929;
    --cyan: #00e5ff;
    --purple: #bf5af2;
    --coral: #ff453a;
    --green: #30d158;
    --yellow: #ffd60a;
    --text: #ffffff;
    --text-dim: #9ca3af;
}

#MainMenu, footer, header, [data-testid="stToolbar"], [data-testid="stDecoration"], [data-testid="stSidebar"] { display: none !important; }

.stApp { background: linear-gradient(160deg, #050a12 0%, #0a1020 50%, #060d18 100%) !important; }
.main .block-container { padding: 0.5rem 2rem !important; max-width: 100% !important; }
* { font-family: 'Inter', sans-serif; }

/* PHONE 1 - PROBLEMS (CYAN/TEAL THEME) */
[data-testid="column"]:nth-child(1) > div:first-child {
    background: linear-gradient(180deg, #0a1a24 0%, #051015 50%, #020a0f 100%);
    border: 5px solid;
    border-image: linear-gradient(180deg, #00e5ff 0%, #00b8d4 50%, #006064 100%) 1;
    border-radius: 45px;
    box-shadow: 
        0 0 50px rgba(0, 229, 255, 0.5),
        0 0 100px rgba(0, 229, 255, 0.25),
        inset 0 0 40px rgba(0, 229, 255, 0.1),
        0 10px 40px rgba(0, 0, 0, 0.5);
    padding: 22px 18px !important;
    min-height: 680px;
    margin: 0 12px;
    position: relative;
    overflow: hidden;
}

[data-testid="column"]:nth-child(1) > div:first-child::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 120px;
    background: linear-gradient(180deg, rgba(0, 229, 255, 0.08) 0%, transparent 100%);
    pointer-events: none;
}

/* PHONE 2 - CODE EDITOR (PURPLE/VIOLET THEME) */
[data-testid="column"]:nth-child(2) > div:first-child {
    background: linear-gradient(180deg, #150a20 0%, #0d0518 50%, #08030f 100%);
    border: 5px solid;
    border-image: linear-gradient(180deg, #bf5af2 0%, #9945ff 50%, #5b21b6 100%) 1;
    border-radius: 45px;
    box-shadow: 
        0 0 50px rgba(191, 90, 242, 0.5),
        0 0 100px rgba(191, 90, 242, 0.25),
        inset 0 0 40px rgba(191, 90, 242, 0.1),
        0 10px 40px rgba(0, 0, 0, 0.5);
    padding: 22px 18px !important;
    min-height: 680px;
    margin: 0 12px;
    position: relative;
    overflow: hidden;
}

[data-testid="column"]:nth-child(2) > div:first-child::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 120px;
    background: linear-gradient(180deg, rgba(191, 90, 242, 0.08) 0%, transparent 100%);
    pointer-events: none;
}

/* PHONE 3 - AI CHAT (CORAL/ORANGE THEME) */
[data-testid="column"]:nth-child(3) > div:first-child {
    background: linear-gradient(180deg, #1a0a08 0%, #150505 50%, #0f0303 100%);
    border: 5px solid;
    border-image: linear-gradient(180deg, #ff453a 0%, #ff6b6b 50%, #b91c1c 100%) 1;
    border-radius: 45px;
    box-shadow: 
        0 0 50px rgba(255, 69, 58, 0.5),
        0 0 100px rgba(255, 69, 58, 0.25),
        inset 0 0 40px rgba(255, 69, 58, 0.1),
        0 10px 40px rgba(0, 0, 0, 0.5);
    padding: 22px 18px !important;
    min-height: 680px;
    margin: 0 12px;
    position: relative;
    overflow: hidden;
}

[data-testid="column"]:nth-child(3) > div:first-child::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 120px;
    background: linear-gradient(180deg, rgba(255, 69, 58, 0.08) 0%, transparent 100%);
    pointer-events: none;
}

/* Notch Styles with different colors per phone */
.notch { width: 110px; height: 30px; background: #000; border-radius: 15px; margin: 0 auto 12px; display: flex; align-items: center; justify-content: center; gap: 10px; box-shadow: inset 0 2px 4px rgba(0,0,0,0.5); }
.notch-cam { width: 10px; height: 10px; background: #1a2030; border-radius: 50%; border: 2px solid #2a2a40; }
.notch-led { width: 6px; height: 6px; background: var(--green); border-radius: 50%; box-shadow: 0 0 8px var(--green); animation: pulse 2s infinite; }
@keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }

/* Status bar with unique bottom borders per phone */
.status-bar { display: flex; justify-content: space-between; padding: 0 10px 12px; font-size: 11px; font-weight: 600; color: var(--text); margin-bottom: 14px; }
.status-bar-cyan { border-bottom: 2px solid rgba(0, 229, 255, 0.4); }
.status-bar-purple { border-bottom: 2px solid rgba(191, 90, 242, 0.4); }
.status-bar-coral { border-bottom: 2px solid rgba(255, 69, 58, 0.4); }

/* Phone headers with enhanced styling */
.phone-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; padding-bottom: 12px; }
.phone-header-cyan { border-bottom: 1px solid rgba(0, 229, 255, 0.2); }
.phone-header-purple { border-bottom: 1px solid rgba(191, 90, 242, 0.2); }
.phone-header-coral { border-bottom: 1px solid rgba(255, 69, 58, 0.2); }

.phone-title { font-size: 1.5rem; font-weight: 800; text-shadow: 0 0 20px currentColor; }
.title-cyan { color: var(--cyan); text-shadow: 0 0 30px rgba(0, 229, 255, 0.6); }
.title-purple { color: var(--purple); text-shadow: 0 0 30px rgba(191, 90, 242, 0.6); }
.title-coral { color: var(--coral); text-shadow: 0 0 30px rgba(255, 69, 58, 0.6); }

.avatar { width: 44px; height: 44px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 22px; box-shadow: 0 4px 15px rgba(0,0,0,0.3); }
.av-cyan { background: linear-gradient(135deg, #00e5ff, #00b8d4); box-shadow: 0 4px 20px rgba(0, 229, 255, 0.4); }
.av-purple { background: linear-gradient(135deg, #bf5af2, #9945ff); box-shadow: 0 4px 20px rgba(191, 90, 242, 0.4); }
.av-coral { background: linear-gradient(135deg, #ff453a, #ff6b6b); box-shadow: 0 4px 20px rgba(255, 69, 58, 0.4); }

/* Stats row with cyan theme */
.stats-row { display: flex; gap: 10px; margin-bottom: 14px; }
.stat-card { flex: 1; background: linear-gradient(180deg, rgba(0, 229, 255, 0.12) 0%, rgba(0, 229, 255, 0.04) 100%); border: 1px solid rgba(0, 229, 255, 0.35); border-radius: 16px; padding: 14px 10px; text-align: center; backdrop-filter: blur(10px); }
.stat-num { font-size: 1.7rem; font-weight: 800; color: var(--cyan); text-shadow: 0 0 15px rgba(0, 229, 255, 0.5); }
.stat-label { font-size: 10px; color: var(--text-dim); text-transform: uppercase; letter-spacing: 0.8px; margin-top: 2px; }

/* Section titles with enhanced styling */
.section-title { font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 1.2px; margin: 14px 0 10px; padding-left: 8px; border-left: 3px solid; }
.sec-cyan { color: var(--cyan); border-left-color: var(--cyan); }
.sec-purple { color: var(--purple); border-left-color: var(--purple); }
.sec-coral { color: var(--coral); border-left-color: var(--coral); }

/* Question cards with cyan theme */
.q-card { background: linear-gradient(135deg, rgba(0, 229, 255, 0.08) 0%, rgba(0, 229, 255, 0.02) 100%); border: 1px solid rgba(0, 229, 255, 0.3); border-radius: 14px; padding: 12px 14px; margin-bottom: 8px; transition: all 0.25s ease; }
.q-card:hover { background: linear-gradient(135deg, rgba(0, 229, 255, 0.15) 0%, rgba(0, 229, 255, 0.06) 100%); border-color: var(--cyan); transform: translateX(5px); box-shadow: 0 4px 15px rgba(0, 229, 255, 0.2); }
.q-card-active { background: linear-gradient(135deg, rgba(0, 229, 255, 0.2) 0%, rgba(0, 229, 255, 0.1) 100%) !important; border-color: var(--cyan) !important; box-shadow: 0 0 20px rgba(0, 229, 255, 0.3) !important; }
.q-header { display: flex; align-items: center; gap: 10px; }
.q-icon { font-size: 18px; }
.q-title { flex: 1; font-size: 12px; font-weight: 600; color: var(--text); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.q-tags { font-size: 10px; color: var(--cyan); margin-top: 4px; opacity: 0.85; }

/* Problem box with purple theme */
.problem-box { background: linear-gradient(135deg, rgba(191, 90, 242, 0.12) 0%, rgba(191, 90, 242, 0.04) 100%); border: 2px solid rgba(191, 90, 242, 0.4); border-radius: 18px; padding: 16px; margin-bottom: 12px; box-shadow: inset 0 0 20px rgba(191, 90, 242, 0.05); }
.problem-title { font-size: 1rem; font-weight: 700; color: var(--text); margin-bottom: 8px; line-height: 1.3; }
.badges { display: flex; gap: 5px; flex-wrap: wrap; }
.badge { padding: 4px 10px; border-radius: 16px; font-size: 10px; font-weight: 600; }
.b-easy { background: rgba(48, 209, 88, 0.2); color: var(--green); border: 1px solid rgba(48, 209, 88, 0.4); }
.b-med { background: rgba(255, 214, 10, 0.2); color: var(--yellow); border: 1px solid rgba(255, 214, 10, 0.4); }
.b-hard { background: rgba(255, 69, 58, 0.2); color: var(--coral); border: 1px solid rgba(255, 69, 58, 0.4); }
.b-tag { background: rgba(191, 90, 242, 0.15); color: #d8b4fe; border: 1px solid rgba(191, 90, 242, 0.3); }

.editor-box { background: #080a0f; border: 1px solid rgba(191, 90, 242, 0.3); border-radius: 12px; overflow: hidden; margin-bottom: 10px; }
.editor-header { background: rgba(191, 90, 242, 0.1); padding: 8px 12px; display: flex; align-items: center; gap: 6px; border-bottom: 1px solid rgba(191, 90, 242, 0.2); }
.dot { width: 10px; height: 10px; border-radius: 50%; }
.d-r { background: #ff5f57; }
.d-y { background: #febc2e; }
.d-g { background: #28c840; }
.editor-file { margin-left: 10px; font-size: 11px; color: #d8b4fe; font-family: 'JetBrains Mono', monospace; }

.timer { text-align: center; font-family: 'JetBrains Mono', monospace; font-size: 1.1rem; font-weight: 700; color: #d8b4fe; padding: 6px 0; }

/* Welcome screens with enhanced theming */
.welcome { text-align: center; padding: 30px 15px; }
.welcome-icon { width: 90px; height: 90px; border-radius: 50%; margin: 0 auto 20px; display: flex; align-items: center; justify-content: center; font-size: 44px; animation: float 3s ease-in-out infinite; }
.w-purple { background: linear-gradient(135deg, #bf5af2, #9945ff); box-shadow: 0 15px 50px rgba(191, 90, 242, 0.5), 0 0 80px rgba(191, 90, 242, 0.2); }
.w-coral { background: linear-gradient(135deg, #ff453a, #ff6b6b); box-shadow: 0 15px 50px rgba(255, 69, 58, 0.5), 0 0 80px rgba(255, 69, 58, 0.2); }
.w-cyan { background: linear-gradient(135deg, #00e5ff, #00b8d4); box-shadow: 0 15px 50px rgba(0, 229, 255, 0.5), 0 0 80px rgba(0, 229, 255, 0.2); }
.welcome-title { font-size: 1.5rem; font-weight: 700; color: var(--text); line-height: 1.35; margin-bottom: 8px; }
.welcome-sub { color: var(--text-dim); font-size: 13px; }

/* Chat buttons with coral theme */
.chat-btns { display: flex; gap: 10px; justify-content: center; margin: 16px 0; }
.chat-btn { background: linear-gradient(135deg, rgba(255, 69, 58, 0.1) 0%, rgba(255, 69, 58, 0.03) 100%); border: 1px solid rgba(255, 69, 58, 0.35); border-radius: 14px; padding: 12px 16px; display: flex; align-items: center; gap: 8px; transition: all 0.2s; }
.chat-btn:hover { background: linear-gradient(135deg, rgba(255, 69, 58, 0.2) 0%, rgba(255, 69, 58, 0.08) 100%); transform: translateY(-2px); box-shadow: 0 4px 15px rgba(255, 69, 58, 0.2); }
.chat-icon { width: 28px; height: 28px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 14px; }
.chat-label { font-size: 12px; font-weight: 600; color: var(--text); }

/* Chat messages */
.msg { padding: 12px 16px; border-radius: 18px; margin: 8px 0; max-width: 88%; font-size: 12px; line-height: 1.5; }
.msg-user { background: linear-gradient(135deg, #ff453a, #ff6b6b); color: white; margin-left: auto; border-radius: 18px 18px 4px 18px; box-shadow: 0 4px 15px rgba(255, 69, 58, 0.3); }
.msg-ai { background: linear-gradient(135deg, rgba(255, 255, 255, 0.08) 0%, rgba(255, 255, 255, 0.03) 100%); border: 1px solid rgba(255, 69, 58, 0.3); color: #e5e7eb; border-radius: 18px 18px 18px 4px; }

/* Text inputs with different theming */
.stTextArea textarea { font-family: 'JetBrains Mono', monospace !important; font-size: 12px !important; background: #060810 !important; color: #e2e8f0 !important; border: 1px solid rgba(191, 90, 242, 0.25) !important; border-radius: 8px !important; }
.stTextInput input { background: rgba(255, 255, 255, 0.05) !important; border: 1px solid rgba(255, 255, 255, 0.2) !important; border-radius: 14px !important; color: var(--text) !important; font-size: 13px !important; padding: 12px 16px !important; }
.stTextInput input:focus { border-color: currentColor !important; box-shadow: 0 0 20px rgba(255, 255, 255, 0.1) !important; }

/* Buttons with enhanced styling */
.stButton > button { font-weight: 600 !important; border-radius: 12px !important; font-size: 12px !important; padding: 8px 16px !important; transition: all 0.25s ease !important; }
.stButton > button:hover { transform: translateY(-2px) !important; }

/* Button styles per column */
[data-testid="column"]:nth-child(1) .stButton > button[kind="primary"] { background: linear-gradient(135deg, #00e5ff, #00b8d4) !important; border: none !important; box-shadow: 0 4px 15px rgba(0, 229, 255, 0.35) !important; }
[data-testid="column"]:nth-child(1) .stButton > button[kind="secondary"] { background: rgba(0, 229, 255, 0.1) !important; border: 1px solid rgba(0, 229, 255, 0.4) !important; color: var(--cyan) !important; }

[data-testid="column"]:nth-child(2) .stButton > button[kind="primary"] { background: linear-gradient(135deg, #bf5af2, #9945ff) !important; border: none !important; box-shadow: 0 4px 15px rgba(191, 90, 242, 0.35) !important; }
[data-testid="column"]:nth-child(2) .stButton > button[kind="secondary"] { background: rgba(191, 90, 242, 0.1) !important; border: 1px solid rgba(191, 90, 242, 0.4) !important; color: var(--purple) !important; }

[data-testid="column"]:nth-child(3) .stButton > button[kind="primary"] { background: linear-gradient(135deg, #ff453a, #ff6b6b) !important; border: none !important; box-shadow: 0 4px 15px rgba(255, 69, 58, 0.35) !important; }
[data-testid="column"]:nth-child(3) .stButton > button[kind="secondary"] { background: rgba(255, 69, 58, 0.1) !important; border: 1px solid rgba(255, 69, 58, 0.4) !important; color: var(--coral) !important; }

/* Progress bar with purple theme */
.stProgress > div > div { background: linear-gradient(90deg, var(--purple), #d8b4fe) !important; border-radius: 8px; box-shadow: 0 0 10px rgba(191, 90, 242, 0.4); }
.stProgress > div { background: rgba(191, 90, 242, 0.12) !important; border-radius: 8px; height: 8px !important; }

.msg-ok { background: rgba(48, 209, 88, 0.15); border: 1px solid rgba(48, 209, 88, 0.4); border-left: 4px solid var(--green); border-radius: 0 12px 12px 0; padding: 12px 14px; color: #86efac; margin: 8px 0; font-size: 12px; }
.msg-err { background: rgba(255, 69, 58, 0.15); border: 1px solid rgba(255, 69, 58, 0.4); border-left: 4px solid var(--coral); border-radius: 0 12px 12px 0; padding: 12px 14px; color: #fca5a5; margin: 8px 0; font-size: 12px; }
.msg-hint { background: rgba(191, 90, 242, 0.12); border: 1px solid rgba(191, 90, 242, 0.35); border-left: 4px solid var(--purple); border-radius: 0 12px 12px 0; padding: 12px 14px; margin: 8px 0; font-size: 12px; color: #e5e7eb; }

.test-case { background: rgba(191, 90, 242, 0.08); border: 1px solid rgba(191, 90, 242, 0.25); border-radius: 8px; padding: 8px 12px; margin: 4px 0; font-family: 'JetBrains Mono', monospace; font-size: 10px; }
.test-lbl { color: #d8b4fe; font-weight: 600; }

@keyframes float { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-8px); } }
</style>
""", unsafe_allow_html=True)

# Session State
if "progress" not in st.session_state:
    loaded = load_progress()
    st.session_state.progress = loaded if loaded else get_default_progress()

defaults = {
    "stage": None,
    "q_index": 0,
    "passed": False,
    "show_hint": 0,
    "timer_start": None,
    "chat_history": [],
    "ai_feedback": None,
    "ai_hint": None,
    "app_mode": "Practice",
    "selected_difficulty": "Basic",
    # Interview engine state
    "interview_active": False,
    "interview_engine": None,
    "interview_code": "",
    "interview_feedback_shown": False,
    "interview_config": {"difficulty": "mid", "type": "technical", "time_limit": 30},
    # Achievements tracking
    "last_achievements": [],
    "new_achievement": None,
    "used_hint_this_problem": False,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# Update streak on app load
if st.session_state.progress:
    st.session_state.progress = update_streak(st.session_state.progress)
    save_progress(st.session_state.progress)

DIFFS = ["Basic", "Intermediate", "Advanced"]


def get_status(stage, idx):
    if idx in st.session_state.progress[stage]["completed"]:
        return "✅"
    if idx in st.session_state.progress[stage]["skipped"]:
        return "⏭️"
    return "📝"


def get_stats_d(stage):
    return len(QUESTIONS[stage]), len(st.session_state.progress[stage]["completed"]), len(st.session_state.progress[stage]["skipped"])


def next_q(stage):
    for i in range(len(QUESTIONS[stage])):
        if i not in st.session_state.progress[stage]["completed"] and i not in st.session_state.progress[stage]["skipped"]:
            return i
    return 0


def go_to(stage, idx):
    st.session_state.stage = stage
    st.session_state.q_index = idx
    st.session_state.passed = False
    st.session_state.show_hint = 0
    st.session_state.timer_start = time.time()
    st.session_state.ai_feedback = None
    st.session_state.ai_hint = None


def badge_cls(s):
    if s == "Basic":
        return "b-easy"
    elif s == "Intermediate":
        return "b-med"
    return "b-hard"


def render_tags(tags):
    return "".join([f'<span class="badge b-tag">{t}</span>' for t in tags[:3]])


def get_chat_context():
    if not st.session_state.chat_history:
        return ""
    recent = st.session_state.chat_history[-4:]
    context = "Previous conversation:\n"
    for msg in recent:
        role = "User" if msg["role"] == "user" else "Assistant"
        content = msg['content'][:100] + "..." if len(msg['content']) > 100 else msg['content']
        context += f"{role}: {content}\n"
    return context


# Header
st.markdown("""
<div style="text-align:center;padding:6px 0 12px">
    <div style="display:inline-flex;align-items:center;gap:12px">
        <div style="font-size:2rem">🤖</div>
        <div>
            <div style="font-size:1.6rem;font-weight:800;background:linear-gradient(90deg,#00e5ff,#bf5af2,#ff453a);-webkit-background-clip:text;-webkit-text-fill-color:transparent">PyCode AI</div>
            <div style="font-size:0.7rem;color:#9ca3af;letter-spacing:1px">SMART PYTHON LEARNING</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Mode Selector
mode_cols = st.columns([1, 3, 1])
with mode_cols[1]:
    modes = ["💻 Practice", "🎯 Interview", "🤖 AI Chat"]
    current_idx = 0
    if st.session_state.app_mode == "Interview":
        current_idx = 1
    elif st.session_state.app_mode == "Chat":
        current_idx = 2
    
    mode = st.radio("", modes, index=current_idx, horizontal=True, label_visibility="collapsed")
    new_mode = mode.split(" ")[-1]
    if new_mode != st.session_state.app_mode:
        st.session_state.app_mode = new_mode
        st.rerun()

# Layout - three distinct phone interfaces
c1, c2, c3 = st.columns([1, 1.25, 1], gap="large")

# LEFT PHONE - PROBLEMS
with c1:
    st.markdown('<div class="notch"><div class="notch-cam"></div><div class="notch-led"></div></div>', unsafe_allow_html=True)
    st.markdown('<div class="status-bar status-bar-cyan"><span>9:41</span><span>📶 🔋 100%</span></div>', unsafe_allow_html=True)
    
    if st.session_state.app_mode == "Interview":
        st.markdown('<div class="phone-header phone-header-cyan"><span class="phone-title title-cyan">Interview</span><div class="avatar av-cyan">🎯</div></div>', unsafe_allow_html=True)
        
        if not st.session_state.interview_active:
            # Interview Setup Panel
            st.markdown('<div class="section-title sec-cyan">DIFFICULTY</div>', unsafe_allow_html=True)
            diff_map = {"Junior": "junior", "Mid-Level": "mid", "Senior": "senior"}
            diff = st.selectbox("", list(diff_map.keys()), index=1, key="iv_diff", label_visibility="collapsed")
            
            st.markdown('<div class="section-title sec-cyan">TYPE</div>', unsafe_allow_html=True)
            type_map = {"Technical": "technical", "Behavioral": "behavioral", "Mixed": "mixed"}
            iv_type = st.selectbox("", list(type_map.keys()), index=0, key="iv_type", label_visibility="collapsed")
            
            st.markdown('<div class="section-title sec-cyan">TIME (minutes)</div>', unsafe_allow_html=True)
            time_limit = st.slider("", 15, 60, 30, 5, key="iv_time", label_visibility="collapsed")
            
            st.markdown('<div class="section-title sec-cyan">PROBLEM</div>', unsafe_allow_html=True)
            # Select a random problem for the interview
            problem_stage = "Intermediate" if diff == "Mid-Level" else ("Advanced" if diff == "Senior" else "Basic")
            available_problems = [(i, q) for i, q in enumerate(QUESTIONS[problem_stage])]
            problem_names = [f"{q['question'][:30]}..." for _, q in available_problems]
            selected_problem = st.selectbox("", problem_names, key="iv_problem", label_visibility="collapsed")
            
            if st.button("🚀 Start Interview", type="primary", use_container_width=True):
                # Create interview engine with selected config
                engine = create_interview_engine(
                    difficulty=diff_map[diff],
                    interview_type=type_map[iv_type],
                    time_limit=time_limit
                )
                
                # Get selected problem
                prob_idx = problem_names.index(selected_problem)
                problem_data = available_problems[prob_idx][1]
                
                # Start the interview
                intro_msg = engine.start_new_interview(
                    problem=problem_data["question"],
                    function_name=problem_data["function"]
                )
                
                st.session_state.interview_engine = engine
                st.session_state.interview_active = True
                st.session_state.interview_code = f"def {problem_data['function']}():\n    # Your code here\n    pass"
                st.session_state.interview_feedback_shown = False
                st.session_state.interview_problem = problem_data
                st.rerun()
        else:
            # Show Interview Progress
            engine = st.session_state.interview_engine
            if engine:
                progress = engine.get_stage_progress()
                
                # Stage indicator
                stage_icons = {
                    "intro": "👋", "approach": "🧠", "coding": "💻",
                    "optimization": "⚡", "behavioral": "💬", "wrapup": "🎁", "completed": "✅"
                }
                current_stage = progress["current_stage"]
                st.markdown(f'<div class="stat-card"><div class="stat-num">{stage_icons.get(current_stage, "🎯")}</div><div class="stat-label">{current_stage.upper()}</div></div>', unsafe_allow_html=True)
                
                # Time remaining
                remaining = progress["remaining_time"]
                mins, secs = divmod(remaining, 60)
                time_color = "var(--coral)" if remaining < 120 else "var(--cyan)"
                st.markdown(f'<div style="text-align:center;font-size:1.5rem;font-weight:700;color:{time_color};font-family:JetBrains Mono">{mins:02d}:{secs:02d}</div>', unsafe_allow_html=True)
                
                # Progress bar
                st.progress(progress["progress_percent"] / 100)
                
                # Live scores (if enabled)
                scores = engine.state.scores
                st.markdown('<div class="section-title sec-cyan">LIVE SCORES</div>', unsafe_allow_html=True)
                score_items = [
                    ("🧩 Problem", scores.problem_solving),
                    ("💬 Comms", scores.communication),
                    ("📝 Code", scores.code_quality),
                    ("📊 Analysis", scores.complexity_analysis)
                ]
                for label, score in score_items:
                    st.markdown(f'<div style="display:flex;justify-content:space-between;padding:4px 0;font-size:11px"><span>{label}</span><span style="color:var(--cyan)">{score:.0f}</span></div>', unsafe_allow_html=True)
                
                if st.button("🛑 End Interview", use_container_width=True, type="secondary"):
                    feedback = engine.force_end_interview()
                    st.session_state.interview_feedback_shown = True
                    st.rerun()
        
        # Recent interviews
        history = load_interview_history()
        if history and not st.session_state.interview_active:
            st.markdown('<div class="section-title sec-cyan">RECENT</div>', unsafe_allow_html=True)
            for h in history[-3:]:
                grade = h.get("grade", "?")
                topic = h.get("topic", "Interview")[:20]
                st.markdown(f'<div class="q-card"><div class="q-header"><span class="q-icon">📊</span><span class="q-title">{topic}</span><span style="color:var(--green)">{grade}</span></div></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="phone-header phone-header-cyan"><span class="phone-title title-cyan">Problems</span><div class="avatar av-cyan">📋</div></div>', unsafe_allow_html=True)
        
        stats = get_stats(st.session_state.progress)
        st.markdown(f'<div class="stats-row"><div class="stat-card"><div class="stat-num">{stats["total_completed"]}</div><div class="stat-label">Solved</div></div><div class="stat-card"><div class="stat-num">{stats["completion_rate"]:.0f}%</div><div class="stat-label">Progress</div></div></div>', unsafe_allow_html=True)
        
        st.markdown('<div class="section-title sec-cyan">DIFFICULTY</div>', unsafe_allow_html=True)
        diff_cols = st.columns(3)
        for i, d in enumerate(DIFFS):
            with diff_cols[i]:
                btn_type = "primary" if st.session_state.selected_difficulty == d else "secondary"
                if st.button(d[:3].upper(), key=f"diff_{d}", use_container_width=True, type=btn_type):
                    st.session_state.selected_difficulty = d
                    st.rerun()
        
        selected_d = st.session_state.selected_difficulty
        t, c, s = get_stats_d(selected_d)
        st.markdown(f'<div class="section-title sec-cyan">{selected_d.upper()} ({c}/{t})</div>', unsafe_allow_html=True)
        
        with st.container(height=320):
            for i, q in enumerate(QUESTIONS[selected_d]):
                icon = get_status(selected_d, i)
                is_active = st.session_state.stage == selected_d and st.session_state.q_index == i
                active_cls = "q-card-active" if is_active else ""
                
                st.markdown(f'<div class="q-card {active_cls}"><div class="q-header"><span class="q-icon">{icon}</span><span class="q-title">{q["question"][:26]}...</span></div><div class="q-tags">{", ".join(q.get("tags", [])[:2])}</div></div>', unsafe_allow_html=True)
                
                if st.button("Select →", key=f"sel_{selected_d}_{i}", use_container_width=True):
                    go_to(selected_d, i)
                    st.rerun()

# CENTER PHONE - CODE EDITOR
with c2:
    st.markdown('<div class="notch"><div class="notch-cam"></div><div class="notch-led"></div></div>', unsafe_allow_html=True)
    st.markdown('<div class="status-bar status-bar-purple"><span>9:41</span><span>📶 🔋 100%</span></div>', unsafe_allow_html=True)
    
    if st.session_state.app_mode == "Interview" and st.session_state.interview_active:
        engine = st.session_state.interview_engine
        
        if engine and st.session_state.interview_feedback_shown:
            # Show final feedback
            st.markdown('<div style="text-align:center;font-weight:700;color:#30d158;padding:8px;margin-bottom:10px;background:rgba(48,209,88,0.1);border-radius:10px">✅ Interview Complete</div>', unsafe_allow_html=True)
            
            feedback = engine._generate_final_feedback()
            st.markdown(f'<div class="msg-hint" style="max-height:500px;overflow-y:auto">{feedback}</div>', unsafe_allow_html=True)
            
            # Save interview result
            result = {
                "topic": engine.state.problem_name,
                "scores": {
                    "problem_solving": engine.state.scores.problem_solving,
                    "communication": engine.state.scores.communication,
                    "code_quality": engine.state.scores.code_quality,
                    "complexity_analysis": engine.state.scores.complexity_analysis,
                    "total": engine.state.scores.get_total()
                },
                "grade": engine.state.scores.get_grade(),
                "recommendation": engine.state.scores.get_hiring_recommendation(),
                "difficulty": engine.state.config.difficulty.value,
                "interview_type": engine.state.config.interview_type.value,
                "duration_seconds": engine.state.get_elapsed_time()
            }
            save_interview_history(result)
            
            if st.button("🔄 Start New Interview", type="primary", use_container_width=True):
                st.session_state.interview_active = False
                st.session_state.interview_engine = None
                st.session_state.interview_feedback_shown = False
                st.rerun()
        
        elif engine:
            # Active interview
            problem = st.session_state.get("interview_problem", {})
            progress = engine.get_stage_progress()
            current_stage = progress["current_stage"]
            
            # Header with problem and stage
            stage_names = {"intro": "Introduction", "approach": "Approach", "coding": "Coding", "optimization": "Optimization", "behavioral": "Behavioral", "wrapup": "Wrap Up"}
            st.markdown(f'<div style="text-align:center;font-weight:700;color:#d8b4fe;padding:8px;margin-bottom:10px;background:rgba(191,90,242,0.1);border-radius:10px">🎯 {stage_names.get(current_stage, "Interview")}</div>', unsafe_allow_html=True)
            
            # Problem display
            if problem:
                st.markdown(f'<div class="problem-box"><div class="problem-title">{problem.get("question", "Coding Problem")}</div></div>', unsafe_allow_html=True)
            
            # Conversation history
            with st.container(height=180):
                for msg in engine.state.conversation_history[-6:]:
                    if msg["role"] == "user":
                        st.markdown(f'<div class="msg msg-user">{msg["content"]}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="msg msg-ai">{msg["content"]}</div>', unsafe_allow_html=True)
            
            # Code editor (for coding stage)
            if current_stage in ["coding", "optimization"]:
                st.markdown('<div class="editor-box"><div class="editor-header"><span class="dot d-r"></span><span class="dot d-y"></span><span class="dot d-g"></span><span class="editor-file">solution.py</span></div></div>', unsafe_allow_html=True)
                code = st.text_area("", value=st.session_state.interview_code, height=100, key="iv_code_editor", label_visibility="collapsed")
                st.session_state.interview_code = code
            
            # Input and send
            iv_input = st.text_input("", placeholder="Your response...", key="iv_input", label_visibility="collapsed")
            
            iv_c1, iv_c2 = st.columns([4, 1])
            with iv_c1:
                if st.button("Send →", type="primary", use_container_width=True, key="iv_send"):
                    if iv_input:
                        code = st.session_state.interview_code if current_stage in ["coding", "optimization"] else ""
                        response = engine.process_response(iv_input, code)
                        
                        # Check if interview is complete
                        if engine.state.current_stage == InterviewStage.COMPLETED:
                            st.session_state.interview_feedback_shown = True
                        
                        st.rerun()
            with iv_c2:
                if st.button("End", key="iv_end"):
                    engine.force_end_interview()
                    st.session_state.interview_feedback_shown = True
                    st.rerun()
            
            # Check for time up
            if progress["is_time_up"] and not st.session_state.interview_feedback_shown:
                engine.force_end_interview()
                st.session_state.interview_feedback_shown = True
                st.rerun()
    
    elif st.session_state.stage is None:
        st.markdown('<div class="welcome"><div class="welcome-icon w-purple">💻</div><div class="welcome-title">Welcome to<br/>Code Editor</div><div class="welcome-sub">Select a problem to start coding</div></div>', unsafe_allow_html=True)
        
        b1, b2, b3 = st.columns(3)
        with b1:
            if st.button("🌱 Easy", use_container_width=True, type="primary"):
                st.session_state.selected_difficulty = "Basic"
                go_to("Basic", next_q("Basic"))
                st.rerun()
        with b2:
            if st.button("🌿 Medium", use_container_width=True):
                st.session_state.selected_difficulty = "Intermediate"
                go_to("Intermediate", next_q("Intermediate"))
                st.rerun()
        with b3:
            if st.button("🔥 Hard", use_container_width=True):
                st.session_state.selected_difficulty = "Advanced"
                go_to("Advanced", next_q("Advanced"))
                st.rerun()
    else:
        stage = st.session_state.stage
        qi = st.session_state.q_index
        data = QUESTIONS[stage][qi]
        t, c, s = get_stats_d(stage)
        
        n1, n2, n3 = st.columns([1, 2, 1])
        with n1:
            if st.button("⬅️", key="back"):
                st.session_state.stage = None
                st.rerun()
        with n2:
            st.markdown(f'<div style="text-align:center;font-weight:700;color:#d8b4fe;padding:6px">{stage} • Q{qi+1}/{t}</div>', unsafe_allow_html=True)
        with n3:
            if qi < t - 1:
                if st.button("➡️", key="next"):
                    go_to(stage, qi + 1)
                    st.rerun()
        
        st.markdown(f'<div class="problem-box"><div class="problem-title">{data["question"]}</div><div class="badges"><span class="badge {badge_cls(stage)}">{stage}</span>{render_tags(data.get("tags", []))}</div></div>', unsafe_allow_html=True)
        
        st.progress((c + s) / t if t > 0 else 0)
        
        if st.session_state.timer_start is None:
            st.session_state.timer_start = time.time()
        if not st.session_state.passed:
            st.markdown(f'<div class="timer">⏱️ {format_time(time.time() - st.session_state.timer_start)}</div>', unsafe_allow_html=True)
        
        tc = data["test_cases"]
        if not tc:
            params = ""
        elif len(tc[0][0]) == 1:
            params = "n"
        elif len(tc[0][0]) == 2:
            params = "a, b"
        else:
            params = ", ".join([f"arg{j+1}" for j in range(len(tc[0][0]))])
        template = f"def {data['function']}({params}):\n    # Your code here\n    pass"
        
        st.markdown('<div class="editor-box"><div class="editor-header"><span class="dot d-r"></span><span class="dot d-y"></span><span class="dot d-g"></span><span class="editor-file">solution.py</span></div></div>', unsafe_allow_html=True)
        
        code = st.text_area("", value=template, height=100, key=f"code_{stage}_{qi}", label_visibility="collapsed")
        
        btn1, btn2, btn3 = st.columns(3)
        with btn1:
            run_btn = st.button("▶️ Run", type="primary", use_container_width=True)
        with btn2:
            hint_btn = st.button("💡 Hint", use_container_width=True)
        with btn3:
            skip_btn = st.button("⏭️ Skip", use_container_width=True)
        
        if hint_btn:
            with st.spinner("🤔"):
                try:
                    st.session_state.ai_hint = builtin_smart_hint(code, data['question'], data['function'], data.get('hints', []), st.session_state.show_hint + 1)
                    st.session_state.show_hint += 1
                except Exception as e:
                    st.session_state.ai_hint = str(e)
        
        if st.session_state.ai_hint:
            st.markdown(f'<div class="msg-hint">💡 {st.session_state.ai_hint}</div>', unsafe_allow_html=True)
        
        if run_btn:
            ok, msg = evaluate_user_code(code, data["function"], data["test_cases"])
            if ok:
                el = time.time() - st.session_state.timer_start
                st.markdown(f'<div class="msg-ok">✅ All tests passed! Time: {format_time(el)}</div>', unsafe_allow_html=True)
                st.session_state.passed = True
                st.session_state.progress[stage]["completed"].add(qi)
                st.session_state.progress[stage]["skipped"].discard(qi)
                st.session_state.progress = save_question_time(st.session_state.progress, stage, qi, el)
                save_progress(st.session_state.progress)
                with st.spinner("📝"):
                    try:
                        st.session_state.ai_feedback = builtin_code_review(code, data['question'], data['function'], el)
                    except Exception:
                        pass
            else:
                st.markdown(f'<div class="msg-err">❌ {msg}</div>', unsafe_allow_html=True)
                with st.spinner("🔍"):
                    try:
                        bug = builtin_bug_hint(code, msg, data['question'], data['function'])
                        st.markdown(f'<div class="msg-hint">🔍 {bug}</div>', unsafe_allow_html=True)
                    except Exception:
                        pass
        
        if st.session_state.ai_feedback:
            st.markdown(f'<div class="msg-hint">📝 {st.session_state.ai_feedback}</div>', unsafe_allow_html=True)
        
        if skip_btn:
            if qi not in st.session_state.progress[stage]["completed"]:
                st.session_state.progress[stage]["skipped"].add(qi)
                save_progress(st.session_state.progress)
            go_to(stage, (qi + 1) % t)
            st.rerun()
        
        st.markdown('<div class="section-title sec-purple">TEST CASES</div>', unsafe_allow_html=True)
        for inp, exp in data["test_cases"][:2]:
            st.markdown(f'<div class="test-case"><span class="test-lbl">In:</span> {inp} → <span class="test-lbl">Out:</span> {exp}</div>', unsafe_allow_html=True)

# RIGHT PHONE - AI CHAT
with c3:
    st.markdown('<div class="notch"><div class="notch-cam"></div><div class="notch-led"></div></div>', unsafe_allow_html=True)
    st.markdown('<div class="status-bar status-bar-coral"><span>9:41</span><span>📶 🔋 100%</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="phone-header phone-header-coral"><span class="phone-title title-coral">AI Chat</span><div class="avatar av-coral">🤖</div></div>', unsafe_allow_html=True)
    
    if not st.session_state.chat_history:
        st.markdown('<div class="welcome"><div class="welcome-icon w-coral">🤖</div><div class="welcome-title">Welcome to<br/>AI Chat</div></div>', unsafe_allow_html=True)
        st.markdown('<div class="chat-btns"><div class="chat-btn"><div class="chat-icon" style="background:linear-gradient(135deg,#ff9500,#ff5e3a)">📝</div><span class="chat-label">Python</span></div><div class="chat-btn"><div class="chat-icon" style="background:linear-gradient(135deg,#30d158,#00c853)">🔧</div><span class="chat-label">Selenium</span></div><div class="chat-btn"><div class="chat-icon" style="background:linear-gradient(135deg,#bf5af2,#9945ff)">🤖</div><span class="chat-label">Robot</span></div></div>', unsafe_allow_html=True)
    else:
        with st.container(height=350):
            for m in st.session_state.chat_history[-8:]:
                if m["role"] == "user":
                    st.markdown(f'<div class="msg msg-user">{m["content"]}</div>', unsafe_allow_html=True)
                else:
                    # Show full response, not truncated
                    st.markdown(f'<div class="msg msg-ai">{m["content"]}</div>', unsafe_allow_html=True)
    
    user_msg = st.text_input("", placeholder="Ask about Python, Selenium, Robot Framework...", key="chat_in", label_visibility="collapsed")
    
    send_col, clear_col = st.columns([4, 1])
    with send_col:
        send_btn = st.button("Send →", type="primary", use_container_width=True, key="send")
    with clear_col:
        if st.button("🗑️", key="clear"):
            st.session_state.chat_history = []
            st.rerun()
    
    if send_btn and user_msg:
        st.session_state.chat_history.append({"role": "user", "content": user_msg})
        with st.spinner("🤖"):
            try:
                context = get_chat_context()
                enhanced_msg = f"{context}\nCurrent question: {user_msg}" if context else user_msg
                
                if st.session_state.stage:
                    d = QUESTIONS[st.session_state.stage][st.session_state.q_index]
                    cc = st.session_state.get(f"code_{st.session_state.stage}_{st.session_state.q_index}", "")
                    resp = builtin_chat(enhanced_msg, d['question'], d['function'], cc, False)
                else:
                    resp = builtin_chat(enhanced_msg, "", "", "", False)
                st.session_state.chat_history.append({"role": "assistant", "content": resp})
            except Exception as e:
                st.session_state.chat_history.append({"role": "assistant", "content": f"Error: {str(e)[:50]}"})
        st.rerun()
    
    st.markdown('<div class="section-title sec-coral">QUICK PROMPTS</div>', unsafe_allow_html=True)
    qp1, qp2 = st.columns(2)
    with qp1:
        if st.button("Explain 📖", use_container_width=True, key="qp1"):
            st.session_state.chat_history.append({"role": "user", "content": "Explain this problem in detail"})
            st.rerun()
    with qp2:
        if st.button("Help 💡", use_container_width=True, key="qp2"):
            st.session_state.chat_history.append({"role": "user", "content": "Give me a hint to solve this"})
            st.rerun()

st.markdown('<div style="text-align:center;padding:10px;color:#6b7280;font-size:0.65rem">Made with ❤️ • <span style="background:linear-gradient(90deg,#00e5ff,#bf5af2,#ff453a);-webkit-background-clip:text;-webkit-text-fill-color:transparent;font-weight:700">PyCode AI</span></div>', unsafe_allow_html=True)
