# main.py
"""
PyCode - AI-Powered Python Coding Challenge Platform
"""

import streamlit as st
import time
import os
from questions import QUESTIONS, ALL_TAGS, count_questions_by_tag
from evaluator import evaluate_user_code
from persistence import (
    save_progress, load_progress, get_default_progress,
    save_question_time, get_best_time, format_time, get_stats
)

GROQ_AVAILABLE = bool(os.environ.get("GROQ_API_KEY"))

if GROQ_AVAILABLE:
    try:
        from ai_service import (
            get_code_review as groq_code_review,
            get_bug_detection as groq_bug_detection,
            get_smart_hint as groq_smart_hint,
            get_tutor_response as groq_tutor_response,
            get_code_explanation as groq_code_explanation,
        )
    except ImportError:
        GROQ_AVAILABLE = False

from builtin_assistant import (
    generate_response as builtin_chat,
    get_code_review as builtin_code_review,
    get_bug_hint as builtin_bug_hint,
    get_smart_hint as builtin_smart_hint,
)

st.set_page_config(
    page_title="PyCode",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
    
    :root {
        --bg-primary: #0a0a0f;
        --bg-secondary: #12121a;
        --bg-card: #1a1a24;
        --bg-elevated: #22222e;
        --border: #2a2a3a;
        --text-primary: #f0f0f5;
        --text-secondary: #8888a0;
        --text-muted: #5a5a70;
        --accent: #ff6b6b;
        --success: #10b981;
        --warning: #f59e0b;
        --error: #ef4444;
        --purple: #a855f7;
        --teal: #14b8a6;
        --gradient-1: linear-gradient(135deg, #ff6b6b 0%, #a855f7 100%);
    }
    
    .stApp { background: var(--bg-primary); }
    .main .block-container { padding: 1.5rem 2rem; max-width: 100%; }
    
    h1, h2, h3, h4, h5 {
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 600;
        color: var(--text-primary);
    }
    
    p, span, div { font-family: 'Space Grotesk', sans-serif; }
    
    [data-testid="stSidebar"] {
        background: var(--bg-secondary);
        border-right: 1px solid var(--border);
    }
    
    .stat-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
    }
    
    .stat-value {
        font-size: 2.5rem;
        font-weight: 700;
        background: var(--gradient-1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .stat-label {
        font-size: 0.875rem;
        color: var(--text-secondary);
        text-transform: uppercase;
    }
    
    .diff-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 1.75rem;
        transition: all 0.3s;
    }
    
    .diff-card:hover {
        border-color: var(--accent);
        transform: translateY(-4px);
    }
    
    .code-editor-container {
        background: #0d0d12;
        border: 1px solid var(--border);
        border-radius: 12px;
        overflow: hidden;
    }
    
    .code-header {
        background: linear-gradient(180deg, #1a1a24 0%, #15151e 100%);
        padding: 12px 16px;
        display: flex;
        align-items: center;
        gap: 8px;
        border-bottom: 1px solid var(--border);
    }
    
    .code-dot { width: 12px; height: 12px; border-radius: 50%; }
    .dot-close { background: #ff5f57; }
    .dot-min { background: #febc2e; }
    .dot-max { background: #28c840; }
    
    .code-title {
        margin-left: 12px;
        font-size: 13px;
        color: var(--text-secondary);
        font-family: 'JetBrains Mono', monospace;
    }
    
    .stTextArea textarea {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 14px !important;
        background: #0d0d12 !important;
        color: #e0e0e8 !important;
        border: none !important;
    }
    
    .stButton > button {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 600;
        border-radius: 10px;
    }
    
    .stProgress > div > div { background: var(--gradient-1); border-radius: 10px; }
    .stProgress > div { background: var(--bg-elevated); border-radius: 10px; }
    
    .tag {
        display: inline-flex;
        padding: 4px 12px;
        margin: 3px;
        border-radius: 20px;
        font-size: 12px;
        background: rgba(20, 184, 166, 0.15);
        color: var(--teal);
        border: 1px solid rgba(20, 184, 166, 0.3);
    }
    
    .ai-badge {
        display: inline-flex;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 600;
        background: var(--gradient-1);
        color: white;
        text-transform: uppercase;
    }
    
    .msg-success {
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-left: 4px solid var(--success);
        padding: 1rem;
        border-radius: 0 12px 12px 0;
        color: var(--success);
        margin: 0.75rem 0;
    }
    
    .msg-error {
        background: rgba(239, 68, 68, 0.1);
        border: 1px solid rgba(239, 68, 68, 0.3);
        border-left: 4px solid var(--error);
        padding: 1rem;
        border-radius: 0 12px 12px 0;
        margin: 0.75rem 0;
    }
    
    .msg-ai {
        background: rgba(168, 85, 247, 0.1);
        border: 1px solid rgba(168, 85, 247, 0.3);
        border-left: 4px solid var(--purple);
        padding: 1rem;
        border-radius: 0 12px 12px 0;
        margin: 0.75rem 0;
    }
    
    .timer {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.5rem;
        font-weight: 600;
        color: var(--text-secondary);
        padding: 0.5rem 1rem;
        background: var(--bg-card);
        border-radius: 8px;
        border: 1px solid var(--border);
    }
    
    .topics-grid { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 1rem; }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    [data-testid="collapsedControl"] {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 8px;
    }
    
    .stTextInput input {
        background: var(--bg-card) !important;
        border: 1px solid var(--border) !important;
        border-radius: 10px !important;
        color: var(--text-primary) !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stButton"] > button {
        background: var(--bg-card);
        border: 1px solid var(--border);
        color: var(--text-secondary);
        font-size: 0.85rem;
        text-align: left;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
</style>
""", unsafe_allow_html=True)

# SESSION STATE
if "progress" not in st.session_state:
    loaded = load_progress()
    st.session_state.progress = loaded if loaded else get_default_progress()

if "stage" not in st.session_state:
    st.session_state.stage = None
if "q_index" not in st.session_state:
    st.session_state.q_index = 0
if "passed" not in st.session_state:
    st.session_state.passed = False
if "show_celebration" not in st.session_state:
    st.session_state.show_celebration = False
if "show_hint" not in st.session_state:
    st.session_state.show_hint = 0
if "show_solution" not in st.session_state:
    st.session_state.show_solution = False
if "timer_start" not in st.session_state:
    st.session_state.timer_start = None
if "selected_tag" not in st.session_state:
    st.session_state.selected_tag = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "ai_feedback" not in st.session_state:
    st.session_state.ai_feedback = None
if "ai_hint" not in st.session_state:
    st.session_state.ai_hint = None
if "interview_mode" not in st.session_state:
    st.session_state.interview_mode = False
if "ai_explanation" not in st.session_state:
    st.session_state.ai_explanation = None
if "show_chat" not in st.session_state:
    st.session_state.show_chat = True

DIFFICULTIES = ["Basic", "Intermediate", "Advanced"]
DIFFICULTY_COLORS = {"Basic": "#10b981", "Intermediate": "#f59e0b", "Advanced": "#ef4444"}


def render_tags(tags):
    return "".join([f'<span class="tag">{tag}</span>' for tag in tags])

def get_status_text(stage, q_idx):
    if q_idx in st.session_state.progress[stage]["completed"]:
        return "done", "✓"
    elif q_idx in st.session_state.progress[stage]["skipped"]:
        return "skipped", "–"
    return "", ""

def get_progress_stats(stage):
    total = len(QUESTIONS[stage])
    completed = len(st.session_state.progress[stage]["completed"])
    skipped = len(st.session_state.progress[stage]["skipped"])
    return total, completed, skipped

def is_level_complete(stage):
    total, completed, skipped = get_progress_stats(stage)
    return (completed + skipped) >= total

def get_next_unanswered(stage):
    for i in range(len(QUESTIONS[stage])):
        if (i not in st.session_state.progress[stage]["completed"] and 
            i not in st.session_state.progress[stage]["skipped"]):
            return i
    return 0

def navigate_to(stage, q_idx):
    st.session_state.stage = stage
    st.session_state.q_index = q_idx
    st.session_state.passed = False
    st.session_state.show_celebration = False
    st.session_state.show_hint = 0
    st.session_state.show_solution = False
    st.session_state.timer_start = time.time()
    st.session_state.chat_history = []
    st.session_state.ai_feedback = None
    st.session_state.ai_hint = None
    st.session_state.ai_explanation = None

def reset_level(stage):
    st.session_state.progress[stage] = {"completed": set(), "skipped": set(), "times": {}}
    st.session_state.q_index = 0
    st.session_state.passed = False
    st.session_state.show_celebration = False
    st.session_state.timer_start = time.time()
    st.session_state.chat_history = []
    save_progress(st.session_state.progress)

def reset_all_progress():
    for stage in DIFFICULTIES:
        st.session_state.progress[stage] = {"completed": set(), "skipped": set(), "times": {}}
    st.session_state.stage = None
    st.session_state.q_index = 0
    st.session_state.passed = False
    st.session_state.show_celebration = False
    st.session_state.timer_start = None
    st.session_state.chat_history = []
    st.session_state.ai_feedback = None
    st.session_state.ai_hint = None
    st.session_state.ai_explanation = None
    save_progress(st.session_state.progress)


# SIDEBAR
with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:1rem 0;">
        <div style="font-size:2rem;margin-bottom:0.5rem">⚡</div>
        <div style="font-size:1.5rem;font-weight:700;background:linear-gradient(135deg,#ff6b6b,#a855f7);-webkit-background-clip:text;-webkit-text-fill-color:transparent">PyCode</div>
    </div>
    """, unsafe_allow_html=True)
    
    if GROQ_AVAILABLE:
        st.markdown('<div style="text-align:center"><span class="ai-badge">✨ Groq AI</span></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div style="text-align:center"><span class="ai-badge" style="background:linear-gradient(135deg,#14b8a6,#3b82f6)">🤖 AI Built-in</span></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("##### AI Features")
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.show_chat = st.toggle("Chat", value=st.session_state.show_chat)
    with col2:
        st.session_state.interview_mode = st.toggle("Interview", value=st.session_state.interview_mode)
    
    st.markdown("---")
    
    st.markdown("##### Filter by Topic")
    tag_counts = count_questions_by_tag()
    tag_options = ["All Topics"] + [f"{tag} ({tag_counts[tag]})" for tag in ALL_TAGS if tag_counts[tag] > 0]
    selected = st.selectbox("", tag_options, key="tag_filter", label_visibility="collapsed")
    
    if selected != "All Topics":
        st.session_state.selected_tag = selected.split(" (")[0]
    else:
        st.session_state.selected_tag = None
    
    st.markdown("---")
    
    for difficulty in DIFFICULTIES:
        total, completed, skipped = get_progress_stats(difficulty)
        pct = (completed + skipped) / total if total > 0 else 0
        
        with st.expander(f"● {difficulty} — {completed}/{total}", expanded=(st.session_state.stage == difficulty)):
            st.progress(pct)
            st.caption(f"✓ {completed} solved  •  – {skipped} skipped")
            
            for q_idx, q_data in enumerate(QUESTIONS[difficulty]):
                if st.session_state.selected_tag:
                    if st.session_state.selected_tag not in q_data.get("tags", []):
                        continue
                
                _, status_icon = get_status_text(difficulty, q_idx)
                is_current = (st.session_state.stage == difficulty and st.session_state.q_index == q_idx)
                
                prefix = "▸ " if is_current else "  "
                best = get_best_time(st.session_state.progress, difficulty, q_idx)
                time_str = f" • {format_time(best)}" if best else ""
                
                if st.button(f"{prefix}Q{q_idx + 1} {status_icon}{time_str}", key=f"nav_{difficulty}_{q_idx}", use_container_width=True):
                    navigate_to(difficulty, q_idx)
                    st.rerun()
    
    st.markdown("---")
    
    stats = get_stats(st.session_state.progress)
    st.markdown(f"""
    <div style="text-align:center;padding:1rem;background:var(--bg-card);border-radius:12px;border:1px solid var(--border)">
        <div style="font-size:2rem;font-weight:700;background:linear-gradient(135deg,#10b981,#14b8a6);-webkit-background-clip:text;-webkit-text-fill-color:transparent">{stats['completion_rate']:.0f}%</div>
        <div style="font-size:0.75rem;color:var(--text-secondary);text-transform:uppercase">Complete</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("")
    
    if st.session_state.stage:
        if st.button("↺ Reset Level", use_container_width=True):
            reset_level(st.session_state.stage)
            st.rerun()
    
    if st.button("⌂ Home", use_container_width=True):
        st.session_state.stage = None
        st.session_state.timer_start = None
        st.session_state.chat_history = []
        st.rerun()


# MAIN LAYOUT
if st.session_state.show_chat:
    main_col, chat_col = st.columns([2.2, 1])
else:
    main_col = st.container()
    chat_col = None
    _, toggle_col = st.columns([8, 1])
    with toggle_col:
        if st.button("💬 Chat", key="show_chat_btn"):
            st.session_state.show_chat = True
            st.rerun()

with main_col:
    # HOME SCREEN
    if st.session_state.stage is None:
        st.markdown("""
        <div style="text-align:center;padding:2rem 0">
            <div style="font-size:3.5rem;font-weight:700;background:linear-gradient(135deg,#ff6b6b 0%,#a855f7 50%,#14b8a6 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent">
                Python Coding Challenge
            </div>
            <div style="font-size:1.1rem;color:var(--text-secondary)">
                Master Python through hands-on practice with AI assistance
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        stats = get_stats(st.session_state.progress)
        
        cols = st.columns(4)
        stat_data = [
            (stats['total_questions'], "Total", "#ff6b6b"),
            (stats['total_completed'], "Solved", "#10b981"),
            (stats['total_skipped'], "Skipped", "#f59e0b"),
            (f"{stats['completion_rate']:.0f}%", "Progress", "#a855f7")
        ]
        
        for i, (value, label, color) in enumerate(stat_data):
            with cols[i]:
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-value" style="background:linear-gradient(135deg,{color},#14b8a6);-webkit-background-clip:text;-webkit-text-fill-color:transparent">{value}</div>
                    <div class="stat-label">{label}</div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### Select Difficulty")
        
        diff_cols = st.columns(3)
        for idx, difficulty in enumerate(DIFFICULTIES):
            with diff_cols[idx]:
                total, completed, skipped = get_progress_stats(difficulty)
                color = DIFFICULTY_COLORS[difficulty]
                pct = (completed + skipped) / total if total > 0 else 0
                
                st.markdown(f"""
                <div class="diff-card">
                    <div style="display:flex;align-items:center;gap:10px;margin-bottom:1rem">
                        <div style="width:14px;height:14px;border-radius:50%;background:{color}"></div>
                        <span style="font-size:1.3rem;font-weight:600">{difficulty}</span>
                    </div>
                    <div style="color:var(--text-secondary)">{total} questions</div>
                </div>
                """, unsafe_allow_html=True)
                
                if completed > 0 or skipped > 0:
                    st.progress(pct)
                    st.caption(f"{completed} solved • {skipped} skipped")
                
                if st.button("Start →", key=f"start_{difficulty}", use_container_width=True, type="primary"):
                    navigate_to(difficulty, get_next_unanswered(difficulty))
                    st.rerun()
        
        st.markdown("---")
        st.markdown("### Topics")
        tags_html = "".join([f'<span class="tag">{tag} ({count})</span>' for tag, count in tag_counts.items() if count > 0])
        st.markdown(f'<div class="topics-grid">{tags_html}</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        if GROQ_AVAILABLE:
            st.markdown("""
            <div style="background:linear-gradient(135deg,rgba(168,85,247,0.1),rgba(255,107,107,0.1));border:1px solid rgba(168,85,247,0.3);border-radius:16px;padding:1.5rem;display:flex;align-items:center;gap:1.5rem">
                <div style="font-size:2.5rem">✨</div>
                <div style="flex:1">
                    <div style="font-weight:600;font-size:1.1rem">Groq AI Enabled</div>
                    <div style="font-size:0.9rem;color:var(--text-secondary)">Enhanced AI: code reviews, smart hints, bug detection, AI tutor</div>
                </div>
                <span class="ai-badge">ACTIVE</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background:linear-gradient(135deg,rgba(20,184,166,0.1),rgba(59,130,246,0.1));border:1px solid rgba(20,184,166,0.3);border-radius:16px;padding:1.5rem;display:flex;align-items:center;gap:1.5rem">
                <div style="font-size:2.5rem">🤖</div>
                <div style="flex:1">
                    <div style="font-weight:600;font-size:1.1rem">Built-in AI Assistant</div>
                    <div style="font-size:0.9rem;color:var(--text-secondary)">Smart hints, code review, debugging help - no API key needed!</div>
                </div>
                <code style="font-size:0.75rem;background:var(--bg-elevated);padding:0.5rem;border-radius:6px;color:var(--text-muted)">Optional: GROQ_API_KEY</code>
            </div>
            """, unsafe_allow_html=True)
        
        if stats['total_completed'] > 0 or stats['total_skipped'] > 0:
            st.markdown("")
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("🔄 Restart All Progress", use_container_width=True):
                    reset_all_progress()
                    st.rerun()
    
    # CELEBRATION SCREEN
    elif st.session_state.show_celebration:
        stage = st.session_state.stage
        total, completed, skipped = get_progress_stats(stage)
        accuracy = (completed / total * 100) if total > 0 else 0
        
        st.markdown(f"""
        <div style="text-align:center;padding:3rem 0">
            <div style="font-size:4rem">🎉</div>
            <div style="font-size:2.5rem;font-weight:700;background:linear-gradient(135deg,#10b981,#14b8a6);-webkit-background-clip:text;-webkit-text-fill-color:transparent">
                Level Complete!
            </div>
            <div style="color:var(--text-secondary);margin-top:0.5rem">
                You've finished {stage} difficulty
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        cols = st.columns(3)
        with cols[0]:
            st.metric("Total", total)
        with cols[1]:
            st.metric("Solved", completed, delta=f"{accuracy:.0f}%")
        with cols[2]:
            st.metric("Skipped", skipped)
        
        st.markdown("---")
        
        cols = st.columns(3)
        with cols[0]:
            if st.button("↺ Restart Level", use_container_width=True):
                reset_level(stage)
                st.rerun()
        with cols[1]:
            if st.button("⌂ Home", use_container_width=True):
                st.session_state.stage = None
                st.session_state.show_celebration = False
                st.rerun()
        with cols[2]:
            idx = DIFFICULTIES.index(stage)
            if idx < len(DIFFICULTIES) - 1:
                if st.button(f"→ {DIFFICULTIES[idx + 1]}", use_container_width=True, type="primary"):
                    navigate_to(DIFFICULTIES[idx + 1], get_next_unanswered(DIFFICULTIES[idx + 1]))
                    st.rerun()
    
    # QUESTION SCREEN
    else:
        stage = st.session_state.stage
        q_index = st.session_state.q_index
        data = QUESTIONS[stage][q_index]
        total, completed, skipped = get_progress_stats(stage)
        
        # TOP NAVIGATION BAR
        nav_cols = st.columns([1, 1, 4, 1, 1])
        with nav_cols[0]:
            if st.button("⌂ Home", key="top_home", use_container_width=True):
                st.session_state.stage = None
                st.session_state.timer_start = None
                st.session_state.chat_history = []
                st.rerun()
        with nav_cols[1]:
            if st.button("↺ Restart", key="top_restart", use_container_width=True):
                reset_level(stage)
                st.rerun()
        with nav_cols[2]:
            color = DIFFICULTY_COLORS[stage]
            st.markdown(f'<div style="text-align:center;padding:0.5rem"><span style="color:{color};font-weight:600">{stage}</span> • Question {q_index + 1} of {total}</div>', unsafe_allow_html=True)
        with nav_cols[3]:
            if st.button("← Prev", key="top_prev", use_container_width=True, disabled=(q_index == 0)):
                navigate_to(stage, q_index - 1)
                st.rerun()
        with nav_cols[4]:
            if st.button("Next →", key="top_next", use_container_width=True, disabled=(q_index >= total - 1)):
                navigate_to(stage, q_index + 1)
                st.rerun()
        
        st.markdown("---")
        
        if st.session_state.timer_start is None:
            st.session_state.timer_start = time.time()
        
        col1, col2 = st.columns([3, 1])
        with col1:
            mode_badge = '<span class="ai-badge">Interview</span>' if st.session_state.interview_mode else ''
            st.markdown(f"## {data['question']} {mode_badge}", unsafe_allow_html=True)
        
        with col2:
            if not st.session_state.passed:
                elapsed = time.time() - st.session_state.timer_start
                st.markdown(f'<div class="timer">{format_time(elapsed)}</div>', unsafe_allow_html=True)
            else:
                best = get_best_time(st.session_state.progress, stage, q_index)
                if best:
                    st.markdown(f'<div class="timer">Best: {format_time(best)}</div>', unsafe_allow_html=True)
        
        st.progress((completed + skipped) / total if total > 0 else 0)
        
        if data.get("tags"):
            st.markdown(f'<div style="margin:0.5rem 0">{render_tags(data["tags"])}</div>', unsafe_allow_html=True)
        
        if data.get("time_complexity") or data.get("space_complexity"):
            complexity = []
            if data.get("time_complexity"):
                complexity.append(f"Time: {data['time_complexity']}")
            if data.get("space_complexity"):
                complexity.append(f"Space: {data['space_complexity']}")
            st.caption(" • ".join(complexity))
        
        st.markdown("---")
        
        if data["test_cases"]:
            sample = data["test_cases"][0][0]
            params = "" if len(sample) == 0 else "n" if len(sample) == 1 else "a, b" if len(sample) == 2 else ", ".join([f"arg{i+1}" for i in range(len(sample))])
        else:
            params = "n"
        
        template = f"def {data['function']}({params}):\n    # Your code here\n    pass"
        
        st.markdown("""
        <div class="code-editor-container">
            <div class="code-header">
                <span class="code-dot dot-close"></span>
                <span class="code-dot dot-min"></span>
                <span class="code-dot dot-max"></span>
                <span class="code-title">solution.py</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        user_code = st.text_area("", value=template, height=200, key=f"code_{stage}_{q_index}", label_visibility="collapsed")
        
        btn_cols = st.columns(5)
        with btn_cols[0]:
            run_clicked = st.button("▶ Run", type="primary", use_container_width=True)
        with btn_cols[1]:
            skip_clicked = st.button("→ Skip", use_container_width=True)
        with btn_cols[2]:
            if st.session_state.passed or q_index in st.session_state.progress[stage]["completed"]:
                next_clicked = st.button("→ Next", type="primary", use_container_width=True)
            else:
                next_clicked = False
        with btn_cols[3]:
            hint_clicked = st.button("💡 Hint", use_container_width=True)
        with btn_cols[4]:
            if st.session_state.passed and data.get("solution"):
                explain_clicked = st.button("📖 Explain", use_container_width=True)
            else:
                explain_clicked = False
        
        if hint_clicked:
            with st.spinner("Thinking..."):
                try:
                    if GROQ_AVAILABLE:
                        st.session_state.ai_hint = groq_smart_hint(user_code, data['question'], data['function'], data.get('hints', []), st.session_state.show_hint + 1)
                    else:
                        st.session_state.ai_hint = builtin_smart_hint(user_code, data['question'], data['function'], data.get('hints', []), st.session_state.show_hint + 1)
                    st.session_state.show_hint += 1
                except Exception as e:
                    st.session_state.ai_hint = f"Error: {e}"
        
        if st.session_state.ai_hint:
            st.markdown(f'<div class="msg-ai">{st.session_state.ai_hint}</div>', unsafe_allow_html=True)
        
        if run_clicked:
            passed, message = evaluate_user_code(user_code, data["function"], data["test_cases"])
            
            if passed:
                elapsed = time.time() - st.session_state.timer_start
                st.markdown(f'<div class="msg-success">✓ Passed — {format_time(elapsed)}</div>', unsafe_allow_html=True)
                
                st.session_state.passed = True
                st.session_state.progress[stage]["completed"].add(q_index)
                st.session_state.progress[stage]["skipped"].discard(q_index)
                st.session_state.progress = save_question_time(st.session_state.progress, stage, q_index, elapsed)
                save_progress(st.session_state.progress)
                
                with st.spinner("Reviewing..."):
                    try:
                        if GROQ_AVAILABLE:
                            st.session_state.ai_feedback = groq_code_review(user_code, data['question'], data['function'], elapsed)
                        else:
                            st.session_state.ai_feedback = builtin_code_review(user_code, data['question'], data['function'], elapsed)
                    except Exception as e:
                        st.session_state.ai_feedback = None  # Silently fail on AI review
                
                if is_level_complete(stage):
                    st.session_state.show_celebration = True
                    st.rerun()
            else:
                st.session_state.passed = False
                st.markdown(f'<div class="msg-error">{message}</div>', unsafe_allow_html=True)
                
                with st.spinner("Analyzing..."):
                    try:
                        if GROQ_AVAILABLE:
                            bug = groq_bug_detection(user_code, data['question'], data['function'], message, data["test_cases"][0][0] if data["test_cases"] else None, data["test_cases"][0][1] if data["test_cases"] else None, None)
                        else:
                            bug = builtin_bug_hint(user_code, message, data['question'], data['function'])
                        st.markdown(f'<div class="msg-ai"><strong>🔍 Analysis:</strong><br>{bug}</div>', unsafe_allow_html=True)
                    except Exception as e:
                        pass  # Silently fail on bug detection
        
        if st.session_state.ai_feedback:
            st.markdown(f'<div class="msg-ai">{st.session_state.ai_feedback}</div>', unsafe_allow_html=True)
        
        if explain_clicked:
            with st.spinner("Generating explanation..."):
                try:
                    if GROQ_AVAILABLE:
                        st.session_state.ai_explanation = groq_code_explanation(data.get('solution', ''), data['question'], data['function'])
                    else:
                        st.session_state.ai_explanation = f"**Solution for {data['function']}:**\n\nReview the solution code below and trace through the logic step by step."
                except Exception as e:
                    st.session_state.ai_explanation = None  # Silently fail
            st.session_state.show_solution = True
        
        if skip_clicked:
            if q_index not in st.session_state.progress[stage]["completed"]:
                st.session_state.progress[stage]["skipped"].add(q_index)
                save_progress(st.session_state.progress)
            if is_level_complete(stage):
                st.session_state.show_celebration = True
                st.rerun()
            else:
                navigate_to(stage, (q_index + 1) % total)
                st.rerun()
        
        if next_clicked:
            if is_level_complete(stage):
                st.session_state.show_celebration = True
                st.rerun()
            else:
                navigate_to(stage, (q_index + 1) % total)
                st.rerun()
        
        if st.session_state.passed or q_index in st.session_state.progress[stage]["completed"]:
            if not st.session_state.ai_feedback:
                st.markdown('<div class="msg-success">✓ Completed — Click Next to continue</div>', unsafe_allow_html=True)
            
            if st.session_state.show_solution and data.get("solution"):
                st.markdown("#### Solution")
                st.code(data["solution"], language="python")
                if st.session_state.ai_explanation:
                    st.markdown(f'<div class="msg-ai">{st.session_state.ai_explanation}</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("#### Test Cases")
        for inputs, expected in data["test_cases"][:3]:
            st.code(f"Input: {inputs}\nExpected: {expected}", language="text")


# CHAT PANEL
if chat_col:
    with chat_col:
        header_col1, header_col2 = st.columns([4, 1])
        with header_col1:
            st.markdown("""
            <div style="display:flex;align-items:center;gap:10px;padding:0.5rem 0">
                <div style="width:10px;height:10px;border-radius:50%;background:linear-gradient(135deg,#a855f7,#ff6b6b);animation:pulse 2s infinite"></div>
                <span style="font-weight:600;font-size:1.1rem">AI Tutor</span>
            </div>
            """, unsafe_allow_html=True)
        with header_col2:
            if st.button("✕", key="close_chat"):
                st.session_state.show_chat = False
                st.rerun()
        
        if GROQ_AVAILABLE:
            st.markdown('<div style="background:rgba(168,85,247,0.15);border:1px solid rgba(168,85,247,0.3);border-radius:8px;padding:0.5rem;margin-bottom:0.5rem;font-size:0.75rem;color:#a855f7">✨ Groq AI</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div style="background:rgba(20,184,166,0.15);border:1px solid rgba(20,184,166,0.3);border-radius:8px;padding:0.5rem;margin-bottom:0.5rem;font-size:0.75rem;color:#14b8a6">🤖 Built-in Assistant</div>', unsafe_allow_html=True)
        
        if st.session_state.interview_mode:
            st.markdown('<div style="background:rgba(239,68,68,0.15);border:1px solid rgba(239,68,68,0.3);border-radius:8px;padding:0.75rem;margin:0.5rem 0"><div style="font-weight:600;font-size:0.85rem;color:#ef4444">🎯 Interview Mode</div></div>', unsafe_allow_html=True)
        
        chat_container = st.container(height=350)
        with chat_container:
            if not st.session_state.chat_history:
                st.markdown('<div style="text-align:center;padding:2rem;color:var(--text-muted)"><div style="font-size:2rem;margin-bottom:0.5rem">💭</div><div>Start a conversation</div></div>', unsafe_allow_html=True)
            
            for msg in st.session_state.chat_history:
                if msg["role"] == "user":
                    st.markdown(f'<div style="display:flex;justify-content:flex-end;margin:0.5rem 0"><div style="background:rgba(20,184,166,0.2);border:1px solid rgba(20,184,166,0.3);padding:0.75rem;border-radius:12px 12px 4px 12px;max-width:85%;font-size:0.9rem">{msg["content"]}</div></div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div style="display:flex;justify-content:flex-start;margin:0.5rem 0"><div style="background:rgba(168,85,247,0.15);border:1px solid rgba(168,85,247,0.3);padding:0.75rem;border-radius:12px 12px 12px 4px;max-width:85%;font-size:0.9rem">{msg["content"]}</div></div>', unsafe_allow_html=True)
        
        user_msg = st.text_input("", placeholder="Ask anything...", key="chat_input", label_visibility="collapsed")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            send_clicked = st.button("Send →", use_container_width=True, type="primary")
        with col2:
            clear_clicked = st.button("Clear", use_container_width=True)
        
        if send_clicked and user_msg:
            st.session_state.chat_history.append({"role": "user", "content": user_msg})
            
            with st.spinner(""):
                try:
                    if st.session_state.stage is not None:
                        data = QUESTIONS[st.session_state.stage][st.session_state.q_index]
                        current_code = st.session_state.get(f"code_{st.session_state.stage}_{st.session_state.q_index}", "")
                        
                        if GROQ_AVAILABLE:
                            response = groq_tutor_response(user_msg, data['question'], data['function'], current_code, st.session_state.chat_history[:-1], st.session_state.interview_mode)
                        else:
                            response = builtin_chat(user_msg, data['question'], data['function'], current_code, st.session_state.interview_mode)
                    else:
                        # No problem selected - still allow general Python questions
                        response = builtin_chat(user_msg, "", "", "", False)
                    st.session_state.chat_history.append({"role": "assistant", "content": response})
                except Exception as e:
                    st.session_state.chat_history.append({"role": "assistant", "content": f"Error: {str(e)[:100]}"})
            
            st.rerun()
        
        if clear_clicked:
            st.session_state.chat_history = []
            st.rerun()
        
        st.markdown('<div style="font-size:0.75rem;color:var(--text-muted);margin:0.5rem 0">Quick prompts:</div>', unsafe_allow_html=True)
        qc = st.columns(2)
        with qc[0]:
            if st.button("Explain problem", use_container_width=True, key="q1"):
                st.session_state.chat_history.append({"role": "user", "content": "Explain this problem to me"})
                st.rerun()
        with qc[1]:
            if st.button("Give hint", use_container_width=True, key="q2"):
                st.session_state.chat_history.append({"role": "user", "content": "Give me a hint"})
                st.rerun()
