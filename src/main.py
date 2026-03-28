import html
import time

import streamlit as st

from model import model_response


# ── helpers ──────────────────────────────────────────────────────────────────


def stream_words(text: str, delay: float = 0.04):
    words = text.split()
    built = []
    for word in words:
        built.append(word)
        yield " ".join(built)
        time.sleep(delay)


def format_message_html(text: str) -> str:
    html_parts = []
    list_buffer = []

    def flush_list():
        nonlocal list_buffer
        if list_buffer:
            items = "".join(f"<li>{item}</li>" for item in list_buffer)
            html_parts.append(f"<ul>{items}</ul>")
            list_buffer = []

    for line in text.splitlines():
        cleaned = line.strip()
        if not cleaned:
            flush_list()
            continue

        safe = html.escape(cleaned)

        if safe.startswith("### "):
            flush_list()
            html_parts.append(f"<h3>{safe[4:]}</h3>")
        elif safe.startswith("- "):
            list_buffer.append(safe[2:])
        else:
            flush_list()
            html_parts.append(f"<p>{safe}</p>")

    flush_list()
    return "".join(html_parts) or "<p></p>"


def render_chat_bubble(role: str, text: str, placeholder=None) -> None:
    if role == "assistant":
        avatar_html = '<div class="chat-avatar" style="background: linear-gradient(135deg, #06b6d4, #8b5cf6);">&#10022;</div>'
        bubble_style = "background: rgba(255,255,255,0.04); border-color: rgba(255,255,255,0.08); color: #e2e8f0;"
        row_style = "justify-content: flex-start;"
        content = format_message_html(text)
        html_out = (
            f'<div class="chat-row" style="{row_style}">'
            f'{avatar_html}'
            f'<div class="chat-bubble" style="{bubble_style}">{content}</div>'
            f'</div>'
        )
    else:
        avatar_html = '<div class="chat-avatar" style="background: linear-gradient(135deg, #6366f1, #a855f7);">U</div>'
        bubble_style = "background: linear-gradient(135deg,rgba(99,102,241,0.18),rgba(139,92,246,0.12)); border-color: rgba(139,92,246,0.25); color: #e2e8f0;"
        row_style = "justify-content: flex-end;"
        content = format_message_html(text)
        html_out = (
            f'<div class="chat-row" style="{row_style}">'
            f'<div class="chat-bubble" style="{bubble_style}">{content}</div>'
            f'{avatar_html}'
            f'</div>'
        )

    target = placeholder if placeholder is not None else st
    target.markdown(html_out, unsafe_allow_html=True)


# ── page config ──────────────────────────────────────────────────────────────

st.set_page_config(page_title="Career Guide", page_icon=":compass:", layout="wide")

# ── global CSS ───────────────────────────────────────────────────────────────

