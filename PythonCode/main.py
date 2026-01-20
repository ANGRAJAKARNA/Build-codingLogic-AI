# main.py
"""
PyCode - AI-Powered Python Coding Challenge Platform
2-Panel Phone UI with AI Chat Modal
"""

import streamlit as st
import time
import os
import random
import html
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
    store_qa_interaction,
    record_feedback,
    get_learning_stats,
)

st.set_page_config(page_title="PyCode AI", page_icon="🤖", layout="wide", initial_sidebar_state="collapsed")

# CSS Styles - Futuristic Neon Cyber Design
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800;900&family=Rajdhani:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');
    
    :root {
    --bg-deep: #030508;
    --bg-dark: #0a0f1a;
    --bg-card: rgba(10, 20, 40, 0.85);
    --neon-cyan: #00f5ff;
    --neon-purple: #bf00ff;
    --neon-pink: #ff00aa;
    --neon-green: #00ff88;
    --neon-orange: #ff6b00;
    --text: #e8f4f8;
    --text-dim: #8fa3b8;
    --text-muted: #4a6380;
    --glass: rgba(255, 255, 255, 0.03);
    --glass-border: rgba(255, 255, 255, 0.08);
}

#MainMenu, footer, [data-testid="stToolbar"], [data-testid="stDecoration"] { display: none !important; }
[data-testid="stSidebar"] { display: none !important; }

/* ========== ANIMATED BACKGROUND ========== */
.stApp { 
    background: 
        radial-gradient(ellipse at 20% 80%, rgba(0, 245, 255, 0.08) 0%, transparent 50%),
        radial-gradient(ellipse at 80% 20%, rgba(191, 0, 255, 0.08) 0%, transparent 50%),
        radial-gradient(ellipse at 50% 50%, rgba(0, 255, 136, 0.03) 0%, transparent 60%),
        linear-gradient(180deg, #030508 0%, #0a0f1a 50%, #050810 100%) !important;
    color: var(--text) !important;
    min-height: 100vh;
}

.main .block-container { 
    padding: 0.8rem 2rem !important; 
    max-width: 100% !important; 
}

* { font-family: 'Rajdhani', -apple-system, sans-serif !important; }
.stApp *, [data-testid="stVerticalBlock"], .stMarkdown, p, span, div { color: var(--text) !important; }

/* ========== FUTURISTIC CARD 1 - Problems ========== */
[data-testid="column"]:nth-child(1) > div:first-child {
    background: linear-gradient(135deg, rgba(0, 245, 255, 0.05) 0%, rgba(8, 16, 32, 0.98) 50%, rgba(0, 255, 136, 0.03) 100%) !important;
    border: 2px solid rgba(0, 245, 255, 0.35) !important;
    -webkit-border-radius: 20px !important;
    border-radius: 20px !important;
    padding: 20px !important;
    min-height: 700px;
    margin: 0 10px;
    -webkit-backdrop-filter: blur(20px);
    backdrop-filter: blur(20px);
    -webkit-box-shadow: 
        0 0 50px rgba(0, 245, 255, 0.2),
        0 20px 60px rgba(0, 0, 0, 0.5),
        inset 0 1px 0 rgba(0, 245, 255, 0.15),
        inset 0 0 30px rgba(0, 245, 255, 0.03);
    box-shadow: 
        0 0 50px rgba(0, 245, 255, 0.2),
        0 20px 60px rgba(0, 0, 0, 0.5),
        inset 0 1px 0 rgba(0, 245, 255, 0.15),
        inset 0 0 30px rgba(0, 245, 255, 0.03) !important;
    position: relative;
    overflow: hidden;
}

/* ========== FUTURISTIC CARD 2 - Editor ========== */
[data-testid="column"]:nth-child(2) > div:first-child {
    background: linear-gradient(135deg, rgba(191, 0, 255, 0.05) 0%, rgba(8, 16, 32, 0.98) 50%, rgba(255, 0, 170, 0.03) 100%) !important;
    border: 2px solid rgba(191, 0, 255, 0.35) !important;
    -webkit-border-radius: 20px !important;
    border-radius: 20px !important;
    padding: 20px !important;
    min-height: 700px;
    margin: 0 10px;
    -webkit-backdrop-filter: blur(20px);
    backdrop-filter: blur(20px);
    -webkit-box-shadow: 
        0 0 50px rgba(191, 0, 255, 0.2),
        0 20px 60px rgba(0, 0, 0, 0.5),
        inset 0 1px 0 rgba(191, 0, 255, 0.15),
        inset 0 0 30px rgba(191, 0, 255, 0.03);
    box-shadow: 
        0 0 50px rgba(191, 0, 255, 0.2),
        0 20px 60px rgba(0, 0, 0, 0.5),
        inset 0 1px 0 rgba(191, 0, 255, 0.15),
        inset 0 0 30px rgba(191, 0, 255, 0.03) !important;
    position: relative;
    overflow: hidden;
}

@keyframes scanline {
    0% { transform: translateX(-100%); }
    100% { transform: translateX(100%); }
}

/* ========== HEADER STYLES ========== */
.card-header { 
    display: flex;
    justify-content: space-between; 
    align-items: center;
    margin-bottom: 18px; 
    padding-bottom: 14px;
    border-bottom: 1px solid rgba(0, 245, 255, 0.15);
}
.card-title { 
    font-family: 'Orbitron', sans-serif !important;
    font-size: 1.3rem; 
        font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    background: linear-gradient(90deg, var(--neon-cyan), var(--neon-green));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    text-shadow: 0 0 30px rgba(0, 245, 255, 0.5);
}
.card-badge {
    padding: 6px 16px;
    border-radius: 4px;
    font-family: 'Orbitron', sans-serif !important;
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 2px;
    background: rgba(0, 245, 255, 0.1);
    color: var(--neon-cyan);
    border: 1px solid rgba(0, 245, 255, 0.3);
    text-shadow: 0 0 10px var(--neon-cyan);
    animation: pulse-glow 2s ease-in-out infinite;
}
@keyframes pulse-glow {
    0%, 100% { box-shadow: 0 0 5px rgba(0, 245, 255, 0.3); }
    50% { box-shadow: 0 0 20px rgba(0, 245, 255, 0.5), 0 0 30px rgba(0, 245, 255, 0.2); }
}

/* ========== CYBER STATS ========== */
.stats-row { display: flex; gap: 12px; margin-bottom: 18px; }
.stat-card {
    flex: 1; 
    background: linear-gradient(135deg, rgba(0, 245, 255, 0.05) 0%, rgba(0, 20, 40, 0.8) 100%);
    border: 1px solid rgba(0, 245, 255, 0.2);
    border-radius: 12px;
    padding: 16px 12px; 
    text-align: center;
    position: relative;
    overflow: hidden;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.stat-card:hover {
    transform: translateY(-4px) scale(1.02);
    border-color: var(--neon-cyan);
    box-shadow: 0 0 30px rgba(0, 245, 255, 0.3), inset 0 0 20px rgba(0, 245, 255, 0.05);
}
.stat-card::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--neon-cyan), transparent);
}
.stat-num { 
    font-family: 'Orbitron', sans-serif !important;
    font-size: 2.2rem; 
    font-weight: 800; 
    background: linear-gradient(180deg, #fff 0%, var(--neon-cyan) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 0 0 40px rgba(0, 245, 255, 0.8);
}
    .stat-label {
    font-family: 'Orbitron', sans-serif !important;
    font-size: 9px; 
    color: var(--text-dim); 
        text-transform: uppercase;
    letter-spacing: 2px; 
    margin-top: 8px; 
}

/* ========== SECTION TITLES ========== */
.section-title { 
    font-family: 'Orbitron', sans-serif !important;
    font-size: 10px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 3px; 
    margin: 20px 0 12px; 
    padding: 8px 0 8px 14px; 
    border-left: 3px solid;
    color: var(--text-dim);
    background: linear-gradient(90deg, rgba(0, 245, 255, 0.05) 0%, transparent 100%);
}
.sec-cyan { border-left-color: var(--neon-cyan); color: var(--neon-cyan); }
.sec-purple { border-left-color: var(--neon-purple); color: var(--neon-purple); }
.sec-coral { border-left-color: var(--neon-pink); color: var(--neon-pink); }

/* ========== QUESTION CARDS ========== */
.q-card { 
    background: linear-gradient(135deg, rgba(0, 245, 255, 0.02) 0%, rgba(10, 15, 30, 0.9) 100%);
    border: 1px solid rgba(0, 245, 255, 0.1); 
    border-radius: 10px; 
    padding: 14px 16px; 
    margin-bottom: 10px; 
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}
.q-card::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 3px;
    background: linear-gradient(180deg, var(--neon-cyan), var(--neon-green));
    opacity: 0;
    transition: opacity 0.3s;
}
.q-card:hover { 
    background: linear-gradient(135deg, rgba(0, 245, 255, 0.08) 0%, rgba(10, 20, 40, 0.95) 100%);
    border-color: rgba(0, 245, 255, 0.3);
    transform: translateX(8px);
    box-shadow: 0 0 25px rgba(0, 245, 255, 0.15);
}
.q-card:hover::before { opacity: 1; }
.q-card-active { 
    background: linear-gradient(135deg, rgba(0, 255, 136, 0.1) 0%, rgba(10, 20, 40, 0.95) 100%) !important;
    border-color: var(--neon-green) !important;
    box-shadow: 0 0 30px rgba(0, 255, 136, 0.2) !important;
}
.q-header { display: flex; align-items: center; gap: 14px; }
.q-icon { 
    width: 32px; 
    height: 32px; 
    border-radius: 6px; 
    display: flex; 
    align-items: center; 
    justify-content: center;
    font-family: 'Orbitron', sans-serif !important;
    font-size: 12px;
    font-weight: 700;
    background: linear-gradient(135deg, rgba(0, 245, 255, 0.2) 0%, rgba(0, 255, 136, 0.1) 100%);
    color: var(--neon-cyan);
    border: 1px solid rgba(0, 245, 255, 0.3);
    text-shadow: 0 0 10px var(--neon-cyan);
}
.q-title { flex: 1; font-size: 13px; font-weight: 500; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.q-tags { font-size: 10px; color: var(--text-muted); margin-top: 6px; letter-spacing: 0.5px; }

/* ========== PROBLEM BOX ========== */
.problem-box { 
    background: linear-gradient(135deg, rgba(191, 0, 255, 0.05) 0%, rgba(10, 15, 30, 0.9) 100%);
    border: 1px solid rgba(191, 0, 255, 0.2); 
    border-radius: 14px;
    padding: 18px; 
    margin-bottom: 16px;
    position: relative;
}
.problem-box::before {
    content: '';
    position: absolute;
    top: 0; left: 20px; right: 20px;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(191, 0, 255, 0.5), transparent);
}
.problem-title { font-size: 1rem; font-weight: 600; margin-bottom: 14px; line-height: 1.5; }
.badges { display: flex; gap: 8px; flex-wrap: wrap; }
.badge { 
    padding: 5px 14px; 
    border-radius: 4px; 
    font-family: 'Orbitron', sans-serif !important;
    font-size: 9px; 
    font-weight: 600; 
    letter-spacing: 1px;
    text-transform: uppercase;
}
.b-easy { 
    background: rgba(0, 255, 136, 0.1); 
    color: var(--neon-green); 
    border: 1px solid rgba(0, 255, 136, 0.3);
    text-shadow: 0 0 10px rgba(0, 255, 136, 0.5);
}
.b-med { 
    background: rgba(255, 107, 0, 0.1); 
    color: var(--neon-orange); 
    border: 1px solid rgba(255, 107, 0, 0.3);
    text-shadow: 0 0 10px rgba(255, 107, 0, 0.5);
}
.b-hard { 
    background: rgba(255, 0, 170, 0.1); 
    color: var(--neon-pink); 
    border: 1px solid rgba(255, 0, 170, 0.3);
    text-shadow: 0 0 10px rgba(255, 0, 170, 0.5);
}
.b-tag { 
    background: rgba(0, 245, 255, 0.08); 
    color: var(--neon-cyan); 
    border: 1px solid rgba(0, 245, 255, 0.2); 
}

