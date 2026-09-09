# pages/10_AI_Stylist_Chat.py
# Purpose: Styled chat interface that auto-greets the user with a
# personalized opener right after an analysis, then supports normal
# back-and-forth chat with full context and memory.

import streamlit as st
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from src.chatbot import get_chatbot_reply, get_greeting_reply

st.title("💬 Chat with Your AI Stylist")

# ---------------------------------------------------------------
# CSS: pink/dark themed bubbles + typing dots (from Day 60)
# ---------------------------------------------------------------
st.markdown("""
<style>
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
div[data-testid="stChatMessage"]:has(img[data-testid="stChatMessageAvatarAssistant"]) div[data-testid="stChatMessageContent"] {
    background-color: #1C1F26;
    color: #FFB6C1;
    border-radius: 16px;
    padding: 10px 16px;
}
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

TYPING_DOTS_HTML = '<div class="typing-dots"><span></span><span></span><span></span></div>'

# ---------------------------------------------------------------
# STEP 1: Read the standardized context (set by set_analysis_context)
# with a fallback for older session_state keys, and a manual
# override for testing.
# ---------------------------------------------------------------
context = st.session_state.get("stylist_context", {})
detected_skin_tone = context.get("skin_tone")
detected_occasion = context.get("occasion")

if not detected_skin_tone:
    # backward-compatible fallback, same as Day 59
    for possible_key in ["skin_tone", "detected_skin_tone", "user_skin_tone"]:
        if possible_key in st.session_state:
            value = st.session_state[possible_key]
            detected_skin_tone = value.get("skin_tone") if isinstance(value, dict) else value
            break

with st.sidebar:
    st.subheader("Skin Tone Context")
    if detected_skin_tone:
        st.success(f"Detected: **{detected_skin_tone}**")
        if detected_occasion:
            st.caption(f"Occasion: {detected_occasion}")
        override = st.selectbox("Override for testing (optional):", ["Use detected value", "warm", "cool", "neutral"])
        if override != "Use detected value":
            detected_skin_tone = override
    else:
        st.warning("No skin tone detected yet.")
        detected_skin_tone = st.selectbox("Select manually for testing:", ["warm", "cool", "neutral"])

# ---------------------------------------------------------------
# STEP 2: Initialize conversation memory
# ---------------------------------------------------------------
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []
if "chat_greeted" not in st.session_state:
    st.session_state.chat_greeted = False

# ---------------------------------------------------------------
# STEP 3: AUTO-GREETING — the wow-factor moment. Runs once per
# fresh analysis (chat_greeted resets to False in set_analysis_context).
# ---------------------------------------------------------------
if not st.session_state.chat_greeted and detected_skin_tone and len(st.session_state.chat_messages) == 0:
    st.session_state.chat_greeted = True

    with st.spinner("Your stylist is typing..."):
        greeting = get_greeting_reply(skin_tone=detected_skin_tone, occasion=detected_occasion)

    if greeting["error"] is None:
        st.session_state.chat_messages.append({"role": "assistant", "content": greeting["reply"]})
    else:
        st.error(f"Something went wrong: {greeting['error']}")

incoming_message = None

# ---------------------------------------------------------------
# STEP 4: Quick-reply buttons — shown until the user sends their
# own first real message (the auto-greeting doesn't count)
# ---------------------------------------------------------------
user_message_count = sum(1 for m in st.session_state.chat_messages if m["role"] == "user")
if user_message_count == 0:
    st.caption("Not sure what to ask? Try one of these:")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("👔 What to wear for interview?", width="stretch"):
            incoming_message = "What should I wear for a job interview?"
    with col2:
        if st.button("☀️ Best summer colors?", width="stretch"):
            incoming_message = "What are the best colors for summer?"

# ---------------------------------------------------------------
# STEP 5: Display existing history
# ---------------------------------------------------------------
for message in st.session_state.chat_messages:
    avatar = "🧑" if message["role"] == "user" else "🎨"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# ---------------------------------------------------------------
# STEP 6: Typed input
# ---------------------------------------------------------------
typed_input = st.chat_input("Ask your stylist anything about colors or outfits...")
if typed_input:
    incoming_message = typed_input

# ---------------------------------------------------------------
# STEP 7: Process a new message (button or typed) — same as Day 60
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
            skin_tone=detected_skin_tone,
            occasion=detected_occasion
        )

        typing_placeholder.empty()
        if result["error"]:
            st.error(f"Something went wrong: {result['error']}")
        else:
            st.markdown(result["reply"])
            st.session_state.chat_messages.append({"role": "assistant", "content": result["reply"]})