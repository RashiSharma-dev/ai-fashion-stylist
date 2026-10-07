import streamlit as st
from PIL import Image
import sys
import os
import hashlib

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from color_recommender import analyze_and_recommend
from recommender import OutfitRecommender
from chatbot import get_chatbot_reply
from analytics import log_event
from theme import apply_theme
from ui_states import empty_state

# Must be the FIRST Streamlit command. Sidebar starts collapsed for the mirror feel.
st.set_page_config(
    page_title="Mirror Mode",
    page_icon="🪞",
    layout="wide",
    initial_sidebar_state="collapsed",
)

apply_theme()

# ------------------------------------------------------------------
# Mirror aesthetic: full-screen dark layout, glow, hidden chrome
# ------------------------------------------------------------------
st.markdown("""
<style>
/* Hide Streamlit's own chrome so only the mirror shows */
[data-testid="stSidebar"],
[data-testid="stSidebarCollapsedControl"],
[data-testid="stHeader"],
footer {
    display: none !important;
}

/* Dark radial gradient: slightly lighter in the middle, like a lit mirror */
.stApp {
    background: radial-gradient(ellipse at center, var(--color-secondary) 0%, var(--color-background) 70%);
}

/* Use the full width of the screen */
.block-container {
    max-width: 100% !important;
    padding-top: 1rem !important;
    padding-bottom: 6rem !important;
}

@keyframes mirrorGlow {
    0%, 100% {
        box-shadow: 0 0 18px color-mix(in srgb, var(--color-primary) 45%, transparent),
                    0 0 50px color-mix(in srgb, var(--color-primary) 20%, transparent);
    }
    50% {
        box-shadow: 0 0 28px color-mix(in srgb, var(--color-primary) 65%, transparent),
                    0 0 80px color-mix(in srgb, var(--color-primary) 30%, transparent);
    }
}

/* The camera becomes the mirror: rounded frame with a pulsing glow */
[data-testid="stCameraInput"] {
    border: 2px solid var(--color-primary);
    border-radius: 28px;
    padding: 12px;
    background-color: var(--color-background);
    animation: mirrorGlow 4s ease-in-out infinite;
}
[data-testid="stCameraInput"] video,
[data-testid="stCameraInput"] img {
    border-radius: 20px;
}

/* Outfit cards: dark glass with a soft glow */
.mirror-card {
    display: flex;
    align-items: center;
    gap: 14px;
    border: 1px solid var(--color-primary);
    border-radius: 16px;
    padding: 12px 16px;
    margin-bottom: 12px;
    background-color: var(--color-secondary);
    box-shadow: 0 0 14px color-mix(in srgb, var(--color-primary) 30%, transparent);
}
.mirror-swatches {
    display: flex;
    flex-direction: column;
    gap: 4px;
    width: 52px;
}
.mirror-swatch {
    height: 24px;
    border-radius: 6px;
    border: 1px solid var(--color-primary);
}
.mirror-info {
    flex: 1;
}
.mirror-score {
    background-color: var(--color-background);
    border-radius: 6px;
    height: 8px;
    margin-top: 8px;
}
.mirror-score-fill {
    background-color: var(--color-primary);
    height: 8px;
    border-radius: 6px;
}
.mirror-tone {
    font-family: var(--font-heading);
    font-size: 1.6rem;
    text-shadow: 0 0 12px color-mix(in srgb, var(--color-primary) 60%, transparent);
}
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------
# Session state for this page (kept separate from the main chat)
# ------------------------------------------------------------------
if "mirror_messages" not in st.session_state:
    st.session_state.mirror_messages = []
if "mirror_photo_hash" not in st.session_state:
    st.session_state.mirror_photo_hash = None
if "mirror_skin_tone" not in st.session_state:
    st.session_state.mirror_skin_tone = None
if "mirror_error" not in st.session_state:
    st.session_state.mirror_error = None

# ------------------------------------------------------------------
# Top bar
# ------------------------------------------------------------------
title_col, exit_col = st.columns([5, 1])
with title_col:
    st.title("🪞 Mirror Mode")
with exit_col:
    st.write("")
    st.page_link("pages/1_Home.py", label="Exit Mirror Mode", icon="🏠")

# ------------------------------------------------------------------
# Main area: left = mirror (camera), right = live recommendations
# ------------------------------------------------------------------
left, right = st.columns(2, gap="large")

with left:
    st.caption("Step in front of the mirror and take a photo. Your colors appear instantly.")
    camera_photo = st.camera_input("Mirror camera", label_visibility="collapsed")

    if camera_photo is not None:
        # Only re-analyze when the photo actually changes (every chat message reruns this page)
        photo_hash = hashlib.md5(camera_photo.getvalue()).hexdigest()

        if photo_hash != st.session_state.mirror_photo_hash:
            with st.spinner("Reading your colors..."):
                image = Image.open(camera_photo).convert("RGB")
                save_path = "data/temp_mirror_capture.jpg"
                image.save(save_path)
                result = analyze_and_recommend(save_path)

            st.session_state.mirror_photo_hash = photo_hash

            if result.get("error"):
                st.session_state.mirror_error = result["error"]
                st.session_state.mirror_skin_tone = None
            else:
                st.session_state.mirror_error = None
                st.session_state.mirror_skin_tone = result["skin_tone"]
                log_event("photo_analyzed")

with right:
    skin_tone = st.session_state.mirror_skin_tone

    if st.session_state.mirror_error:
        st.warning(st.session_state.mirror_error)
    elif skin_tone is None:
        empty_state(
            "🪞",
            "Waiting for you...",
            "Take a photo on the left, and your personalized outfits will appear right here."
        )
    else:
        st.markdown(
            f'<div class="mirror-tone">Your skin tone: {skin_tone.upper()}</div>',
            unsafe_allow_html=True,
        )

        pick_col1, pick_col2 = st.columns(2)
        with pick_col1:
            occasion = st.radio("Occasion", ["Casual", "Formal", "Party"], horizontal=True, key="mirror_occasion")
        with pick_col2:
            season = st.radio("Season", ["Summer", "Winter"], horizontal=True, key="mirror_season")

        recommender = OutfitRecommender()
        outfits = recommender.recommend(skin_tone, occasion, season, top_n=3)

        if not outfits:
            empty_state(
                "🔍",
                "No outfits match this combination.",
                "Try changing Occasion or Season above."
            )

        for outfit in outfits:
            outfit["scores"] = recommender.calculate_match_score(outfit)
            top_hex = recommender.get_color_hex(outfit["top_color"])
            bottom_hex = recommender.get_color_hex(outfit["bottom_color"])
            total = outfit["scores"]["total"]

            st.markdown(f"""
            <div class="mirror-card">
                <div class="mirror-swatches">
                    <div class="mirror-swatch" style="background-color:{top_hex};"></div>
                    <div class="mirror-swatch" style="background-color:{bottom_hex};"></div>
                </div>
                <div class="mirror-info">
                    <b>{outfit['top_color']} + {outfit['bottom_color']}</b><br>
                    <span style="font-size:13px;">Outfit #{outfit['outfit_id']} &middot; {total}% match</span>
                    <div class="mirror-score">
                        <div class="mirror-score-fill" style="width:{total}%;"></div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ------------------------------------------------------------------
# Bottom: chatbot. The chat box is pinned to the bottom of the screen.
# ------------------------------------------------------------------
st.divider()
st.subheader("💬 Ask Your Stylist")

typed_message = st.chat_input("Ask the mirror anything about your look...")

# Handle a new message BEFORE drawing history, so the history loop below
# is the ONLY place messages are displayed (no duplicates).
if typed_message:
    st.session_state.mirror_messages.append({"role": "user", "content": typed_message})
    log_event("chat_message")

    detected_tone = st.session_state.mirror_skin_tone

    if detected_tone is None:
        st.session_state.mirror_messages.append({
            "role": "assistant",
            "content": "Take a photo in the mirror first so I can see your colors! 📸",
        })
    else:
        context = st.session_state.get("stylist_context", {})
        with st.spinner("Your stylist is thinking..."):
            chat_result = get_chatbot_reply(
                conversation_history=st.session_state.mirror_messages,
                skin_tone=detected_tone,
                occasion=context.get("occasion"),
                body_shape=context.get("body_shape"),
                style_personality=context.get("style_personality") or st.session_state.get("style_personality"),
            )

        if chat_result["error"]:
            st.session_state.mirror_messages.append({
                "role": "assistant",
                "content": f"Sorry, something went wrong: {chat_result['error']}",
            })
        else:
            st.session_state.mirror_messages.append({
                "role": "assistant",
                "content": chat_result["reply"],
            })

# The ONE place chat messages are displayed
history_box = st.container(height=260)
with history_box:
    if not st.session_state.mirror_messages:
        st.caption("Try: 'What should I wear to a party tonight?'")
    for message in st.session_state.mirror_messages:
        avatar = "🧑" if message["role"] == "user" else "🎨"
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])
