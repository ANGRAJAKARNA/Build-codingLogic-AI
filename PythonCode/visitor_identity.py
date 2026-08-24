# visitor_identity.py
"""
Anonymous per-visitor identity — no login required.

Why this exists: Streamlit Community Cloud runs ONE shared server process
for every visitor to a public app URL. st.session_state alone doesn't
survive closing and reopening the browser (a fresh session starts empty),
and st.context.cookies is confirmed non-functional specifically on
Streamlit Community Cloud (the platform's proxy layer strips cookies
before they reach the app, even though the same code works locally).

This module instead stores a generated UUID in the browser's own
localStorage via the streamlit-local-storage component, which reads/writes
it through injected JS rather than raw request cookies or headers — so it
isn't affected by that proxy filtering. Every persistence and learning-memory
call in this app is keyed by this id so each visitor gets their own
progress/chat history/interview history instead of sharing one global pool.
"""

import uuid
import streamlit as st

try:
    from streamlit_local_storage import LocalStorage
    _LOCAL_STORAGE_AVAILABLE = True
except ImportError:
    _LOCAL_STORAGE_AVAILABLE = False

_STORAGE_KEY = "pycode_visitor_id"


def get_visitor_id() -> str:
    """
    Return a stable anonymous id for the current browser.

    Cached in st.session_state after the first read, so the localStorage
    component is only consulted once per session rather than on every
    rerun. Falls back to a session-only UUID (regenerated on every browser
    refresh — isolation still works within a session, it just won't persist
    across page reloads) if the local-storage component isn't installed.
    """
    if "visitor_id" in st.session_state:
        return st.session_state.visitor_id

    if not _LOCAL_STORAGE_AVAILABLE:
        new_id = str(uuid.uuid4())
        st.session_state.visitor_id = new_id
        return new_id

    ls = LocalStorage()  # blocks internally until the browser round-trip resolves
    stored = ls.getItem(_STORAGE_KEY)

    if stored:
        st.session_state.visitor_id = stored
        return stored

    new_id = str(uuid.uuid4())
    ls.setItem(_STORAGE_KEY, new_id)
    st.session_state.visitor_id = new_id
    return new_id
