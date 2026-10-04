"""Zoro - a simple one-page AI chat app built with Streamlit and Claude."""

import base64
import os
from pathlib import Path

import anthropic
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

APP_NAME = "Zoro"
MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-5-5")
LOGO_PATH = Path(__file__).parent / "assets" / "logo.svg"

PERSONALITIES = {
    "Friendly": "You are a warm, friendly assistant. Keep answers clear and easy to read.",
    "Concise": "You are a concise assistant. Give short, direct answers with no filler.",
    "Poetic": "You are a gentle, poetic assistant. Answer helpfully, with a touch of lyrical language.",
}

st.set_page_config(page_title=APP_NAME, page_icon="🦋", layout="centered")

STYLE = """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500&family=Fraunces:opsz,wght@9..144,500&display=swap');

html, body, [class*="css"], .stApp {
    font-family: 'DM Sans', sans-serif;
    color: #2A1B3D;
}
.stApp {
    background: linear-gradient(160deg, #F6F1FF 0%, #EEF7FB 55%, #FDF0F6 100%);
}
#MainMenu, footer, header { visibility: hidden; }

.hero { text-align: center; padding: 1.5rem 0 1rem; }
.hero img { width: 92px; height: auto; }
.hero h1 {
    font-family: 'Fraunces', serif;
    font-weight: 500;
    font-size: 2.4rem;
    margin: 0.4rem 0 0.2rem;
    color: #2A1B3D;
}
.hero p { margin: 0; color: #6B5A80; }

[data-testid="stChatMessage"] {
    background: rgba(255, 255, 255, 0.72);
    border: 1px solid rgba(139, 92, 246, 0.16);
    border-radius: 18px;
    padding: 0.9rem 1.1rem;
}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
    background: rgba(233, 222, 252, 0.75);
}

[data-testid="stChatInput"] {
    border-radius: 24px;
    border: 1px solid rgba(139, 92, 246, 0.3);
}
[data-testid="stSidebar"] {
    background: rgba(255, 255, 255, 0.55);
}
.stButton > button {
    border-radius: 999px;
    border: 1px solid rgba(139, 92, 246, 0.35);
    background: transparent;
    color: #2A1B3D;
}
.stButton > button:hover {
    border-color: #8B5CF6;
    color: #6D3FD9;
}
</style>
"""


def logo_data_uri() -> str:
    """Return the logo as a data URI so it can be shown inside HTML."""
    encoded = base64.b64encode(LOGO_PATH.read_bytes()).decode()
    return f"data:image/svg+xml;base64,{encoded}"


def stream_reply(client: anthropic.Anthropic, messages: list, system: str):
    """Yield the reply piece by piece so it appears as it is written."""
    with client.messages.stream(
        model=MODEL,
        max_tokens=1024,
        system=system,
        messages=messages,
    ) as stream:
        for text in stream.text_stream:
            yield text


def main() -> None:
    st.markdown(STYLE, unsafe_allow_html=True)

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        st.error("No API key found. Copy .env.example to .env and add your ANTHROPIC_API_KEY.")
        st.stop()
    client = anthropic.Anthropic(api_key=api_key)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    with st.sidebar:
        st.markdown(f"### {APP_NAME}")
        personality = st.selectbox("Personality", list(PERSONALITIES))
        if st.button("New chat"):
            st.session_state.messages = []
            st.rerun()

    st.markdown(
        f"""
        <div class="hero">
            <img src="{logo_data_uri()}" alt="Butterfly logo">
            <h1>{APP_NAME}</h1>
            <p>Ask me anything.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    for message in st.session_state.messages:
        avatar = "🦋" if message["role"] == "assistant" else None
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

    prompt = st.chat_input("Type your message")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant", avatar="🦋"):
            try:
                reply = st.write_stream(
                    stream_reply(client, st.session_state.messages, PERSONALITIES[personality])
                )
            except anthropic.APIError as error:
                st.error(f"Couldn't get a reply: {error}")
                st.session_state.messages.pop()
                st.stop()

        st.session_state.messages.append({"role": "assistant", "content": reply})


main()
