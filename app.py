import streamlit as st
import requests
import base64
import json
from PIL import Image
import io

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Image Editor · NVIDIA",
    page_icon="🎨",
    layout="centered",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
    background: #0a0a0f;
    color: #e8e6f0;
    font-family: 'Syne', sans-serif;
}

[data-testid="stAppViewContainer"] {
    background: radial-gradient(ellipse at 20% 0%, #1a0a2e 0%, #0a0a0f 60%),
                radial-gradient(ellipse at 80% 100%, #0d1a0a 0%, transparent 50%);
}

[data-testid="stHeader"] { background: transparent; }

/* Title block */
.hero {
    text-align: center;
    padding: 2.5rem 0 1.5rem;
}
.hero h1 {
    font-size: 2.6rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    background: linear-gradient(135deg, #76b900 0%, #a8e063 50%, #00d4aa 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0;
    line-height: 1.1;
}
.hero p {
    color: #6b6880;
    font-size: 0.95rem;
    margin-top: 0.5rem;
    font-family: 'DM Mono', monospace;
    letter-spacing: 0.04em;
}

/* Cards */
.card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(118, 185, 0, 0.15);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1.2rem;
}
.card-label {
    font-size: 0.7rem;
    font-family: 'DM Mono', monospace;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #76b900;
    margin-bottom: 0.6rem;
}

/* Streamlit widget overrides */
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(118,185,0,0.25) !important;
    border-radius: 10px !important;
    color: #e8e6f0 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.9rem !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {
    border-color: #76b900 !important;
    box-shadow: 0 0 0 2px rgba(118,185,0,0.15) !important;
}

/* File uploader */
[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.02) !important;
    border: 1px dashed rgba(118,185,0,0.3) !important;
    border-radius: 12px !important;
}

/* Button */
.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #76b900, #4a7a00) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 12px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    letter-spacing: 0.04em !important;
    padding: 0.75rem 2rem !important;
    transition: all 0.2s ease !important;
    cursor: pointer !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 24px rgba(118,185,0,0.35) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* Result image */
.result-label {
    font-size: 0.7rem;
    font-family: 'DM Mono', monospace;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #00d4aa;
    margin: 1.5rem 0 0.5rem;
    text-align: center;
}

/* Error / info */
.stAlert { border-radius: 10px !important; }

/* Divider */
hr { border-color: rgba(118,185,0,0.1) !important; }

/* Sidebar / password input */
[data-testid="stTextInput"] label,
[data-testid="stTextArea"] label,
[data-testid="stFileUploader"] label {
    color: #9996b0 !important;
    font-size: 0.8rem !important;
    font-family: 'DM Mono', monospace !important;
}
</style>
""", unsafe_allow_html=True)


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>AI Image Editor</h1>
    <p>powered by qwen-image-edit · NVIDIA Build</p>
</div>
""", unsafe_allow_html=True)


# ── API Key ───────────────────────────────────────────────────────────────────
with st.expander("🔑  API Key Settings", expanded=not st.session_state.get("api_key")):
    api_key = st.text_input(
        "NVIDIA API Key (nvapi-...)",
        type="password",
        placeholder="nvapi-xxxxxxxxxxxxxxxx",
        key="api_key_input",
    )
    if api