/* ========== CODE EDITOR ========== */
.editor-box { 
    background: rgba(5, 10, 20, 0.9); 
    border: 1px solid rgba(191, 0, 255, 0.2); 
        border-radius: 12px;
        overflow: hidden;
    margin-bottom: 14px;
    }
.editor-header { 
    background: linear-gradient(90deg, rgba(191, 0, 255, 0.1) 0%, rgba(10, 15, 30, 0.9) 100%);
        padding: 12px 16px;
        display: flex;
        align-items: center;
        gap: 8px;
    border-bottom: 1px solid rgba(191, 0, 255, 0.15);
}
.dot { width: 10px; height: 10px; border-radius: 50%; box-shadow: 0 0 10px currentColor; }
.d-r { background: #ff4757; color: #ff4757; }
.d-y { background: #ffa502; color: #ffa502; }
.d-g { background: #2ed573; color: #2ed573; }
.editor-file { 
    margin-left: 14px; 
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 11px; 
    color: var(--neon-purple); 
    letter-spacing: 1px;
}

.timer { 
    text-align: center; 
    font-family: 'Orbitron', sans-serif !important;
    font-size: 1.6rem; 
    font-weight: 700; 
    background: linear-gradient(90deg, var(--neon-cyan), var(--neon-purple));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 0 0 30px rgba(0, 245, 255, 0.5);
    padding: 12px 0;
    letter-spacing: 4px;
}

/* ========== WELCOME SCREEN ========== */
.welcome { text-align: center; padding: 50px 24px; }
.welcome-icon { 
    width: 100px; 
    height: 100px; 
    border-radius: 20px; 
    margin: 0 auto 30px; 
    display: flex; 
    align-items: center; 
    justify-content: center; 
    font-family: 'Orbitron', sans-serif !important;
    font-size: 28px;
    font-weight: 800;
    background: linear-gradient(135deg, rgba(191, 0, 255, 0.2) 0%, rgba(0, 245, 255, 0.1) 100%);
    border: 2px solid;
    border-image: linear-gradient(135deg, var(--neon-purple), var(--neon-cyan)) 1;
    color: var(--neon-purple);
    text-shadow: 0 0 20px var(--neon-purple);
    animation: float 3s ease-in-out infinite, glow-rotate 4s linear infinite;
    box-shadow: 0 0 40px rgba(191, 0, 255, 0.3);
}
@keyframes glow-rotate {
    0%, 100% { box-shadow: 0 0 40px rgba(191, 0, 255, 0.4), 0 0 80px rgba(0, 245, 255, 0.1); }
    50% { box-shadow: 0 0 60px rgba(0, 245, 255, 0.4), 0 0 100px rgba(191, 0, 255, 0.1); }
}
.welcome-title { 
    font-family: 'Orbitron', sans-serif !important;
    font-size: 1.5rem; 
    font-weight: 700; 
    line-height: 1.4; 
    margin-bottom: 14px;
    letter-spacing: 2px;
    background: linear-gradient(90deg, var(--text), var(--neon-cyan));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.welcome-sub { color: var(--text-dim); font-size: 13px; line-height: 1.7; max-width: 300px; margin: 0 auto; }

/* ========== TEXT INPUTS ========== */
    .stTextArea textarea {
        font-family: 'JetBrains Mono', monospace !important;
    font-size: 13px !important; 
    background: rgba(5, 10, 20, 0.8) !important; 
    color: var(--neon-green) !important; 
    border: 1px solid rgba(0, 255, 136, 0.2) !important; 
    border-radius: 10px !important;
    caret-color: var(--neon-green) !important;
}
.stTextArea textarea:focus {
    border-color: var(--neon-green) !important;
    box-shadow: 0 0 20px rgba(0, 255, 136, 0.2), inset 0 0 20px rgba(0, 255, 136, 0.02) !important;
}
.stTextInput input { 
    background: rgba(10, 15, 30, 0.8) !important; 
    border: 1px solid rgba(0, 245, 255, 0.2) !important; 
    border-radius: 10px !important; 
        font-size: 14px !important;
    padding: 14px 16px !important;
    color: var(--text) !important;
}
.stTextInput input:focus { 
    border-color: var(--neon-cyan) !important; 
    box-shadow: 0 0 25px rgba(0, 245, 255, 0.2), inset 0 0 15px rgba(0, 245, 255, 0.02) !important;
}

/* ========== CYBER BUTTONS ========== */
    .stButton > button {
    font-family: 'Orbitron', sans-serif !important;
    font-weight: 600 !important; 
    font-size: 12px !important; 
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    border-radius: 8px !important; 
    padding: 14px 24px !important; 
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    position: relative !important;
    overflow: hidden !important;
}
.stButton > button::before {
    content: '' !important;
    position: absolute !important;
    top: 0 !important; left: -100% !important;
    width: 100% !important; height: 100% !important;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent) !important;
    transition: left 0.5s !important;
}
.stButton > button:hover::before { left: 100% !important; }
.stButton > button:hover { transform: translateY(-3px) !important; }

/* Primary Button - Neon Green */
.stButton > button[kind="primary"] { 
    background: linear-gradient(135deg, rgba(0, 255, 136, 0.9) 0%, rgba(0, 200, 100, 0.9) 100%) !important; 
    color: #030508 !important;
    border: none !important;
    box-shadow: 0 0 30px rgba(0, 255, 136, 0.4), inset 0 0 20px rgba(255, 255, 255, 0.1) !important;
}
.stButton > button[kind="primary"]:hover {
    box-shadow: 0 0 50px rgba(0, 255, 136, 0.6), 0 10px 40px rgba(0, 255, 136, 0.3) !important;
}

/* Secondary Button */
.stButton > button[kind="secondary"] { 
    background: transparent !important; 
    border: 1px solid rgba(0, 245, 255, 0.4) !important; 
    color: var(--neon-cyan) !important;
}
.stButton > button[kind="secondary"]:hover {
    background: rgba(0, 245, 255, 0.1) !important;
    border-color: var(--neon-cyan) !important;
    box-shadow: 0 0 30px rgba(0, 245, 255, 0.3), inset 0 0 15px rgba(0, 245, 255, 0.05) !important;
}

/* Ensure button labels inherit the neon colors */
.stButton > button div[data-testid="stMarkdownContainer"],
.stButton > button p {
    color: inherit !important;
}
.stButton > button[kind="secondary"] div[data-testid="stMarkdownContainer"],
.stButton > button[kind="secondary"] p {
    color: var(--neon-cyan) !important;
}
.stButton > button[kind="primary"] div[data-testid="stMarkdownContainer"],
.stButton > button[kind="primary"] p {
    color: #030508 !important;
}

/* ========== PROGRESS BAR ========== */
.stProgress > div > div { 
    background: linear-gradient(90deg, var(--neon-cyan), var(--neon-green), var(--neon-cyan)) !important;
    background-size: 200% 100% !important;
    animation: progress-glow 2s linear infinite !important;
    border-radius: 4px !important;
    box-shadow: 0 0 15px var(--neon-cyan) !important;
}
@keyframes progress-glow {
    0% { background-position: 0% 0%; }
    100% { background-position: 200% 0%; }
}
.stProgress > div{ 
    background: rgba(0, 245, 255, 0.1) !important; 
    border-radius: 4px !important; 
    height: 8px !important;
    border: 1px solid rgba(0, 245, 255, 0.2) !important;
}

/* ========== MESSAGES ========== */
.msg-ok { 
    background: linear-gradient(135deg, rgba(0, 255, 136, 0.1) 0%, rgba(10, 20, 40, 0.9) 100%);
    border: 1px solid rgba(0, 255, 136, 0.3); 
    border-radius: 10px; 
    padding: 14px 18px; 
    color: var(--neon-green); 
    margin: 12px 0;
    box-shadow: 0 0 20px rgba(0, 255, 136, 0.1);
}
.msg-err { 
    background: linear-gradient(135deg, rgba(255, 0, 170, 0.1) 0%, rgba(10, 20, 40, 0.9) 100%);
    border: 1px solid rgba(255, 0, 170, 0.3);
    border-radius: 10px; 
    padding: 14px 18px; 
    color: var(--neon-pink); 
    margin: 12px 0;
    box-shadow: 0 0 20px rgba(255, 0, 170, 0.1);
}
.msg-hint { 
    background: linear-gradient(135deg, rgba(0, 245, 255, 0.1) 0%, rgba(10, 20, 40, 0.9) 100%);
    border: 1px solid rgba(0, 245, 255, 0.3); 
    border-radius: 10px; 
    padding: 14px 18px; 
    margin: 12px 0; 
    color: var(--neon-cyan);
    box-shadow: 0 0 20px rgba(0, 245, 255, 0.1);
}

/* ========== TEST CASES ========== */
.test-case { 
    background: rgba(10, 15, 30, 0.8);
    border: 1px solid rgba(0, 245, 255, 0.15); 
        border-radius: 8px;
    padding: 12px 16px; 
    margin: 8px 0; 
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 12px;
}
.test-lbl { color: var(--neon-cyan); font-weight: 600; }

/* ========== CHAT MESSAGES ========== */
.chat-msg { 
    padding: 14px 18px; 
    border-radius: 12px; 
    margin: 10px 0; 
    max-width: 85%; 
    font-size: 13px; 
    line-height: 1.6;
}
.chat-msg-user { 
    background: linear-gradient(135deg, var(--neon-green), rgba(0, 200, 100, 0.9));
    color: #030508; 
    margin-left: auto; 
    border-radius: 12px 12px 4px 12px;
    box-shadow: 0 0 20px rgba(0, 255, 136, 0.3);
}
.chat-msg-ai { 
    background: linear-gradient(135deg, rgba(191, 0, 255, 0.1), rgba(10, 20, 40, 0.9));
    border: 1px solid rgba(191, 0, 255, 0.3); 
    border-radius: 12px 12px 12px 4px;
}

/* ========== MODE TOGGLE ========== */
.stRadio > div {
    background: rgba(10, 15, 30, 0.8) !important;
    border: 1px solid rgba(0, 245, 255, 0.2) !important;
    border-radius: 10px !important;
    padding: 4px !important;
}
.stRadio label { 
    font-family: 'Orbitron', sans-serif !important;
    font-size: 12px !important;
    letter-spacing: 1px !important;
}

/* ========== SELECTBOX ========== */
.stSelectbox > div > div {
    background: rgba(10, 15, 30, 0.9) !important;
    border: 1px solid rgba(0, 245, 255, 0.2) !important;
    border-radius: 8px !important;
}
.stSelectbox > div > div:hover {
    border-color: var(--neon-cyan) !important;
}

/* ========== CONTAINER SCROLLBAR ========== */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: rgba(10, 15, 30, 0.5); border-radius: 3px; }
::-webkit-scrollbar-thumb { 
    background: linear-gradient(180deg, var(--neon-cyan), var(--neon-purple)); 
    border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover { background: var(--neon-cyan); }

/* ========== ANIMATIONS ========== */
@keyframes float { 
    0%, 100% { transform: translateY(0) rotate(0deg); } 
    50% { transform: translateY(-10px) rotate(2deg); } 
}

/* ========== SLIDER ========== */
.stSlider > div > div > div {
    background: linear-gradient(90deg, var(--neon-cyan), var(--neon-purple)) !important;
}
.stSlider > div > div > div > div {
    background: var(--neon-cyan) !important;
    box-shadow: 0 0 15px var(--neon-cyan) !important;
    }
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
    "show_chat_modal": False,
    "reopen_chat": False,
    "pending_chat_msg": None,
    "interview_active": False,
    "interview_engine": None,
    "interview_code": "",
    "interview_feedback_shown": False,
    "interview_config": {"difficulty": "mid", "type": "technical", "time_limit": 30},
    "last_achievements": [],
    "new_achievement": None,
    "used_hint_this_problem": False,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# Interview stage metadata
STAGE_INFO_LIST = [
    ("intro", "01", "Introduction", "Read the problem & ask questions", "Clarify requirements, restate the problem, and ask if anything is missing."),
    ("approach", "02", "Approach Discussion", "Explain your solution strategy", "Describe the algorithm, outline edge cases, and justify data choices."),
    ("coding", "03", "Coding Time", "Write your solution code", "Translate your plan into readable Python and explain each section as you write."),
    ("optimization", "04", "Optimization", "Analyze & improve complexity", "Evaluate time/space trade-offs and suggest refinements or alternate algorithms."),
    ("behavioral", "05", "Behavioral", "Answer situational questions", "Use STAR stories, stay concise, and highlight communication skills."),
    ("wrapup", "06", "Wrap Up", "Ask your questions", "Summarize your solution, thank the interviewer, and ask about next steps."),
]
STAGE_INFO = {key: {"icon": icon, "title": title, "description": desc, "goal": goal} for key, icon, title, desc, goal in STAGE_INFO_LIST}
STAGE_ORDER = [key for key, _, _, _, _ in STAGE_INFO_LIST]

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


# ==================== AI CHAT MODAL ====================
# Topic-based quick prompts organized by category
CHAT_PROMPTS = {
    "Python": [
        ("What is Python?", "🐍"),
        ("Explain list comprehension", "📝"),
        ("How do classes work?", "🏗️"),
    ],
    "Selenium": [
        ("What is Selenium?", "🌐"),
        ("Explain XPath locators", "🔍"),
        ("How do waits work?", "⏱️"),
    ],
    "Robot": [
        ("What is Robot Framework?", "🤖"),
        ("Explain keywords", "🔑"),
        ("How to use variables?", "📊"),
    ],
    "Help": [
        ("Give me a hint", "💡"),
        ("Explain this problem", "❓"),
        ("Debug my code", "🐛"),
    ]
}

# Follow-up suggestions based on topic
FOLLOWUP_SUGGESTIONS = {
    "python": ["Show me an example", "What are best practices?", "Common mistakes to avoid?"],
    "selenium": ["Show me code example", "How to handle errors?", "Best practices?"],
    "robot": ["Show me a test case", "How to organize tests?", "What libraries to use?"],
    "default": ["Can you give an example?", "Tell me more", "What's the best practice?"]
}

def get_followups(last_response: str) -> list:
    """Get contextual follow-up suggestions based on last response."""
    resp_lower = last_response.lower()
    if "selenium" in resp_lower or "webdriver" in resp_lower:
        return FOLLOWUP_SUGGESTIONS["selenium"]
    elif "robot" in resp_lower or "keyword" in resp_lower:
        return FOLLOWUP_SUGGESTIONS["robot"]
    elif "python" in resp_lower or "def " in resp_lower:
        return FOLLOWUP_SUGGESTIONS["python"]
    return FOLLOWUP_SUGGESTIONS["default"]

def extract_code_blocks(content: str) -> list:
    """Extract all Python code blocks from a response."""
    import re
    # Find all ```python ... ``` or ``` ... ``` blocks
    pattern = r'```(?:python)?\n?(.*?)```'
    matches = re.findall(pattern, content, re.DOTALL)
    return [m.strip() for m in matches if m.strip()]

def run_python_code_safe(code: str) -> dict:
    """
    Safely execute Python code and return the result.
    Returns dict with 'output', 'error', and 'success' keys.
    """
    import sys
    from io import StringIO
    import traceback
    
    # Restricted globals for safety
    safe_globals = {
        '__builtins__': {
            'print': print, 'len': len, 'range': range, 'str': str, 'int': int,
            'float': float, 'list': list, 'dict': dict, 'set': set, 'tuple': tuple,
            'bool': bool, 'sum': sum, 'max': max, 'min': min, 'abs': abs,
            'sorted': sorted, 'reversed': reversed, 'enumerate': enumerate,
            'zip': zip, 'map': map, 'filter': filter, 'any': any, 'all': all,
            'isinstance': isinstance, 'type': type, 'round': round, 'pow': pow,
            'divmod': divmod, 'chr': chr, 'ord': ord, 'hex': hex, 'bin': bin,
            'True': True, 'False': False, 'None': None,
        }
    }
    
    # Capture stdout
    old_stdout = sys.stdout
    sys.stdout = captured_output = StringIO()
    
    result = {'output': '', 'error': '', 'success': False}
    
    try:
        # Execute with timeout protection (basic)
        exec(code, safe_globals, {})
        result['output'] = captured_output.getvalue()
        result['success'] = True
    except Exception as e:
        result['error'] = f"{type(e).__name__}: {str(e)}"
        result['output'] = captured_output.getvalue()
    finally:
        sys.stdout = old_stdout
    
    return result

def escape_html_content(text: str) -> str:
    """Escape HTML special characters to prevent XSS and display issues."""
    return html.escape(text, quote=False)

def format_response_html(content: str) -> str:
    """Format AI response with better styling for code blocks."""
    import re
    
    # First, extract code blocks and store them temporarily to avoid escaping code
    code_blocks = []
    def store_code_block(match):
        code = match.group(1)
        idx = len(code_blocks)
        code_blocks.append(code)
        return f"__CODE_BLOCK_{idx}__"
    
    # Store code blocks before escaping
    content = re.sub(r'```(?:python)?\n?(.*?)```', store_code_block, content, flags=re.DOTALL)
    
    # Store inline code
    inline_codes = []
    def store_inline_code(match):
        code = match.group(1)
        idx = len(inline_codes)
        inline_codes.append(code)
        return f"__INLINE_CODE_{idx}__"
    
    content = re.sub(r'`([^`]+)`', store_inline_code, content)
    
    # Now escape HTML in the regular text
    formatted = escape_html_content(content)
    
    # Restore code blocks with styling
    def replace_code_block(match):
        idx = int(match.group(1))
        code = escape_html_content(code_blocks[idx])
        return f'''<div style="position:relative;margin:12px 0">
            <div style="background:#0d1117;border:1px solid rgba(0,245,255,0.2);border-radius:8px;padding:12px 14px;font-family:'JetBrains Mono',monospace;font-size:12px;color:#e8f4f8;overflow-x:auto;white-space:pre-wrap;line-height:1.5">{code}</div>
        </div>'''
    
    formatted = re.sub(r'__CODE_BLOCK_(\d+)__', replace_code_block, formatted)
    
    # Restore inline code with styling
    def replace_inline_code(match):
        idx = int(match.group(1))
        code = escape_html_content(inline_codes[idx])
        return f'<code style="background:rgba(0,245,255,0.15);color:#00f5ff;padding:2px 6px;border-radius:4px;font-family:monospace;font-size:12px">{code}</code>'
    
    formatted = re.sub(r'__INLINE_CODE_(\d+)__', replace_inline_code, formatted)
    
    # Convert **bold** to styled spans
    formatted = re.sub(r'\*\*([^*]+)\*\*', r'<strong style="color:#00ff88;font-weight:600">\1</strong>', formatted)
    # Convert headers ## to styled divs
    formatted = re.sub(r'^## (.+)$', r'<div style="color:#00f5ff;font-size:16px;font-weight:700;margin:16px 0 10px;font-family:Orbitron,sans-serif">\1</div>', formatted, flags=re.MULTILINE)
    formatted = re.sub(r'^### (.+)$', r'<div style="color:#bf00ff;font-size:14px;font-weight:600;margin:12px 0 8px">\1</div>', formatted, flags=re.MULTILINE)
    # Convert bullet points
    formatted = re.sub(r'^- (.+)$', r'<div style="padding-left:16px;margin:4px 0;color:#e8f4f8">• \1</div>', formatted, flags=re.MULTILINE)
    # Convert newlines to breaks
    formatted = formatted.replace('\n\n', '<div style="height:12px"></div>')
    formatted = formatted.replace('\n', '<br>')
    return formatted

@st.dialog("AI Chat Assistant", width="large")
def show_chat_modal():
    """Clean, advanced AI Chat interface with streamlined layout"""
    
    # Initialize chat states
    if "chat_loading" not in st.session_state:
        st.session_state.chat_loading = False
    if "response_mode" not in st.session_state:
        st.session_state.response_mode = "detailed"
    if "code_output" not in st.session_state:
        st.session_state.code_output = None
    if "last_user_msg" not in st.session_state:
        st.session_state.last_user_msg = None
    if "prompt_category" not in st.session_state:
        st.session_state.prompt_category = "Python"
    
    # Clean CSS for modern layout
    st.markdown("""
    <style>
    [data-testid="stDialog"] > div { 
        background: linear-gradient(180deg, #0a1628 0%, #061018 100%) !important; 
        border: 1px solid rgba(0, 245, 255, 0.25) !important; 
        border-radius: 16px !important;
        box-shadow: 0 0 40px rgba(0, 245, 255, 0.15) !important;
        max-width: 90vw !important;
        width: 90vw !important;
    }
    [data-testid="stDialog"] .stMarkdown p { color: #e8f4f8 !important; }
    [data-testid="stDialog"] .stMarkdown li { color: #e8f4f8 !important; }
    @keyframes typing {
        0%, 80%, 100% { opacity: 0.3; }
        40% { opacity: 1; }
    }
    .typing-dot { 
        display: inline-block; width: 8px; height: 8px; border-radius: 50%; 
        background: #00f5ff; margin: 0 3px; animation: typing 1.4s infinite;
    }
    .typing-dot:nth-child(2) { animation-delay: 0.2s; }
    .typing-dot:nth-child(3) { animation-delay: 0.4s; }
    .chat-msg-user {
        background: linear-gradient(135deg, #00ff88, #00cc6a); color: #030508;
        padding: 12px 16px; border-radius: 16px 16px 4px 16px; margin: 8px 0 8px 80px;
        font-size: 13px; line-height: 1.5; box-shadow: 0 4px 15px rgba(0,255,136,0.2);
    }
    .chat-msg-ai {
        background: linear-gradient(135deg, rgba(0,245,255,0.08), rgba(10,20,40,0.95));
        border: 1px solid rgba(0,245,255,0.2); color: #e8f4f8;
        padding: 14px 18px; border-radius: 16px 16px 16px 4px; margin: 8px 80px 8px 0;
        font-size: 13px; line-height: 1.6; box-shadow: 0 4px 15px rgba(0,245,255,0.08);
    }
    .quick-btn {
        font-size: 11px !important; padding: 8px 12px !important; 
        border-radius: 20px !important; margin: 2px !important;
        background: rgba(0,245,255,0.08) !important;
        border: 1px solid rgba(0,245,255,0.2) !important;
        transition: all 0.2s ease !important;
    }
    .quick-btn:hover {
        background: rgba(0,245,255,0.15) !important;
        border-color: rgba(0,245,255,0.4) !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Process pending message
    if st.session_state.get("pending_chat_msg"):
        msg = st.session_state.pending_chat_msg
        st.session_state.pending_chat_msg = None
        st.session_state.last_user_msg = msg
        st.session_state.chat_history.append({"role": "user", "content": msg})
        st.session_state.chat_loading = True
        try:
            if st.session_state.stage:
                d = QUESTIONS[st.session_state.stage][st.session_state.q_index]
                cc = st.session_state.get(f"code_{st.session_state.stage}_{st.session_state.q_index}", "")
                resp = builtin_chat(msg, d['question'], d['function'], cc, False)
            else:
                resp = builtin_chat(msg, "", "", "", False)
            st.session_state.chat_history.append({"role": "assistant", "content": resp})
            try:
                store_qa_interaction(msg, resp)
            except Exception:
                pass
        except Exception as e:
            st.session_state.chat_history.append({"role": "assistant", "content": f"Error: {str(e)[:100]}"})
        st.session_state.chat_loading = False
        st.session_state.code_output = None
    
    # ========== HEADER BAR ==========
    stats = get_learning_stats()
    total_qas = stats.get("total_interactions", 0)
    
    # Header with topic tabs and actions
    header_cols = st.columns([3, 5, 2])
    
    with header_cols[0]:
        st.markdown("""
        <div style="display:flex;align-items:center;gap:10px">
            <div style="font-size:24px">🤖</div>
            <div>
                <div style="font-size:14px;font-weight:700;color:#fff">PyCode AI</div>
                <div style="font-size:10px;color:#8fa3b8">Python • Selenium • Linux • Network</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with header_cols[1]:
        # Topic selector as pill buttons
        topics = ["🐍 Python", "🌐 Selenium", "🤖 Robot", "🐧 Linux", "🌐 Network"]
        topic_cols = st.columns(len(topics))
        for i, topic in enumerate(topics):
            with topic_cols[i]:
                topic_name = topic.split()[-1]
                is_selected = st.session_state.prompt_category == topic_name
                if st.button(topic, key=f"topic_{topic_name}", use_container_width=True, 
                           type="primary" if is_selected else "secondary"):
                    st.session_state.prompt_category = topic_name
                    st.session_state.reopen_chat = True
                    st.rerun()
    
    with header_cols[2]:
        # Quick actions
        action_cols = st.columns(3)
        with action_cols[0]:
            mode_icon = "⚡" if st.session_state.response_mode == "concise" else "📝"
            if st.button(mode_icon, key="toggle_mode", help="Toggle Detailed/Concise"):
                st.session_state.response_mode = "concise" if st.session_state.response_mode == "detailed" else "detailed"
                st.session_state.reopen_chat = True
                st.rerun()
        with action_cols[1]:
            if st.button("🗑️", key="clear_chat_header", help="Clear Chat"):
                st.session_state.chat_history = []
                st.session_state.code_output = None
                st.session_state.reopen_chat = True
                st.rerun()
        with action_cols[2]:
            st.markdown(f"""<div style="font-size:10px;color:#00f5ff;text-align:center;padding:8px 0">
                {total_qas} Q&As
            </div>""", unsafe_allow_html=True)
    
    st.markdown("<hr style='margin:8px 0;border-color:rgba(0,245,255,0.15)'>", unsafe_allow_html=True)
    
    # ========== MAIN LAYOUT ==========
    main_cols = st.columns([1, 5])
    
    # ========== LEFT SIDEBAR - Quick Prompts ==========
    with main_cols[0]:
        # Show prompts based on selected category
        cat_key = st.session_state.prompt_category
        
        extended_prompts = {
            "Python": [("What is class?", "🏗️"), ("Explain loops", "🔄"), ("List vs Tuple", "📊"), ("Functions", "⚡")],
            "Selenium": [("What is Selenium?", "🌐"), ("Locators", "🎯"), ("Waits", "⏳"), ("Actions", "🖱️")],
            "Robot": [("Robot Framework", "🤖"), ("Keywords", "🔑"), ("Variables", "📦"), ("Libraries", "📚")],
            "Linux": [("What is Linux?", "🐧"), ("Bash scripting", "📜"), ("systemd", "⚡"), ("chmod", "🔐")],
            "Network": [("TCP/IP", "🌐"), ("DNS", "📡"), ("HTTP", "🔗"), ("Firewall", "🔥")]
        }
        
        st.markdown(f"<div style='font-size:9px;color:#4a6380;letter-spacing:1px;margin-bottom:8px'>QUICK ASK</div>", unsafe_allow_html=True)
        
        for prompt, icon in extended_prompts.get(cat_key, []):
            if st.button(f"{icon} {prompt}", key=f"qp_{cat_key}_{prompt[:8]}", use_container_width=True):
                st.session_state.pending_chat_msg = prompt
                st.session_state.reopen_chat = True
                st.rerun()
        
        # Divider
        st.markdown("<hr style='margin:12px 0;border-color:rgba(0,245,255,0.1)'>", unsafe_allow_html=True)
        
        # Action buttons
        if st.session_state.chat_history:
            last_ai = next((m["content"] for m in reversed(st.session_state.chat_history) if m["role"] == "assistant"), None)
            if last_ai:
                code_blocks = extract_code_blocks(last_ai)
                if code_blocks:
                    if st.button("▶️ Run Code", key="run_code_btn", use_container_width=True):
                        st.session_state.code_output = run_python_code_safe(code_blocks[0])
                        st.session_state.reopen_chat = True
                        st.rerun()
                
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("👍", key="fb_up", help="Good"):
                        record_feedback(st.session_state.last_user_msg or "", last_ai, True)
                        st.toast("Thanks! 🧠")
                with c2:
                    if st.button("👎", key="fb_down", help="Improve"):
                        record_feedback(st.session_state.last_user_msg or "", last_ai, False)
                        st.toast("Noted! 📝")
    
    # ========== MAIN CHAT AREA ==========
    with main_cols[1]:
        # Chat container
        chat_container = st.container(height=480)
        with chat_container:
            if not st.session_state.chat_history:
                st.markdown("""
                <div style="text-align:center;padding:100px 40px">
                    <div style="font-size:50px;margin-bottom:16px;opacity:0.8">🤖</div>
                    <div style="font-size:16px;font-weight:600;color:#fff;margin-bottom:8px">Ask me anything!</div>
                    <div style="color:#8fa3b8;font-size:12px">Python • Selenium • Robot • Linux • Network</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                # Display messages - clean and simple
                for m in st.session_state.chat_history[-20:]:
                    if m["role"] == "user":
                        user_content = escape_html_content(m["content"][:500])
                        st.markdown(f'''
                        <div class="chat-msg-user">
                            <div style="font-size:9px;opacity:0.6;margin-bottom:4px">YOU</div>
                            {user_content}{"..." if len(m["content"]) > 500 else ""}
                        </div>
                        ''', unsafe_allow_html=True)
                    else:
                        formatted = format_response_html(m["content"])
                        st.markdown(f'''
                        <div class="chat-msg-ai">
                            <div style="font-size:9px;color:#00f5ff;margin-bottom:5px">AI</div>
                            <div>{formatted}</div>
                        </div>
                        ''', unsafe_allow_html=True)
                
                # Typing indicator
                if st.session_state.get("chat_loading"):
                    st.markdown('''
                    <div class="chat-msg-ai" style="display:inline-block;padding:10px 16px">
                        <span class="typing-dot"></span><span class="typing-dot"></span><span class="typing-dot"></span>
                    </div>
                    ''', unsafe_allow_html=True)
        
        # Show code output if exists
        if st.session_state.code_output:
            result = st.session_state.code_output
            if result['success']:
                output_text = result['output'] if result['output'] else "(No output)"
                st.success(f"```\n{output_text}\n```")
            else:
                st.error(f"```\n{result['error']}\n```")
        
        # Follow-up suggestions
        if st.session_state.chat_history:
            last_resp = next((m["content"] for m in reversed(st.session_state.chat_history) if m["role"] == "assistant"), "")
            if last_resp:
                followups = get_followups(last_resp)
                fu_cols = st.columns(3)
                for i, fu in enumerate(followups):
                    with fu_cols[i]:
                        if st.button(fu, key=f"fu_{i}", use_container_width=True):
                            st.session_state.pending_chat_msg = fu
                            st.session_state.reopen_chat = True
                            st.rerun()
        
        # Input form
        with st.form(key="chat_form", clear_on_submit=True):
            cols = st.columns([6, 1])
            with cols[0]:
                user_msg = st.text_input("", placeholder="Type your question here...", 
                                         key="chat_input", label_visibility="collapsed")
            with cols[1]:
                send = st.form_submit_button("➤", type="primary", use_container_width=True)
            
            if send and user_msg:
                st.session_state.pending_chat_msg = user_msg
                st.session_state.reopen_chat = True
                st.rerun()


# ==================== HEADER ====================
header_cols = st.columns([1, 4, 1])

with header_cols[0]:
    st.markdown('''
    <div style="padding:8px 0">
        <div style="
            width:40px;height:40px;
            background:linear-gradient(135deg,rgba(0,245,255,0.2),rgba(191,0,255,0.1));
            border:1px solid rgba(0,245,255,0.4);
            border-radius:10px;
            display:flex;align-items:center;justify-content:center;
            font-family:'Orbitron',sans-serif;font-size:14px;font-weight:800;
            color:#00f5ff;text-shadow:0 0 20px #00f5ff;
            box-shadow:0 0 25px rgba(0,245,255,0.3);
        ">&lt;/&gt;</div>
    </div>
    ''', unsafe_allow_html=True)

with header_cols[1]:
    st.markdown("""
    <div style="text-align:center;padding:6px 0">
        <div style="
            font-family:'Orbitron',sans-serif;
            font-size:2rem;font-weight:900;letter-spacing:6px;
            background:linear-gradient(90deg,#00f5ff,#bf00ff,#00f5ff);
            background-size:200% auto;
            -webkit-background-clip:text;-webkit-text-fill-color:transparent;
            animation:shine 3s linear infinite;
            text-shadow:0 0 40px rgba(0,245,255,0.5);
        ">NUTANIX PYCODE</div>
        <div style="font-family:'Orbitron',sans-serif;font-size:0.6rem;color:#4a6380;letter-spacing:4px;margin-top:4px">CYBER · CODING · PLATFORM</div>
    </div>
    <style>@keyframes shine{0%{background-position:0% center}100%{background-position:200% center}}</style>
    """, unsafe_allow_html=True)
    
with header_cols[2]:
    if st.button("AI Chat", type="primary", use_container_width=True, key="open_chat"):
        st.session_state.reopen_chat = False
        show_chat_modal()

# Auto-reopen chat modal if flag is set
if st.session_state.get("reopen_chat", False):
    st.session_state.reopen_chat = False
    show_chat_modal()

# Mode Selector
mode_cols = st.columns([1, 2, 1])
with mode_cols[1]:
    modes = ["Practice", "Interview"]
    current_idx = 0 if st.session_state.app_mode == "Practice" else 1
    mode = st.radio("Mode", modes, index=current_idx, horizontal=True, label_visibility="collapsed")
    if mode != st.session_state.app_mode:
        st.session_state.app_mode = mode
        st.rerun()

# ==================== MAIN LAYOUT - 2 CARDS ====================
c1, c2 = st.columns([1, 1.3], gap="large")

# ==================== LEFT CARD - PROBLEMS ====================
with c1:
    if st.session_state.app_mode == "Interview":
        st.markdown('<div class="card-header"><span class="card-title">Interview</span><span class="card-badge">MOCK</span></div>', unsafe_allow_html=True)
        
        if not st.session_state.interview_active:
            # Interview Setup with Clear Instructions
            st.markdown("""
            <div style="background:linear-gradient(135deg,rgba(0,245,255,0.06),rgba(10,20,40,0.9));border:1px solid rgba(0,245,255,0.2);border-radius:12px;padding:16px;margin-bottom:18px;position:relative;overflow:hidden">
                <div style="position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,transparent,#00f5ff,transparent)"></div>
                <div style="font-family:'Orbitron',sans-serif;font-size:11px;font-weight:600;color:#00f5ff;margin-bottom:8px;letter-spacing:2px;text-shadow:0 0 10px rgba(0,245,255,0.5)">MOCK INTERVIEW MODE</div>
                <div style="font-size:12px;color:#8fa3b8;line-height:1.6">Practice technical interviews with AI. Stages: <span style="color:#00f5ff">INTRO</span> → <span style="color:#bf00ff">APPROACH</span> → <span style="color:#00ff88">CODING</span> → <span style="color:#ff6b00">OPTIMIZE</span> → <span style="color:#ff00aa">WRAP-UP</span></div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("""
            <div style="background:rgba(255,255,255,0.02);border:1px solid rgba(0,245,255,0.12);border-radius:14px;padding:14px;margin-bottom:16px;">
                <div style="font-size:0.7rem;font-weight:700;color:#00f5ff;letter-spacing:2px;margin-bottom:6px">HOW IT WORKS</div>
                <div style="font-size:12px;color:#a3b8a0;line-height:1.6">
                    • <strong>Intro:</strong> Rephrase the prompt, ask any clarifications, and confirm constraints.<br/>
                    • <strong>Approach:</strong> Describe your algorithm, mention space/time trade-offs, then plan.<br/>
                    • <strong>Coding:</strong> Translate your approach into working code while narrating key decisions.<br/>
                    • <strong>Optimization:</strong> Analyze complexity and suggest refinements.<br/>
                    • <strong>Wrap-up:</strong> Ask for feedback, highlight what you learned, thank the interviewer.
            </div>
        </div>
        """, unsafe_allow_html=True)
            st.markdown("""
            <div style="display:flex;gap:10px;margin-bottom:14px;">
                <div style="flex:1;background:rgba(0,255,136,0.08);border:1px solid rgba(0,255,136,0.3);border-radius:10px;padding:10px;text-align:center;">
                    <div style="font-size:11px;color:#00ff88;font-weight:600">AI Coach</div>
                    <div style="font-size:14px;color:#ffffff;margin-top:6px;">Guides the flow</div>
                    <div style="font-size:10px;color:#6b8068;margin-top:4px;">Hints, nudges, reminders</div>
                </div>
                <div style="flex:1;background:rgba(191,0,255,0.08);border:1px solid rgba(191,0,255,0.3);border-radius:10px;padding:10px;text-align:center;">
                    <div style="font-size:11px;color:#bf00ff;font-weight:600">Live Feedback</div>
                    <div style="font-size:14px;color:#ffffff;margin-top:6px;">Metrics + tips</div>
                    <div style="font-size:10px;color:#6b8068;margin-top:4px;">Scores, strengths, gaps</div>
                </div>
                <div style="flex:1;background:rgba(245,107,0,0.08);border:1px solid rgba(245,107,0,0.3);border-radius:10px;padding:10px;text-align:center;">
                    <div style="font-size:11px;color:#ff6b00;font-weight:600">Wrap-Up</div>
                    <div style="font-size:14px;color:#ffffff;margin-top:6px;">Reflect</div>
                    <div style="font-size:10px;color:#6b8068;margin-top:4px;">Ask questions, note improvements</div>
                </div>
                </div>
                """, unsafe_allow_html=True)
        
            st.markdown('<div class="section-title sec-cyan">DIFFICULTY</div>', unsafe_allow_html=True)
            diff_map = {"Junior (Entry Level)": "junior", "Mid-Level (2-4 years)": "mid", "Senior (5+ years)": "senior"}
            diff = st.selectbox("Difficulty level", list(diff_map.keys()), index=1, key="iv_diff", label_visibility="collapsed")
            
            st.markdown('<div class="section-title sec-cyan">INTERVIEW TYPE</div>', unsafe_allow_html=True)
            type_map = {"Technical (Coding Focus)": "technical", "Behavioral (Soft Skills)": "behavioral", "Mixed (Both)": "mixed"}
            iv_type = st.selectbox("Interview type", list(type_map.keys()), index=0, key="iv_type", label_visibility="collapsed")
            
            st.markdown('<div class="section-title sec-cyan">TIME LIMIT</div>', unsafe_allow_html=True)
            time_limit = st.slider("Time limit (min)", 15, 60, 30, 5, key="iv_time", label_visibility="collapsed")
            st.markdown(f'<div style="text-align:center;font-size:11px;color:#6b8068">{time_limit} minutes</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="section-title sec-cyan">SELECT PROBLEM</div>', unsafe_allow_html=True)
            diff_key = diff.split(" ")[0]
            problem_stage = "Intermediate" if "Mid" in diff else ("Advanced" if "Senior" in diff else "Basic")
            available_problems = [(i, q) for i, q in enumerate(QUESTIONS[problem_stage])]
            problem_names = [f"{q['question'][:40]}..." for _, q in available_problems]
            selected_problem = st.selectbox("Problem", problem_names, key="iv_problem", label_visibility="collapsed")
            
            st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
            
            if st.button("Start Interview", type="primary", use_container_width=True):
                engine = create_interview_engine(
                    difficulty=diff_map[diff],
                    interview_type=type_map[iv_type],
                    time_limit=time_limit
                )
                prob_idx = problem_names.index(selected_problem)
                problem_data = available_problems[prob_idx][1]
                intro_msg = engine.start_new_interview(
                    problem=problem_data["question"],
                    function_name=problem_data["function"]
                )
                # Add the intro message to conversation history
                engine.state.add_message("assistant", intro_msg)
                st.session_state.interview_engine = engine
                st.session_state.interview_active = True
                st.session_state.interview_code = f"def {problem_data['function']}():\n    # Write your solution here\n    pass"
                st.session_state.interview_feedback_shown = False
                st.session_state.interview_problem = problem_data
                st.rerun()
        
            # Interview History
            history = load_interview_history()
            if history:
                st.markdown('<div class="section-title sec-cyan">YOUR HISTORY</div>', unsafe_allow_html=True)
                for h in history[-3:][::-1]:
                    grade = h.get("grade", "?")
                    topic = h.get("topic", "Interview")[:20]
                    rec = h.get("recommendation", "")[:15]
                    st.markdown(f'<div class="q-card"><div class="q-header"><span class="q-icon">#</span><span class="q-title">{topic}</span><span style="color:#4ade80;font-weight:700">{grade}</span></div><div style="font-size:10px;color:#6b8068;margin-top:4px">{rec}</div></div>', unsafe_allow_html=True)
        else:
            # Active Interview - Left Panel (Status & Tips)
            engine = st.session_state.interview_engine
            if engine:
                progress = engine.get_stage_progress()
                current_stage = progress["current_stage"]
                stage_info = STAGE_INFO.get(current_stage, {})
                icon = stage_info.get("icon", "00")
                title = stage_info.get("title", current_stage.title())
                desc = stage_info.get("description", "")
                st.markdown(f'''
                <div style="background:linear-gradient(135deg,rgba(0,245,255,0.08),rgba(10,20,40,0.95));border:1px solid rgba(0,245,255,0.3);border-radius:14px;padding:18px;text-align:center;margin-bottom:14px;position:relative;box-shadow:0 0 30px rgba(0,245,255,0.15)">
                    <div style="position:absolute;top:0;left:50%;transform:translateX(-50%);width:60%;height:2px;background:linear-gradient(90deg,transparent,#00f5ff,transparent)"></div>
                    <div style="font-family:'Orbitron',sans-serif;font-size:2rem;font-weight:900;background:linear-gradient(180deg,#fff,#00f5ff);-webkit-background-clip:text;-webkit-text-fill-color:transparent;text-shadow:0 0 30px rgba(0,245,255,0.8);margin-bottom:8px">{icon}</div>
                    <div style="font-family:'Orbitron',sans-serif;font-size:0.85rem;font-weight:700;color:#00f5ff;text-transform:uppercase;letter-spacing:3px;text-shadow:0 0 15px rgba(0,245,255,0.5)">{title}</div>
                    <div style="font-size:10px;color:#8fa3b8;margin-top:8px">{desc}</div>
                </div>
                ''', unsafe_allow_html=True)
                stage_sequence = [
                    ("intro", "Intro"),
                    ("approach", "Approach"),
                    ("coding", "Coding"),
                    ("optimization", "Optimize"),
                    ("behavioral", "Behavioral"),
                    ("wrapup", "Wrap-up")
                ]
                stage_markers = []
                for key, label in stage_sequence:
                    active = key == current_stage
                    color = "#00f5ff" if active else "rgba(255,255,255,0.15)"
                    stage_markers.append(f'<div style="flex:1;border-radius:8px;border:1px solid {color};background:{color};padding:6px 4px;font-size:10px;font-weight:600;color:#030508;text-align:center;letter-spacing:1px;margin:0 4px">{label}</div>')
                st.markdown(f'<div style="display:flex;margin-bottom:12px;">{"".join(stage_markers)}</div>', unsafe_allow_html=True)
                
                # Timer
                remaining = progress["remaining_time"]
                mins, secs = divmod(remaining, 60)
                time_color = "#ff00aa" if remaining < 120 else "#00f5ff"
                time_glow = "rgba(255,0,170,0.4)" if remaining < 120 else "rgba(0,245,255,0.4)"
                st.markdown(f'''
                <div style="text-align:center;font-family:'Orbitron',sans-serif;font-size:2rem;font-weight:700;color:{time_color};padding:14px;background:rgba(10,15,30,0.8);border:1px solid {time_color};border-radius:12px;margin-bottom:14px;letter-spacing:4px;text-shadow:0 0 20px {time_glow};box-shadow:0 0 25px {time_glow}">
                    {mins:02d}:{secs:02d}
            </div>
                ''', unsafe_allow_html=True)
                
                # Progress Bar
                st.progress(progress["progress_percent"] / 100)
                st.markdown(f'<div style="text-align:center;font-size:10px;color:#6b8068;margin-top:4px">Stage {progress["stage_index"] + 1} of {progress["total_stages"]}</div>', unsafe_allow_html=True)
                
                # Live Scores with Progress Bars
                scores = engine.state.scores
                st.markdown('<div class="section-title sec-cyan">LIVE METRICS</div>', unsafe_allow_html=True)
                score_items = [
                    ("Problem Solving", scores.problem_solving, "#00ff88"),
                    ("Communication", scores.communication, "#00f5ff"),
                    ("Code Quality", scores.code_quality, "#f59e0b"),
                    ("Complexity", scores.complexity_analysis, "#fbbf24")
                ]
                for label, score, color in score_items:
                    st.markdown(f'''
                    <div style="margin-bottom:10px">
                        <div style="display:flex;justify-content:space-between;font-size:11px;margin-bottom:4px">
                            <span style="color:#a3b8a0">{label}</span>
                            <span style="color:{color};font-weight:600">{score:.0f}</span>
            </div>
                        <div style="background:rgba(255,255,255,0.06);border-radius:4px;height:5px;overflow:hidden">
                            <div style="width:{score}%;height:100%;background:{color};border-radius:4px"></div>
            </div>
        </div>
                    ''', unsafe_allow_html=True)
                
                # Stage-Specific Tips
                stage_tips = {
                    "intro": ["• Ask clarifying questions", "• Confirm input/output format", "• Say 'I'm ready' to proceed"],
                    "approach": ["• Explain your algorithm", "• Mention edge cases", "• Discuss data structures"],
                    "coding": ["• Write clean code", "• Add comments", "• Talk through your logic"],
                    "optimization": ["• Analyze time complexity", "• Discuss space usage", "• Suggest improvements"],
                    "behavioral": ["• Use STAR method", "• Give specific examples", "• Be concise"],
                    "wrapup": ["• Ask about the team", "• Show genuine interest", "• Thank the interviewer"]
                }
                tips = stage_tips.get(current_stage, [])
                if tips:
                    st.markdown('<div class="section-title sec-cyan">TIPS FOR THIS STAGE</div>', unsafe_allow_html=True)
                    for tip in tips:
                        st.markdown(f'<div style="font-size:11px;color:#6b8068;padding:4px 0">{tip}</div>', unsafe_allow_html=True)
                
                st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
                
                if st.button("End Interview Early", use_container_width=True, type="secondary"):
                    engine.force_end_interview()
                    st.session_state.interview_feedback_shown = True
                    st.rerun()
    else:
        st.markdown('<div class="card-header"><span class="card-title">Problems</span></div>', unsafe_allow_html=True)
        
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
        
        with st.container(height=380):
            for i, q in enumerate(QUESTIONS[selected_d]):
                status = get_status(selected_d, i)
                # Replace emoji status icons with text indicators
                status_text = "✓" if status == "✅" else ("→" if status == "🔄" else str(i+1).zfill(2))
                is_active = st.session_state.stage == selected_d and st.session_state.q_index == i
                active_cls = "q-card-active" if is_active else ""
                st.markdown(f'<div class="q-card {active_cls}"><div class="q-header"><span class="q-icon">{status_text}</span><span class="q-title">{q["question"][:30]}...</span></div><div class="q-tags">{", ".join(q.get("tags", [])[:2])}</div></div>', unsafe_allow_html=True)
                if st.button("Select", key=f"sel_{selected_d}_{i}", use_container_width=True):
                    go_to(selected_d, i)
                    st.rerun()
        
# ==================== RIGHT CARD - CODE EDITOR ====================
with c2:
    if st.session_state.app_mode == "Interview" and st.session_state.interview_active:
        engine = st.session_state.interview_engine
        
        if engine and st.session_state.interview_feedback_shown:
            # Interview Complete - Show Detailed Feedback
            scores = engine.state.scores
            total = scores.get_total()
            grade = scores.get_grade()
            rec = scores.get_hiring_recommendation()
            
            # Grade Display with Color
            grade_colors = {"A": "#4ade80", "B": "#22c55e", "C": "#fbbf24", "D": "#f59e0b", "F": "#f87171"}
            grade_color = grade_colors.get(grade, "#6b8068")
            
            st.markdown(f'''
            <div style="text-align:center;padding:24px;background:rgba(74,222,128,0.08);border:1px solid rgba(74,222,128,0.2);border-radius:20px;margin-bottom:18px">
                <div style="font-size:3rem;font-weight:800;color:{grade_color};letter-spacing:-2px">{grade}</div>
                <div style="font-size:1.4rem;font-weight:700;color:#f5f5f0">{total:.0f}/100</div>
                <div style="font-size:0.85rem;color:#4ade80;font-weight:600;margin-top:8px">{rec}</div>
            </div>
            ''', unsafe_allow_html=True)
            
            # Score Breakdown
            st.markdown('<div class="section-title sec-purple">SCORE BREAKDOWN</div>', unsafe_allow_html=True)
            score_data = [
                ("Problem Solving", scores.problem_solving, "#4ade80", "35%"),
                ("Communication", scores.communication, "#22c55e", "25%"),
                ("Code Quality", scores.code_quality, "#f59e0b", "25%"),
                ("Complexity Analysis", scores.complexity_analysis, "#fbbf24", "15%")
            ]
            for name, score, color, weight in score_data:
                st.markdown(f'''
                <div style="background:rgba(255,255,255,0.03);border-radius:12px;padding:12px 14px;margin-bottom:10px">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px">
                        <span style="font-size:12px;font-weight:600;color:#f5f5f0">{name}</span>
                        <span style="font-size:14px;font-weight:700;color:{color}">{score:.0f}</span>
                    </div>
                    <div style="background:rgba(255,255,255,0.06);border-radius:4px;height:6px;overflow:hidden">
                        <div style="width:{score}%;height:100%;background:{color};border-radius:4px"></div>
                    </div>
                    <div style="font-size:9px;color:#6b8068;margin-top:4px">Weight: {weight}</div>
                </div>
                ''', unsafe_allow_html=True)
            
            # Strengths & Improvements
            strengths = []
            improvements = []
            aspects = scores.evaluated_aspects
            
            if aspects.get("explained_approach"): strengths.append("Clear problem-solving approach")
            else: improvements.append("Explain your approach before coding")
            if aspects.get("mentioned_edge_cases"): strengths.append("Good edge case awareness")
            else: improvements.append("Consider edge cases more thoroughly")
            if aspects.get("discussed_complexity"): strengths.append("Strong complexity analysis")
            else: improvements.append("Practice analyzing time/space complexity")
            if aspects.get("asked_clarifying_questions"): strengths.append("Asked clarifying questions")
            else: improvements.append("Ask more clarifying questions upfront")
            if aspects.get("wrote_working_code"): strengths.append("Produced working code")
            else: improvements.append("Focus on getting to working code faster")
            
            if strengths:
                st.markdown('<div class="section-title sec-purple">STRENGTHS</div>', unsafe_allow_html=True)
                for s in strengths:
                    st.markdown(f'<div style="font-size:12px;color:#4ade80;padding:5px 0">+ {s}</div>', unsafe_allow_html=True)
            
            if improvements:
                st.markdown('<div class="section-title sec-purple">AREAS TO IMPROVE</div>', unsafe_allow_html=True)
                for i in improvements:
                    st.markdown(f'<div style="font-size:12px;color:#f59e0b;padding:5px 0">• {i}</div>', unsafe_allow_html=True)
            
            # Save Result
            result = {
                "topic": engine.state.problem_name,
                "scores": {"problem_solving": scores.problem_solving, "communication": scores.communication, "code_quality": scores.code_quality, "complexity_analysis": scores.complexity_analysis, "total": total},
                "grade": grade,
                "recommendation": rec,
                "difficulty": engine.state.config.difficulty.value,
                "interview_type": engine.state.config.interview_type.value,
                "duration_seconds": engine.state.get_elapsed_time()
            }
            save_interview_history(result)
            
            st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
            if st.button("Start New Interview", type="primary", use_container_width=True):
                st.session_state.interview_active = False
                st.session_state.interview_engine = None
                st.session_state.interview_feedback_shown = False
                st.rerun()
        
        elif engine:
            # Active Interview - Right Panel (Conversation & Code)
            problem = st.session_state.get("interview_problem", {})
            progress = engine.get_stage_progress()
            current_stage = progress["current_stage"]
            stage_info = STAGE_INFO.get(current_stage, {"title": current_stage.title(), "goal": ""})
            
            # Stage Header
            st.markdown(f'''
            <div style="text-align:center;font-weight:600;color:#f59e0b;padding:14px;margin-bottom:12px;background:rgba(245,158,11,0.08);border:1px solid rgba(245,158,11,0.15);border-radius:14px;font-size:1rem;letter-spacing:0.5px">
                {stage_info.get("title", current_stage.title())}
            </div>
            ''', unsafe_allow_html=True)
            # Stage timeline
            markers = []
            for key in STAGE_ORDER:
                info = STAGE_INFO[key]
                active = key == current_stage
                color = "#00f5ff" if active else "rgba(255,255,255,0.15)"
                text_color = "#030508" if active else "#a3b8a0"
                markers.append(f'<div style="flex:1;padding:6px 4px;margin:0 4px;border-radius:8px;border:1px solid {color};background:{color};font-size:11px;font-weight:600;color:{text_color};text-align:center;letter-spacing:1px">{info["title"]}</div>')
            st.markdown(f'<div style="display:flex;margin-bottom:12px;">{"".join(markers)}</div>', unsafe_allow_html=True)
            goal = stage_info.get("goal", "")
            if goal:
                st.markdown(f'<div style="font-size:12px;color:#6b8068;margin-bottom:10px;line-height:1.6">{goal}</div>', unsafe_allow_html=True)
            
            # Problem Statement (Always Visible)
            if problem:
                st.markdown(f'''
                <div style="background:rgba(245,158,11,0.06);border:1px solid rgba(245,158,11,0.12);border-radius:12px;padding:14px;margin-bottom:12px">
                    <div style="font-size:10px;font-weight:600;color:#f59e0b;text-transform:uppercase;letter-spacing:1.2px;margin-bottom:8px">Problem</div>
                    <div style="font-size:13px;font-weight:500;color:#f5f5f0;line-height:1.5">{problem.get("question", "")}</div>
        </div>
                ''', unsafe_allow_html=True)
            
            # Conversation Area (Larger)
            st.markdown('<div style="font-size:10px;font-weight:600;color:#f59e0b;text-transform:uppercase;letter-spacing:1.2px;margin:10px 0 6px">Conversation</div>', unsafe_allow_html=True)
            with st.container(height=180):
                if engine.state.conversation_history:
                    for msg in engine.state.conversation_history:
                        if msg["role"] == "user":
                            st.markdown(f'''
                            <div style="background:linear-gradient(135deg,#22c55e,#16a34a);color:#0f1a14;padding:10px 14px;border-radius:16px 16px 4px 16px;margin:8px 0 8px 40px;font-size:12px;line-height:1.5">
                                <div style="font-size:9px;opacity:0.7;margin-bottom:4px">You</div>
                                {msg["content"]}
                            </div>
                            ''', unsafe_allow_html=True)
                        else:
                            st.markdown(f'''
                            <div style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);color:#f5f5f0;padding:10px 14px;border-radius:16px 16px 16px 4px;margin:8px 40px 8px 0;font-size:12px;line-height:1.5">
                                <div style="font-size:9px;color:#f59e0b;margin-bottom:4px">Interviewer</div>
                                {msg["content"]}
                            </div>
                            ''', unsafe_allow_html=True)
                else:
                    st.markdown('<div style="text-align:center;color:#6b8068;font-size:12px;padding:30px">Interview starting...</div>', unsafe_allow_html=True)
            
            # Code Editor (Show in coding/optimization stages)
            if current_stage in ["coding", "optimization", "approach"]:
                st.markdown('''
                <div style="margin-top:10px">
                    <div style="background:rgba(15,26,20,0.8);padding:10px 14px;border-radius:10px 10px 0 0;display:flex;align-items:center;gap:8px;border:1px solid rgba(255,255,255,0.06);border-bottom:none">
                        <span style="width:8px;height:8px;border-radius:50%;background:#f87171"></span>
                        <span style="width:8px;height:8px;border-radius:50%;background:#fbbf24"></span>
                        <span style="width:8px;height:8px;border-radius:50%;background:#4ade80"></span>
                        <span style="font-size:11px;color:#6b8068;font-family:'JetBrains Mono';margin-left:10px">solution.py</span>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
                code = st.text_area("", value=st.session_state.interview_code, height=90, key="iv_code_editor", label_visibility="collapsed")
                st.session_state.interview_code = code
            
            # Quick Response Buttons Based on Stage
            stage_quick_responses = {
                "intro": ["I have a question", "I understand, let me think", "Can you clarify the input format?", "I'm ready to discuss my approach"],
                "approach": ["I'll use a hash map", "Let me consider edge cases", "The time complexity would be O(n)", "I'll iterate through the array"],
                "coding": ["Let me walk through the code", "I need to handle edge cases", "This part handles the main logic", "I'm testing with an example"],
                "optimization": ["The current time complexity is O(n)", "We could use memoization", "Space complexity is O(1)", "A better approach would be..."],
                "behavioral": ["In my previous role...", "I learned that...", "The outcome was...", "I would handle it by..."],
                "wrapup": ["What's the team structure?", "What technologies do you use?", "Thank you for the interview", "What are the next steps?"]
            }
            
            quick_resps = stage_quick_responses.get(current_stage, [])
            if quick_resps:
                st.markdown('<div style="font-size:9px;color:#6b8068;margin:10px 0 6px">Quick responses:</div>', unsafe_allow_html=True)
                qr_cols = st.columns(2)
                for i, qr in enumerate(quick_resps[:4]):
                    with qr_cols[i % 2]:
                        if st.button(qr[:25] + ("..." if len(qr) > 25 else ""), key=f"qr_{i}", use_container_width=True):
                            code = st.session_state.interview_code if current_stage in ["coding", "optimization", "approach"] else ""
                            engine.process_response(qr, code)
                            if engine.state.current_stage == InterviewStage.COMPLETED:
                                st.session_state.interview_feedback_shown = True
                            st.rerun()
        
            # Custom Input
            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
            placeholder_text = stage_info.get("goal", "Type your response or use quick buttons above...")
            iv_input = st.text_input("Your response", placeholder=placeholder_text, key="iv_input", label_visibility="collapsed")
            
            send_col, end_col = st.columns([4, 1])
            with send_col:
                if st.button("Send Response", type="primary", use_container_width=True, key="iv_send"):
                    if iv_input:
                        code = st.session_state.interview_code if current_stage in ["coding", "optimization", "approach"] else ""
                        engine.process_response(iv_input, code)
                        if engine.state.current_stage == InterviewStage.COMPLETED:
                            st.session_state.interview_feedback_shown = True
                        st.rerun()
            with end_col:
                if st.button("X", key="iv_end", help="End Interview"):
                    engine.force_end_interview()
                    st.session_state.interview_feedback_shown = True
                    st.rerun()
        
            # Auto-end on time up
            if progress["is_time_up"] and not st.session_state.interview_feedback_shown:
                st.warning("Time's up! Generating your feedback...")
                engine.force_end_interview()
                st.session_state.interview_feedback_shown = True
                st.rerun()
    
    elif st.session_state.stage is None:
        st.markdown('<div class="welcome"><div class="welcome-icon">&lt;/&gt;</div><div class="welcome-title">Welcome to<br/>Code Editor</div><div class="welcome-sub">Select a problem from the left panel to start coding</div></div>', unsafe_allow_html=True)
        
        st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
        
        b1, b2, b3 = st.columns(3)
        with b1:
            if st.button("Easy", use_container_width=True, type="primary"):
                st.session_state.selected_difficulty = "Basic"
                go_to("Basic", next_q("Basic"))
                st.rerun()
        with b2:
            if st.button("Medium", use_container_width=True):
                st.session_state.selected_difficulty = "Intermediate"
                go_to("Intermediate", next_q("Intermediate"))
                st.rerun()
        with b3:
            if st.button("Hard", use_container_width=True):
                st.session_state.selected_difficulty = "Advanced"
                go_to("Advanced", next_q("Advanced"))
                st.rerun()
    
    else:
        # Code Editor - when a problem IS selected
        stage = st.session_state.stage
        qi = st.session_state.q_index
        data = QUESTIONS[stage][qi]
        t, c, s = get_stats_d(stage)
        
        n1, n2, n3 = st.columns([1, 2, 1])
        with n1:
            if st.button("←", key="back"):
                st.session_state.stage = None
                st.rerun()
        with n2:
            st.markdown(f'<div style="text-align:center;font-weight:600;color:#f59e0b;padding:8px;font-size:0.95rem">{stage} • Q{qi+1}/{t}</div>', unsafe_allow_html=True)
        with n3:
            if qi < t - 1:
                if st.button("→", key="next"):
                    go_to(stage, qi + 1)
                    st.rerun()
        
        st.markdown(f'<div class="problem-box"><div class="problem-title">{data["question"]}</div><div class="badges"><span class="badge {badge_cls(stage)}">{stage}</span>{render_tags(data.get("tags", []))}</div></div>', unsafe_allow_html=True)
        
        st.progress((c + s) / t if t > 0 else 0)
        
        if st.session_state.timer_start is None:
            st.session_state.timer_start = time.time()
        if not st.session_state.passed:
            st.markdown(f'<div class="timer">{format_time(time.time() - st.session_state.timer_start)}</div>', unsafe_allow_html=True)
        
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
        
        st.markdown('<div class="editor-box"><div class="editor-header"><span class="dot d-r"></span><span class="dot d-y"></span><span class="dot d-g"></span><span class="editor-file">Write your code below</span></div></div>', unsafe_allow_html=True)
        
        code = st.text_area("", value=template, height=120, key=f"code_{stage}_{qi}", label_visibility="collapsed")
        
        btn1, btn2, btn3 = st.columns(3)
        with btn1:
            run_btn = st.button("Run", type="primary", use_container_width=True)
        with btn2:
            hint_btn = st.button("Hint", use_container_width=True)
        with btn3:
            skip_btn = st.button("Skip", use_container_width=True)
        
        if hint_btn:
            with st.spinner("Thinking..."):
                try:
                    st.session_state.ai_hint = builtin_smart_hint(code, data['question'], data['function'], data.get('hints', []), st.session_state.show_hint + 1)
                    st.session_state.show_hint += 1
                except Exception as e:
                    st.session_state.ai_hint = str(e)
        
        if st.session_state.ai_hint:
            st.markdown(f'<div class="msg-hint">{st.session_state.ai_hint}</div>', unsafe_allow_html=True)
        
        if run_btn:
            ok, msg = evaluate_user_code(code, data["function"], data["test_cases"])
            if ok:
                # SUCCESS: All tests passed
                el = time.time() - st.session_state.timer_start
                st.markdown(f'<div class="msg-ok">✅ All tests passed! Time: {format_time(el)}</div>', unsafe_allow_html=True)
                st.session_state.passed = True
                st.session_state.progress[stage]["completed"].add(qi)
                st.session_state.progress[stage]["skipped"].discard(qi)
                st.session_state.progress = save_question_time(st.session_state.progress, stage, qi, el)
                save_progress(st.session_state.progress)
                # Generate code review only on success
                with st.spinner("Analyzing your solution..."):
                    try:
                        st.session_state.ai_feedback = builtin_code_review(code, data['question'], data['function'], el)
                    except Exception:
                        pass
            else:
                # FAILURE: Tests failed - show error and bug hint
                st.markdown(f'<div class="msg-err">{msg}</div>', unsafe_allow_html=True)
                with st.spinner("Analyzing error..."):
                    try:
                        bug = builtin_bug_hint(code, msg, data['question'], data['function'])
                        st.markdown(f'<div class="msg-hint">{bug}</div>', unsafe_allow_html=True)
                    except Exception:
                        pass
        
        if st.session_state.ai_feedback:
            st.markdown(f'<div class="msg-hint">{st.session_state.ai_feedback}</div>', unsafe_allow_html=True)
        
        if skip_btn:
            if qi not in st.session_state.progress[stage]["completed"]:
                st.session_state.progress[stage]["skipped"].add(qi)
                save_progress(st.session_state.progress)
            go_to(stage, (qi + 1) % t)
            st.rerun()
        
        # Display TEST CASES with actual results if code was run
        st.markdown('<div class="section-title sec-purple">TEST CASES</div>', unsafe_allow_html=True)
        
        # Check if we have test results to show (after running code)
        test_results_key = f"test_results_{stage}_{qi}"
        if run_btn:
            # Run each test case and store results
            test_results = []
            try:
                # Compile and execute user code to get the function
                safe_env = {'__builtins__': {
                    'range': range, 'len': len, 'int': int, 'str': str, 'list': list, 
                    'dict': dict, 'set': set, 'tuple': tuple, 'bool': bool, 'float': float,
                    'sum': sum, 'min': min, 'max': max, 'abs': abs, 'sorted': sorted,
                    'enumerate': enumerate, 'zip': zip, 'map': map, 'filter': filter,
                    'True': True, 'False': False, 'None': None, 'print': lambda *args: None,
                    'reversed': reversed, 'any': any, 'all': all, 'pow': pow, 'round': round,
                    'divmod': divmod, 'isinstance': isinstance, 'type': type,
                }}
                exec(compile(code, '<user_code>', 'exec'), safe_env)
                func = safe_env.get(data["function"])
                
                if func:
                    for inp, exp in data["test_cases"][:3]:
                        try:
                            actual = func(*inp)
                            passed = actual == exp
                            test_results.append((inp, exp, actual, passed, None))
                        except Exception as e:
                            test_results.append((inp, exp, None, False, str(e)))
                else:
                    test_results = [(inp, exp, None, False, "Function not found") for inp, exp in data["test_cases"][:3]]
            except Exception as e:
                test_results = [(inp, exp, None, False, f"Code error: {str(e)[:50]}") for inp, exp in data["test_cases"][:3]]
            
            st.session_state[test_results_key] = test_results
        
        # Display test cases with results if available
        if test_results_key in st.session_state and st.session_state[test_results_key]:
            for inp, exp, actual, passed, error in st.session_state[test_results_key]:
                if error:
                    st.markdown(f'''
                    <div class="test-case" style="border-left:3px solid #ff6b6b">
                        <span class="test-lbl">❌ Input:</span> {inp} → 
                        <span class="test-lbl">Expected:</span> {exp} | 
                        <span style="color:#ff6b6b">Error: {error}</span>
                    </div>''', unsafe_allow_html=True)
                elif passed:
                    st.markdown(f'''
                    <div class="test-case" style="border-left:3px solid #00ff88">
                        <span class="test-lbl">✅ Input:</span> {inp} → 
                        <span class="test-lbl">Expected:</span> {exp} | 
                        <span style="color:#00ff88">Got: {actual}</span>
                    </div>''', unsafe_allow_html=True)
                else:
                    st.markdown(f'''
                    <div class="test-case" style="border-left:3px solid #ff6b6b">
                        <span class="test-lbl">❌ Input:</span> {inp} → 
                        <span class="test-lbl">Expected:</span> {exp} | 
                        <span style="color:#ff6b6b">Got: {actual}</span>
                    </div>''', unsafe_allow_html=True)
        else:
            # Show expected outputs only (before running)
            for inp, exp in data["test_cases"][:3]:
                st.markdown(f'<div class="test-case"><span class="test-lbl">Input:</span> {inp} → <span class="test-lbl">Expected:</span> {exp}</div>', unsafe_allow_html=True)

# Footer
st.markdown('''
<div style="text-align:center;padding:24px 0;margin-top:20px">
    <div style="height:1px;background:linear-gradient(90deg,transparent,rgba(0,245,255,0.3),rgba(191,0,255,0.3),transparent);margin-bottom:16px"></div>
    <div style="font-family:'Orbitron',sans-serif;font-size:0.65rem;color:#4a6380;letter-spacing:3px">
        ENGINEERED WITH <span style="color:#00f5ff;text-shadow:0 0 10px #00f5ff">◆</span> PYCODE AI
    </div>
</div>
''', unsafe_allow_html=True)