st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

        :root {
            --bg-primary: #0a0e1a;
            --bg-secondary: #111827;
            --bg-card: rgba(255, 255, 255, 0.04);
            --bg-card-hover: rgba(255, 255, 255, 0.07);
            --border: rgba(255, 255, 255, 0.08);
            --border-accent: rgba(6, 182, 212, 0.3);
            --text-primary: #f1f5f9;
            --text-secondary: #94a3b8;
            --text-muted: #64748b;
            --accent-cyan: #06b6d4;
            --accent-cyan-glow: rgba(6, 182, 212, 0.25);
            --accent-violet: #8b5cf6;
            --accent-violet-glow: rgba(139, 92, 246, 0.25);
            --glass: rgba(255, 255, 255, 0.03);
            --glass-border: rgba(255, 255, 255, 0.06);
            --radius: 16px;
            --radius-lg: 24px;
            --radius-full: 9999px;
            --shadow-lg: 0 25px 50px rgba(0, 0, 0, 0.4);
        }

        * { box-sizing: border-box; }

        .stApp {
            background: linear-gradient(145deg, #0a0e1a 0%, #111827 40%, #0f172a 70%, #0a0e1a 100%) !important;
            color: var(--text-primary);
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        }

        .stApp::before {
            content: "";
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background:
                radial-gradient(ellipse 80% 60% at 10% 20%, rgba(6, 182, 212, 0.08), transparent),
                radial-gradient(ellipse 60% 50% at 80% 80%, rgba(139, 92, 246, 0.06), transparent);
            pointer-events: none;
            z-index: 0;
        }

        [data-testid="stHeader"] {
            background: rgba(10, 14, 26, 0.8) !important;
            backdrop-filter: blur(20px) !important;
            border-bottom: 1px solid var(--border) !important;
        }

        [data-testid="stToolbar"] button,
        [data-testid="stToolbar"] button svg,
        [data-testid="stStatusWidget"],
        #MainMenu button,
        header button, header a {
            color: var(--text-secondary) !important;
            fill: var(--text-secondary) !important;
        }

        .block-container {
            max-width: 1100px;
            padding-top: 2rem;
            padding-bottom: 2rem;
        }

        h1, h2, h3 {
            font-family: 'Inter', sans-serif !important;
            color: var(--text-primary) !important;
            letter-spacing: -0.03em;
        }

        p, label, div, textarea, li {
            font-family: 'Inter', sans-serif !important;
        }

        /* preserve Streamlit's Material icon font */
        [data-testid="collapsedControl"] span,
        [data-testid="stSidebarCollapseButton"] span,
        [data-testid="stBaseButton-headerNoPadding"] span,
        button[kind="header"] span,
        .stIcon span,
        span[data-icon] {
            font-family: 'Material Symbols Rounded', 'Material Symbols Outlined', 'Material Icons' !important;
            -webkit-font-feature-settings: 'liga' !important;
            font-feature-settings: 'liga' !important;
        }


        /* ── sidebar ───────────────────────────────── */

        [data-testid="stSidebar"] {
            background: rgba(15, 23, 42, 0.95) !important;
            backdrop-filter: blur(20px) !important;
            border-right: 1px solid var(--border) !important;
        }

        [data-testid="stSidebar"] * {
            color: var(--text-secondary) !important;
        }

        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3,
        [data-testid="stSidebar"] .sidebar-title {
            color: var(--text-primary) !important;
        }


        /* ── hero ──────────────────────────────────── */

        .hero-slim {
            position: relative;
            padding: 2rem 2.5rem;
            margin-bottom: 1.5rem;
            border-radius: var(--radius-lg);
            background: var(--bg-card);
            border: 1px solid var(--border);
            backdrop-filter: blur(16px);
            overflow: hidden;
        }

        .hero-slim::before {
            content: "";
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 2px;
            background: linear-gradient(90deg, var(--accent-cyan), var(--accent-violet), var(--accent-cyan));
            background-size: 200% 100%;
            animation: shimmer 4s ease-in-out infinite;
        }

        @keyframes shimmer {
            0%, 100% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
        }

        .hero-slim .hero-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 2rem;
            flex-wrap: wrap;
        }

        .hero-slim .hero-left h1 {
            font-size: 1.75rem;
            font-weight: 800;
            margin: 0 0 0.4rem 0;
            background: linear-gradient(135deg, #f1f5f9 0%, #06b6d4 50%, #8b5cf6 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .hero-slim .hero-left p {
            color: var(--text-secondary);
            font-size: 0.95rem;
            line-height: 1.6;
            margin: 0;
        }

        .hero-slim .mode-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.5rem 1rem;
            border-radius: var(--radius-full);
            background: rgba(6, 182, 212, 0.1);
            border: 1px solid rgba(6, 182, 212, 0.25);
            color: var(--accent-cyan);
            font-size: 0.82rem;
            font-weight: 600;
            letter-spacing: 0.04em;
            text-transform: uppercase;
            white-space: nowrap;
        }

        .hero-slim .mode-badge::before {
            content: "";
            width: 8px; height: 8px;
            border-radius: 50%;
            background: var(--accent-cyan);
            box-shadow: 0 0 8px var(--accent-cyan-glow);
            animation: pulse-dot 2s ease-in-out infinite;
        }

        @keyframes pulse-dot {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.5; transform: scale(0.85); }
        }


        /* ── chat area ─────────────────────────────── */

        .chat-container {
            border-radius: var(--radius-lg);
            background: var(--bg-card);
            border: 1px solid var(--border);
            backdrop-filter: blur(16px);
            padding: 1.5rem;
            min-height: 420px;
        }

        .chat-row {
            display: flex;
            align-items: flex-start;
            gap: 0.75rem;
            margin-bottom: 1rem;
        }

        .chat-avatar {
            width: 2.4rem;
            height: 2.4rem;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1rem;
            flex: 0 0 auto;
            color: #fff;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        }

        .chat-bubble {
            flex: 1;
            max-width: 80%;
            border-radius: 18px;
            padding: 1rem 1.25rem;
            border: 1px solid rgba(255,255,255,0.08);
            line-height: 1.7;
            box-shadow: 0 4px 20px rgba(0,0,0,0.15);
        }

        .chat-bubble p, .chat-bubble span, .chat-bubble li,
        .chat-bubble strong, .chat-bubble em, .chat-bubble code, .chat-bubble div {
            color: inherit !important;
            -webkit-text-fill-color: inherit !important;
            margin: 0 0 0.6rem 0;
            font-size: 0.92rem;
        }

        .chat-bubble p:last-child { margin-bottom: 0; }

        .chat-bubble h3 {
            margin: 0.3rem 0 0.8rem 0;
            font-size: 1.05rem;
            font-weight: 700;
            color: var(--accent-cyan) !important;
            -webkit-text-fill-color: var(--accent-cyan) !important;
            border-bottom: 1px solid rgba(6, 182, 212, 0.2);
            padding-bottom: 0.4rem;
        }

        .chat-bubble ul {
            margin: 0.15rem 0 0.8rem 0;
            padding-left: 1.2rem;
        }

        .chat-bubble li {
            margin-bottom: 0.35rem;
        }


        /* ── input area ────────────────────────────── */

        .input-shell {
            margin-top: 1rem;
            padding: 0.6rem;
            border-radius: 20px;
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid var(--border);
            backdrop-filter: blur(12px);
        }

        .input-shell textarea,
        [data-baseweb="textarea"] textarea {
            background: rgba(255, 255, 255, 0.05) !important;
            color: var(--text-primary) !important;
            caret-color: var(--accent-cyan) !important;
            -webkit-text-fill-color: var(--text-primary) !important;
            opacity: 1 !important;
            border-radius: 14px !important;
            border: 1px solid var(--border) !important;
            min-height: 70px !important;
            font-family: 'Inter', sans-serif !important;
            font-size: 0.92rem !important;
        }

        .input-shell textarea:focus,
        [data-baseweb="textarea"] textarea:focus {
            border-color: var(--accent-cyan) !important;
            box-shadow: 0 0 0 2px var(--accent-cyan-glow) !important;
        }

        .input-shell textarea::placeholder {
            color: var(--text-muted) !important;
            -webkit-text-fill-color: var(--text-muted) !important;
        }

        [data-baseweb="textarea"] {
            background: transparent !important;
            border-radius: 14px !important;
        }


        /* ── buttons ───────────────────────────────── */

        [data-testid="stFormSubmitButton"] button,
        .stButton > button {
            background: linear-gradient(135deg, #06b6d4, #8b5cf6) !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: 12px !important;
            font-weight: 700 !important;
            font-family: 'Inter', sans-serif !important;
            padding: 0.6rem 1.2rem !important;
            box-shadow: 0 8px 24px rgba(6, 182, 212, 0.25) !important;
            transition: all 0.3s ease !important;
            min-height: 2.6rem !important;
        }

        [data-testid="stFormSubmitButton"] button:hover,
        .stButton > button:hover {
            box-shadow: 0 12px 32px rgba(6, 182, 212, 0.4) !important;
            transform: translateY(-1px) !important;
        }

        [data-testid="stFormSubmitButton"] button p,
        [data-testid="stFormSubmitButton"] button span,
        .stButton > button p,
        .stButton > button span {
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
        }


        /* ── clear button ──────────────────────────── */

        .clear-btn button {
            background: rgba(239, 68, 68, 0.1) !important;
            border: 1px solid rgba(239, 68, 68, 0.25) !important;
            color: #f87171 !important;
            box-shadow: none !important;
            font-size: 0.82rem !important;
            padding: 0.4rem 1rem !important;
            min-height: 2rem !important;
        }

        .clear-btn button:hover {
            background: rgba(239, 68, 68, 0.2) !important;
            box-shadow: 0 4px 12px rgba(239, 68, 68, 0.2) !important;
            transform: none !important;
        }

        .clear-btn button p, .clear-btn button span {
            color: #f87171 !important;
            -webkit-text-fill-color: #f87171 !important;
        }


        /* ── sidebar cards ─────────────────────────── */

        .sidebar-card {
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: var(--radius);
            padding: 1.2rem;
            margin-bottom: 1rem;
            backdrop-filter: blur(10px);
        }

        .sidebar-title {
            font-size: 1rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            color: var(--text-primary);
        }

        .sidebar-copy {
            font-size: 0.85rem;
            color: var(--text-secondary);
            line-height: 1.65;
            margin-bottom: 0.8rem;
        }

        .pill-grid {
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }

        .pill {
            display: inline-flex;
            align-items: center;
            padding: 0.55rem 0.85rem;
            border-radius: 12px;
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.08);
            color: var(--text-secondary);
            font-size: 0.83rem;
            transition: all 0.2s ease;
        }

        .pill:hover {
            background: rgba(6, 182, 212, 0.1);
            border-color: rgba(6, 182, 212, 0.25);
            color: var(--accent-cyan);
        }

        .pill::before {
            content: "";
            width: 6px; height: 6px;
            margin-right: 0.6rem;
            border-radius: 50%;
            background: linear-gradient(135deg, var(--accent-cyan), var(--accent-violet));
            flex: 0 0 auto;
        }


        /* ── streamlit overrides ───────────────────── */

        [data-testid="stForm"] {
            border: none !important;
            padding: 0 !important;
        }

        [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlockBorderWrapper"] {
            background: var(--bg-card) !important;
            border: 1px solid var(--border) !important;
            border-radius: var(--radius-lg) !important;
        }

        .stTextArea label, .stTextInput label {
            color: var(--text-secondary) !important;
        }

        /* hide default Streamlit footer */
        footer { visibility: hidden; }

        @media (max-width: 768px) {
            .hero-slim .hero-row { flex-direction: column; align-items: flex-start; }
            .chat-bubble { max-width: 95%; }
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ── hero ─────────────────────────────────────────────────────────────────────

st.markdown(
    """
    <div class="hero-slim">
        <div class="hero-row">
            <div class="hero-left">
                <h1>Career Discovery Studio</h1>
                <p>Describe your interests and the rule engine will guide you toward matching career paths.</p>
            </div>
            <div class="mode-badge">Rule-Based Chatbot</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ── sidebar ──────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown(
        """
        <div style="padding: 0.5rem 0 1rem;">
            <h2 style="font-size: 1.15rem; font-weight: 800; margin: 0 0 0.3rem 0;
                        background: linear-gradient(135deg, #f1f5f9, #06b6d4);
                        -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                Career Guide
            </h2>
            <p style="font-size: 0.8rem; margin: 0; color: #64748b !important;">
                Powered by forward-chaining rules
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="sidebar-card">
            <div class="sidebar-title">💡 Prompt Ideas</div>
            <div class="sidebar-copy">Try one of these to get started:</div>
            <div class="pill-grid">
                <span class="pill">I like math and physics</span>
                <span class="pill">I enjoy design and creativity</span>
                <span class="pill">I like biology and helping people</span>
                <span class="pill">I enjoy law, debate, and writing</span>
                <span class="pill">I like technology and problem solving</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="sidebar-card">
            <div class="sidebar-title">🧭 How It Works</div>
            <div class="sidebar-copy">
                Chat naturally — mention your interests, add strengths,
                and ask which career sounds best. The rule engine chains
                your facts forward to recommend careers.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ── session state ────────────────────────────────────────────────────────────

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Tell me what you enjoy studying or doing, and I will suggest careers that fit you.",
        }
    ]


# ── chat panel ───────────────────────────────────────────────────────────────

chat_panel = st.container(border=True)

with chat_panel:
    # toolbar
    toolbar_left, toolbar_right = st.columns([5, 1.2])
    with toolbar_left:
        st.markdown(
            '<p style="color: #64748b; font-size: 0.82rem; margin: 0;">Your conversation stays in memory. Each answer builds on the last.</p>',
            unsafe_allow_html=True,
        )
    with toolbar_right:
        st.markdown('<div class="clear-btn">', unsafe_allow_html=True)
        if st.button("🗑 Clear", key="clear_conversation"):
            st.session_state.messages = [
                {
                    "role": "assistant",
                    "content": "Tell me what you enjoy studying or doing, and I will suggest careers that fit you.",
                }
            ]
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # messages
    messages_box = st.container()
    with messages_box:
        for message in st.session_state.messages:
            render_chat_bubble(message["role"], message["content"])

    # input
    st.markdown('<div class="input-shell">', unsafe_allow_html=True)
    with st.form("chat_form", clear_on_submit=True):
        prompt = st.text_area(
            "Message",
            placeholder="Describe your interests…",
            label_visibility="collapsed",
        )
        submitted = st.form_submit_button("Send ➜")
    st.markdown("</div>", unsafe_allow_html=True)

    if submitted and prompt.strip():
        prompt = prompt.strip()
        st.session_state.messages.append({"role": "user", "content": prompt})
        chat_history = [
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ]

        with messages_box:
            render_chat_bubble("user", prompt)

            thinking_placeholder = st.empty()
            render_chat_bubble("assistant", "Thinking…", placeholder=thinking_placeholder)
            try:
                response_text = model_response(chat_history=chat_history)
                for partial in stream_words(response_text):
                    render_chat_bubble("assistant", partial, placeholder=thinking_placeholder)
                render_chat_bubble("assistant", response_text, placeholder=thinking_placeholder)
            except Exception as exc:
                response_text = f"Something went wrong: {exc}"
                render_chat_bubble("assistant", response_text, placeholder=thinking_placeholder)

        st.session_state.messages.append({"role": "assistant", "content": response_text})
        st.rerun()
