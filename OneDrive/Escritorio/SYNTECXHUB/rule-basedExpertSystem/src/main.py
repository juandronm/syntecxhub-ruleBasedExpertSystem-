import html
import time

import streamlit as st

from model import model_response


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
        avatar = "bot"
        avatar_icon = "AI"
        avatar_style = "background: linear-gradient(135deg, #ff9800, #ff7a00);"
        bubble_style = (
            "background: linear-gradient(180deg, #fffdf8, #f2f8f6); "
            "color: #16323a; border: 1px solid rgba(20, 50, 58, 0.12);"
        )
    else:
        avatar = "user"
        avatar_icon = "U"
        avatar_style = "background: linear-gradient(135deg, #ff5a5f, #ff3131);"
        bubble_style = (
            "background: linear-gradient(135deg, #fff8f4, #ffffff); "
            "color: #1c2f35; border: 1px solid rgba(20, 50, 58, 0.12);"
        )

    target = placeholder if placeholder is not None else st
    target.markdown(
        f"""
        <div class="chat-row">
            <div class="chat-avatar {avatar}" style="{avatar_style}">{avatar_icon}</div>
            <div class="chat-bubble {avatar}" style="{bubble_style}">
                {format_message_html(text)}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


st.set_page_config(page_title="Career Guide", page_icon=":compass:", layout="wide")

st.markdown(
    """
    <style>
        :root {
            --bg-1: #fbf7ef;
            --bg-2: #d8ebe8;
            --bg-3: #f7d6bf;
            --surface: rgba(255, 250, 244, 0.78);
            --surface-strong: rgba(255, 255, 255, 0.72);
            --text: #14323a;
            --text-soft: #4f6b71;
            --text-strong: #10262d;
            --accent: #ef6c4d;
            --accent-2: #f4a261;
            --accent-3: #2a9d8f;
            --assistant-bubble: rgba(255, 252, 248, 0.98);
            --assistant-bubble-2: rgba(242, 248, 246, 0.99);
            --assistant-text: #16323a;
            --user-bubble: rgba(255, 248, 244, 0.99);
            --user-bubble-2: rgba(255, 255, 255, 0.99);
            --user-text: #1c2f35;
            --input-bg: #ffffff;
            --input-border: rgba(20, 50, 58, 0.16);
            --line: rgba(20, 50, 58, 0.10);
            --shadow: 0 24px 60px rgba(17, 45, 50, 0.12);
            --radius-lg: 30px;
            --radius-md: 22px;
            --space-4: 1.75rem;
            --space-5: 2.5rem;
        }

        .stApp {
            background:
                radial-gradient(circle at top left, rgba(255, 255, 255, 0.92), transparent 22%),
                radial-gradient(circle at 85% 15%, rgba(244, 162, 97, 0.22), transparent 18%),
                radial-gradient(circle at 20% 75%, rgba(42, 157, 143, 0.18), transparent 24%),
                linear-gradient(155deg, var(--bg-1), var(--bg-2) 52%, var(--bg-3));
            color: var(--text);
        }

        [data-testid="stHeader"] {
            background: rgba(251, 247, 239, 0.72);
            backdrop-filter: blur(14px);
            border-bottom: 1px solid rgba(20, 50, 58, 0.08);
        }

        [data-testid="stToolbar"] button,
        [data-testid="stToolbar"] button svg,
        [data-testid="stStatusWidget"],
        [data-testid="stSidebarNav"] *,
        #MainMenu button,
        header button,
        header a {
            color: var(--text) !important;
            fill: var(--text) !important;
        }

        .block-container {
            max-width: 1220px;
            padding-top: var(--space-5);
            padding-bottom: var(--space-5);
        }

        h1, h2, h3 {
            font-family: Georgia, "Times New Roman", serif;
            color: var(--text);
            letter-spacing: -0.02em;
            line-height: 1.05;
        }

        p, label, div, textarea {
            font-family: "Segoe UI", "Trebuchet MS", sans-serif;
        }

        .hero {
            position: relative;
            overflow: hidden;
            padding: clamp(1.8rem, 4vw, 3rem);
            border: 1px solid rgba(20, 50, 58, 0.08);
            border-radius: var(--radius-lg);
            background:
                linear-gradient(145deg, rgba(255, 248, 239, 0.92), rgba(255, 255, 255, 0.65)),
                linear-gradient(120deg, rgba(239, 108, 77, 0.10), rgba(42, 157, 143, 0.10));
            box-shadow: var(--shadow);
            margin-bottom: var(--space-4);
        }

        .hero-grid {
            display: grid;
            grid-template-columns: minmax(0, 1.4fr) minmax(240px, 0.85fr);
            gap: var(--space-4);
            align-items: end;
        }

        .hero-eyebrow {
            display: inline-block;
            padding: 0.45rem 0.8rem;
            border-radius: 999px;
            background: rgba(20, 50, 58, 0.06);
            color: var(--accent);
            text-transform: uppercase;
            font-size: 0.78rem;
            letter-spacing: 0.18em;
            font-weight: 800;
            margin-bottom: 1rem;
        }

        .hero-copy {
            max-width: 700px;
            font-size: 1.05rem;
            color: var(--text-soft);
            line-height: 1.75;
            margin-top: 1rem;
        }

        .hero-stat {
            padding: 1.15rem 1.2rem;
            border-radius: 24px;
            background: rgba(16, 54, 59, 0.92);
            color: #eefaf8;
            box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.08);
        }

        .hero-stat-label {
            text-transform: uppercase;
            letter-spacing: 0.16em;
            font-size: 0.78rem;
            opacity: 0.75;
            margin-bottom: 0.55rem;
        }

        .hero-stat-value {
            font-size: 2rem;
            font-weight: 700;
            line-height: 1;
        }

        .hero-stat-copy {
            margin-top: 0.7rem;
            font-size: 0.95rem;
            line-height: 1.6;
            color: rgba(238, 250, 248, 0.82);
        }

        .panel {
            background: var(--surface);
            border: 1px solid var(--line);
            border-radius: var(--radius-md);
            padding: var(--space-4);
            box-shadow: var(--shadow);
            backdrop-filter: blur(10px);
        }

        .panel-title {
            font-size: 1.2rem;
            font-weight: 800;
            margin-bottom: 0.4rem;
            color: var(--text);
        }

        .panel-copy {
            color: var(--text-soft);
            line-height: 1.7;
            margin-bottom: 1rem;
        }

        .pill-row {
            display: flex;
            flex-wrap: wrap;
            gap: 0.7rem;
            margin-top: 0.8rem;
        }

        .pill {
            display: inline-flex;
            align-items: center;
            padding: 0.58rem 0.9rem;
            border-radius: 999px;
            background: rgba(255, 255, 255, 0.58);
            border: 1px solid rgba(20, 50, 58, 0.10);
            color: var(--text);
            font-size: 0.93rem;
        }

        .pill::before {
            content: "";
            width: 0.55rem;
            height: 0.55rem;
            margin-right: 0.55rem;
            border-radius: 50%;
            background: linear-gradient(135deg, var(--accent), var(--accent-2));
            flex: 0 0 auto;
        }

        .chat-toolbar {
            display: flex;
            justify-content: flex-end;
            margin-bottom: 0.75rem;
        }

        .chat-messages {
            min-height: 360px;
        }

        .chat-row {
            display: flex;
            align-items: flex-start;
            gap: 0.9rem;
            margin-bottom: 1rem;
        }

        .chat-avatar {
            width: 3rem;
            height: 3rem;
            border-radius: 14px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.4rem;
            flex: 0 0 auto;
            box-shadow: 0 10px 24px rgba(17, 45, 50, 0.12);
        }

        .chat-avatar.bot {
            background: linear-gradient(135deg, #ff9800, #ff7a00);
        }

        .chat-avatar.user {
            background: linear-gradient(135deg, #ff5a5f, #ff3131);
        }

        .chat-bubble {
            flex: 1;
            border-radius: 24px;
            padding: 1rem 1.2rem;
            box-shadow: 0 16px 30px rgba(17, 45, 50, 0.08);
            line-height: 1.7;
            border: 1px solid rgba(20, 50, 58, 0.12);
        }

        .chat-bubble.bot {
            background: linear-gradient(180deg, var(--assistant-bubble), var(--assistant-bubble-2));
            color: var(--assistant-text) !important;
        }

        .chat-bubble.user {
            background: linear-gradient(135deg, var(--user-bubble), var(--user-bubble-2));
            color: var(--user-text) !important;
        }

        .chat-bubble p,
        .chat-bubble span,
        .chat-bubble li,
        .chat-bubble strong,
        .chat-bubble em,
        .chat-bubble code,
        .chat-bubble div {
            color: inherit !important;
            -webkit-text-fill-color: inherit !important;
            margin: 0 0 0.75rem 0;
        }

        .chat-bubble p:last-child {
            margin-bottom: 0;
        }

        .chat-bubble h3 {
            margin: 0.1rem 0 0.9rem 0;
            font-size: 1.15rem;
            line-height: 1.3;
            color: inherit !important;
            border-bottom: 1px solid rgba(20, 50, 58, 0.12);
            padding-bottom: 0.35rem;
        }

        .chat-bubble ul {
            margin: 0.15rem 0 1rem 0;
            padding-left: 1.25rem;
        }

        .chat-bubble li {
            margin-bottom: 0.45rem;
        }

        .chat-intro {
            padding: 0.2rem 0.2rem 1rem;
            color: var(--text-soft);
            line-height: 1.7;
        }

        .chat-input-shell {
            margin-top: 0.9rem;
            padding: 0.75rem;
            border-radius: 24px;
            background: rgba(255, 255, 255, 0.78);
            border: 1px solid rgba(20, 50, 58, 0.10);
            box-shadow: 0 18px 40px rgba(17, 45, 50, 0.08);
        }

        .chat-input-shell textarea {
            background: #ffffff !important;
            color: #111111 !important;
            caret-color: var(--accent) !important;
            -webkit-text-fill-color: #111111 !important;
            opacity: 1 !important;
            border-radius: 18px !important;
            border: 1px solid var(--input-border) !important;
            min-height: 90px !important;
        }

        .chat-input-shell textarea::placeholder {
            color: rgba(79, 107, 113, 0.88) !important;
            -webkit-text-fill-color: rgba(79, 107, 113, 0.88) !important;
        }

        .chat-input-shell [data-testid="stFormSubmitButton"] button,
        .chat-toolbar .stButton > button {
            background: linear-gradient(135deg, #ef6c4d, #ff8a5b) !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: 16px !important;
            min-height: 3rem !important;
            width: auto !important;
            padding: 0.8rem 1rem !important;
            font-weight: 800 !important;
            box-shadow: 0 14px 28px rgba(239, 108, 77, 0.28) !important;
        }

        .chat-input-shell [data-testid="stFormSubmitButton"] button p,
        .chat-input-shell [data-testid="stFormSubmitButton"] button span,
        .chat-toolbar .stButton > button p,
        .chat-toolbar .stButton > button span {
            color: #ffffff !important;
        }

        .chat-input-shell [data-testid="stFormSubmitButton"] button:hover,
        .chat-toolbar .stButton > button:hover {
            background: linear-gradient(135deg, #db5b3d, #ff7b4c) !important;
            color: #ffffff !important;
        }

        div[data-testid="stButton"]:has(button[kind]) button {
            background: linear-gradient(135deg, #ef6c4d, #ff8a5b) !important;
            color: #ffffff !important;
            border: none !important;
            box-shadow: 0 14px 28px rgba(239, 108, 77, 0.28) !important;
        }

        div[data-testid="stButton"]:has(button[kind]) button p,
        div[data-testid="stButton"]:has(button[kind]) button span {
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
        }

        [data-testid="stFormSubmitButton"] button {
            background: linear-gradient(135deg, #ef6c4d, #ff8a5b) !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: 16px !important;
            font-weight: 800 !important;
            box-shadow: 0 14px 28px rgba(239, 108, 77, 0.28) !important;
        }

        [data-testid="stFormSubmitButton"] button p,
        [data-testid="stFormSubmitButton"] button span {
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
        }

        .chat-input-shell [data-baseweb="textarea"] {
            background: #ffffff !important;
            border-radius: 18px !important;
        }

        .chat-input-shell [data-baseweb="textarea"] textarea {
            background: #ffffff !important;
            color: #111111 !important;
        }

        @media (max-width: 900px) {
            .hero-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <section class="hero">
        <div class="hero-eyebrow">Career Discovery Studio</div>
        <div class="hero-grid">
            <div>
                <h1>Talk through your interests like a real career conversation</h1>
                <p class="hero-copy">
                    Tell the assistant what you enjoy, what you are curious about, and what kind of work feels exciting.
                    The chat will respond naturally and guide you toward fitting career paths.
                </p>
            </div>
            <div class="hero-stat">
                <div class="hero-stat-label">Mode</div>
                <div class="hero-stat-value">Chatbot</div>
                <div class="hero-stat-copy">
                    Ask follow-up questions, refine your interests, and get answers that appear progressively like an LLM app.
                </div>
            </div>
        </div>
    </section>
    """,
    unsafe_allow_html=True,
)

main_col, side_col = st.columns([1.6, 0.9], gap="large")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Tell me what you enjoy studying or doing, and I will suggest careers that fit you.",
        }
    ]

with side_col:
    st.markdown(
        """
        <div class="panel">
            <div class="panel-title">Prompt ideas</div>
            <div class="panel-copy">
                Start with one of these and continue the conversation from there.
            </div>
            <div class="pill-row">
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
        <div class="panel" style="margin-top: 1rem;">
            <div class="panel-title">How to use it</div>
            <div class="panel-copy">
                You can keep chatting naturally. For example, first mention your interests, then add strengths, then ask which path sounds best for you.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with main_col:
    chat_panel = st.container(border=True)
    with chat_panel:
        st.markdown(
            """
            <div class="chat-intro">
                Chat with the assistant the same way you would in an LLM app. Your messages stay in the conversation and each new answer builds on the previous one.
            </div>
            """,
            unsafe_allow_html=True,
        )

        toolbar_left, toolbar_right = st.columns([4, 1])
        with toolbar_right:
            if st.button("Clear conversation", key="clear_conversation_inside"):
                st.session_state.messages = [
                    {
                        "role": "assistant",
                        "content": "Tell me what you enjoy studying or doing, and I will suggest careers that fit you.",
                    }
                ]
                st.rerun()

        messages_box = st.container()
        with messages_box:
            for message in st.session_state.messages:
                render_chat_bubble(message["role"], message["content"])

        st.markdown('<div class="chat-input-shell">', unsafe_allow_html=True)
        with st.form("chat_form", clear_on_submit=True):
            prompt = st.text_area(
                "Type your message here...",
                placeholder="Type your message here...",
                label_visibility="collapsed",
            )
            submitted = st.form_submit_button("Send")
        st.markdown("</div>", unsafe_allow_html=True)

        if submitted and prompt.strip():
            prompt = prompt.strip()
            st.session_state.messages.append({"role": "user", "content": prompt})
            chat_history = [
                {"role": message["role"], "content": message["content"]}
                for message in st.session_state.messages
            ]

            with messages_box:
                render_chat_bubble("user", prompt)

                thinking_placeholder = st.empty()
                render_chat_bubble("assistant", "Thinking...", placeholder=thinking_placeholder)
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
