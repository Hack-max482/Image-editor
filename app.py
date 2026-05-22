import streamlit as st
import requests
import base64
from PIL import Image
import io

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Image Editor · NVIDIA",
    page_icon="🎨",
    layout="centered",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@400;500&display=swap');

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

.hero { text-align: center; padding: 2.5rem 0 1.5rem; }
.hero h1 {
    font-size: 2.6rem; font-weight: 800; letter-spacing: -0.03em;
    background: linear-gradient(135deg, #76b900 0%, #a8e063 50%, #00d4aa 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; margin: 0; line-height: 1.1;
}
.hero p {
    color: #6b6880; font-size: 0.85rem; margin-top: 0.4rem;
    font-family: 'DM Mono', monospace; letter-spacing: 0.06em;
}
.result-label {
    font-size: 0.7rem; font-family: 'DM Mono', monospace;
    letter-spacing: 0.12em; text-transform: uppercase;
    color: #00d4aa; margin: 1.5rem 0 0.5rem; text-align: center;
}
.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #76b900, #4a7a00) !important;
    color: #fff !important; border: none !important;
    border-radius: 12px !important; font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important; font-size: 1rem !important;
    letter-spacing: 0.04em !important; padding: 0.75rem 2rem !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 24px rgba(118,185,0,0.35) !important;
}
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(118,185,0,0.25) !important;
    border-radius: 10px !important; color: #e8e6f0 !important;
    font-family: 'DM Mono', monospace !important; font-size: 0.9rem !important;
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

# ── API Key input ─────────────────────────────────────────────────────────────
with st.expander("🔑  Enter your NVIDIA API Key", expanded=True):
    api_key = st.text_input(
        "Paste your nvapi-... key here",
        type="password",
        placeholder="nvapi-xxxxxxxxxxxxxxxx",
    )

st.divider()

# ── Upload reference image ────────────────────────────────────────────────────
st.markdown("#### 📁 Upload Reference Image")
uploaded_file = st.file_uploader(
    "Supported formats: JPG, PNG, WEBP",
    type=["jpg", "jpeg", "png", "webp"],
)

if uploaded_file:
    st.image(uploaded_file, caption="Your reference image", use_container_width=True)

st.divider()

# ── Prompt input ──────────────────────────────────────────────────────────────
st.markdown("#### ✍️ Your Prompt")
prompt = st.text_area(
    "Describe what you want to generate or edit",
    placeholder='e.g. Add a sign saying "Grand Opening" to the storefront, high quality, photorealistic',
    height=120,
)

st.divider()

# ── Generate button ───────────────────────────────────────────────────────────
generate = st.button("🎨  Generate Image", use_container_width=True)

# ── Generation logic ──────────────────────────────────────────────────────────
if generate:
    if not api_key:
        st.error("⚠️ Please enter your NVIDIA API key first.")
    elif not uploaded_file:
        st.error("⚠️ Please upload a reference image.")
    elif not prompt.strip():
        st.error("⚠️ Please enter a prompt.")
    else:
        with st.spinner("✨ Generating your image..."):
            try:
                # Encode image to base64
                img_bytes = uploaded_file.read()
                img_b64 = base64.b64encode(img_bytes).decode("utf-8")

                # Detect mime type
                suffix = uploaded_file.name.split(".")[-1].lower()
                mime = "image/jpeg" if suffix in ("jpg", "jpeg") else f"image/{suffix}"

                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                }

                payload = {
                    "model": "qwen/qwen-image-edit",
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:{mime};base64,{img_b64}"
                                    },
                                },
                                {
                                    "type": "text",
                                    "text": prompt,
                                },
                            ],
                        }
                    ],
                    "max_tokens": 1024,
                }

                response = requests.post(
                    "https://integrate.api.nvidia.com/v1/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=120,
                )

                if response.status_code == 200:
                    data = response.json()
                    content = data["choices"][0]["message"]["content"]

                    # Try to extract base64 image from response
                    if "data:image" in content:
                        # Image returned as base64 data URL
                        b64_start = content.find("base64,") + 7
                        b64_end = content.find('"', b64_start)
                        b64_data = content[b64_start:b64_end] if b64_end != -1 else content[b64_start:]
                        img_data = base64.b64decode(b64_data)
                        result_img = Image.open(io.BytesIO(img_data))
                        st.markdown('<p class="result-label">✅ Generated Result</p>', unsafe_allow_html=True)
                        st.image(result_img, use_container_width=True)

                        # Download button
                        buf = io.BytesIO()
                        result_img.save(buf, format="PNG")
                        st.download_button(
                            label="⬇️  Download Image",
                            data=buf.getvalue(),
                            file_name="generated_image.png",
                            mime="image/png",
                        )
                    else:
                        # Model returned text response
                        st.markdown('<p class="result-label">📝 Model Response</p>', unsafe_allow_html=True)
                        st.info(content)
                        st.warning("The model returned a text response instead of an image. Try rephrasing your prompt to be more specific about image editing.")

                else:
                    st.error(f"API Error {response.status_code}: {response.text}")

            except requests.exceptions.Timeout:
                st.error("⏱️ Request timed out. Please try again.")
            except Exception as e:
                st.error(f"Something went wrong: {str(e)}")

# ── Footer ────────────────────────────────────────────────────────────────────
st.divider()
st.markdown(
    "<p style='text-align:center; color:#3a3850; font-size:0.75rem; font-family:DM Mono,monospace;'>"
    "qwen-image-edit · NVIDIA Build · Key expires 11/22/2026</p>",
    unsafe_allow_html=True,
)
