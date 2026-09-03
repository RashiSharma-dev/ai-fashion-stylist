# pages/10_AI_Stylist_Chat.py
# Purpose: Styled chat interface — pink/dark themed bubbles, typing
# indicator, and quick-reply buttons, talking to the context-aware
# AI stylist built on Day 59.

import streamlit as st
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from src.chatbot import get_chatbot_reply

st.title("💬 Chat with Your AI Stylist")

# ---------------------------------------------------------------
# STEP 1: Inject custom CSS to re-color the built-in chat bubbles
# to match our pink/dark theme (#D96C8C pink, #1C1F26 dark card,
# #FFB6C1 baby pink text), plus the typing-dots animation.
# ---------------------------------------------------------------
st.markdown("""
<style>
/* User messages: pink bubble, right-aligned */
div[data-testid="stChatMessage"]:has(img[data-testid="stChatMessageAvatarUser"]) {
    flex-direction: row-reverse;
    text-align: right;
}
div[data-testid="stChatMessage"]:has(img[data-testid="stChatMessageAvatarUser"]) div[data-testid="stChatMessageContent"] {
    background-color: #D96C8C;
    color: #0E1117;
    border-radius: 16px;
    padding: 10px 16px;
}

/* AI messages: dark card, baby-pink text, left-aligned */
div[data-testid="stChatMessage"]:has(img[data-testid="stChatMessageAvatarAssistant"]) div[data-testid="stChatMessageContent"] {
    background-color: #1C1F26;
    color: #FFB6C1;
    border-radius: 16px;
    padding: 10px 16px;
}

/* Typing indicator dots */
@keyframes bounce {
  0%, 80%, 100% { transform: scale(0); }
  40% { transform: scale(1); }
}
.typing-dots span {
  display: inline-block;
  width: 8px; height: 8px;
  margin: 0 2px;
  background-color: #FFB6C1;
  border-radius: 50%;
  animation: bounce 1.4s infinite ease-in-out both;
}
.typing-dots span:nth-child(1) { animation-delay: -0.32s; }
.typing-dots span:nth-child(2) { animation-delay: -0.16s; }
</style>
""", unsafe_allow_html=True)

TYPING_DOTS_HTML = """
<div class="typing-dots"><span></span><span></span><span></span></div>
"""

# ---------------------------------------------------------------
# STEP 2: Figure out the user's skin tone (same logic as Day 59)
# ---------------------------------------------------------------
detected_skin_tone = None
for possible_key in ["skin_tone", "detected_skin_tone", "user_skin_tone"]:
    if possible_key in st.session_state:
        value = st.session_state[possible_key]
        if isinstance(value, dict) and "skin_tone" in value:
            detected_skin_tone = value["skin_tone"]
        else:
            detected_skin_tone = value
        break

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
            "Select manually for testing:", ["warm", "cool", "neutral"]
        )

# ---------------------------------------------------------------
# STEP 3: Initialize conversation memory
# ---------------------------------------------------------------
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

incoming_message = None

# ---------------------------------------------------------------
# STEP 4: Quick-reply buttons — only shown before the first message,
# to reduce friction for a user who doesn't know what to ask
# ---------------------------------------------------------------
if len(st.session_state.chat_messages) == 0:
    st.caption("Not sure what to ask? Try one of these:")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("👔 What to wear for interview?", width="stretch"):
            incoming_message = "What should I wear for a job interview?"
    with col2:
        if st.button("☀️ Best summer colors?", width="stretch"):
            incoming_message = "What are the best colors for summer?"

# ---------------------------------------------------------------
# STEP 5: Display existing chat history as styled bubbles
# ---------------------------------------------------------------
for message in st.session_state.chat_messages:
    avatar = "🧑" if message["role"] == "user" else "🎨"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# ---------------------------------------------------------------
# STEP 6: Typed input at the bottom of the page
# ---------------------------------------------------------------
typed_input = st.chat_input("Ask your stylist anything about colors or outfits...")
if typed_input:
    incoming_message = typed_input

# ---------------------------------------------------------------
# STEP 7: Process whichever message arrived this run (button or typed)
# ---------------------------------------------------------------
if incoming_message:
    with st.chat_message("user", avatar="🧑"):
        st.markdown(incoming_message)
    st.session_state.chat_messages.append({"role": "user", "content": incoming_message})

    with st.chat_message("assistant", avatar="🎨"):
        typing_placeholder = st.empty()
        typing_placeholder.markdown(TYPING_DOTS_HTML, unsafe_allow_html=True)

        result = get_chatbot_reply(
            conversation_history=st.session_state.chat_messages,
            skin_tone=detected_skin_tone
        )

        typing_placeholder.empty()

        if result["error"]:
            st.error(f"Something went wrong: {result['error']}")
        else:
            st.markdown(result["reply"])
            st.session_state.chat_messages.append(
                {"role": "assistant", "content": result["reply"]}
            )