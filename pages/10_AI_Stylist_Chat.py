# pages/10_AI_Stylist_Chat.py
# Purpose: Chat interface where the user talks to the AI fashion stylist,
# which already knows their detected skin tone.

import streamlit as st
import sys
import os

# Allow importing from the src/ folder
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from src.chatbot import get_chatbot_reply

st.title("💬 Chat with Your AI Stylist")

# --- Step 1: Figure out the user's skin tone from earlier in the app ---
# Your skin tone analysis (from Week 1/2) likely stored a result somewhere
# in st.session_state. We check a few likely key names automatically.
detected_skin_tone = None
for possible_key in ["skin_tone", "detected_skin_tone", "user_skin_tone"]:
    if possible_key in st.session_state:
        value = st.session_state[possible_key]
        # Sometimes this is stored as a dict like {"skin_tone": "warm", ...}
        if isinstance(value, dict) and "skin_tone" in value:
            detected_skin_tone = value["skin_tone"]
        else:
            detected_skin_tone = value
        break

# Fallback: if we couldn't auto-detect it, let the user pick manually
# for testing purposes (this also helps you test all 3 cases quickly)
with st.sidebar:
    st.subheader("Skin Tone Context")
    if detected_skin_tone:
        st.success(f"Detected: **{detected_skin_tone}**")
        override = st.selectbox(
            "Override for testing (optional):",
            ["Use detected value", "warm", "cool", "neutral"]
        )
        if override != "Use detected value":
            detected_skin_tone = override
    else:
        st.warning("No skin tone detected yet.")
        detected_skin_tone = st.selectbox(
            "Select manually for testing:",
            ["warm", "cool", "neutral"]
        )

# --- Step 2: Initialize conversation history (only once per session) ---
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

# --- Step 3: Display all past messages as chat bubbles ---
for message in st.session_state.chat_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Step 4: Get new user input at the bottom of the page ---
user_input = st.chat_input("Ask your stylist anything about colors or outfits...")

if user_input:
    # Show the user's message immediately (right-aligned bubble, built-in)
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.chat_messages.append({"role": "user", "content": user_input})

    # Get the AI's reply, passing the FULL history so it has memory
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result = get_chatbot_reply(
                conversation_history=st.session_state.chat_messages,
                skin_tone=detected_skin_tone
            )

        if result["error"]:
            st.error(f"Something went wrong: {result['error']}")
        else:
            st.markdown(result["reply"])
            st.session_state.chat_messages.append(
                {"role": "assistant", "content": result["reply"]}
            )
