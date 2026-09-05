# src/chatbot.py
# Purpose: Handles all communication with the Groq AI chatbot,
# including context-aware prompts, scope limiting, conversation
# memory, and auto-personalized greetings after an analysis completes.

import os
from dotenv import load_dotenv
from groq import Groq
import streamlit as st

load_dotenv()
_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL_NAME = "openai/gpt-oss-20b"


def build_system_prompt(skin_tone, occasion=None):
    """Builds the AI's standing instructions, including whatever
    context we currently know about the user, plus scope-limiting
    rules so the bot stays focused on fashion."""
    if skin_tone:
        context_line = f"The user has a {skin_tone} skin tone."
    else:
        context_line = "The user's skin tone has not been detected yet."

    occasion_line = ""
    if occasion:
        occasion_line = f" They are currently interested in outfits for: {occasion}."

    return (
        "You are a professional fashion color stylist working inside a "
        "styling app. Give specific, actionable advice about clothing "
        "colors, outfit choices, and color combinations. "
        f"{context_line}{occasion_line} "
        "SCOPE RULE: Only answer questions about fashion, clothing colors, "
        "outfit choices, styling, and color theory. If the user asks about "
        "anything unrelated (sports, politics, homework, coding, trivia, "
        "entertainment, medical advice, etc.), politely decline and redirect "
        "them back to fashion — for example: 'I'm a fashion stylist! Ask me "
        "about colors, outfits, or style tips.' "
        "SENSITIVE TOPICS: If the user expresses sadness, stress, or emotional "
        "distress, do not simply redirect them to fashion topics. Respond with "
        "warmth first, gently acknowledge that this is outside what you're "
        "able to help with as a styling assistant, and encourage them to talk "
        "to someone they trust. "
        "Keep responses concise (3-5 sentences) unless the user asks "
        "for more detail."
    )


def get_chatbot_reply(conversation_history, skin_tone, occasion=None):
    """Sends the conversation + fresh context to Groq and returns the reply.
    Always returns {"error": None or "message", "reply": "..." or None}."""
    try:
        system_message = {"role": "system", "content": build_system_prompt(skin_tone, occasion)}
        full_messages = [system_message] + conversation_history

        response = _client.chat.completions.create(
            model=MODEL_NAME,
            messages=full_messages
        )
        reply_text = response.choices[0].message.content
        return {"error": None, "reply": reply_text}

    except Exception as e:
        return {"error": str(e), "reply": None}


def get_greeting_reply(skin_tone, occasion=None):
    """
    Generates a personalized OPENING message with no real user question —
    this is what makes the chat feel like the AI 'already knows' the user
    the moment they arrive.
    """
    kickoff_instruction = {
        "role": "user",
        "content": (
            "Greet me warmly and briefly introduce yourself as my personal "
            "stylist. Summarize my skin tone analysis result in one sentence, "
            "then give 2-3 quick top color tips based on it. Keep it short "
            "and friendly, like the start of a conversation, not a report."
        )
    }
    return get_chatbot_reply(conversation_history=[kickoff_instruction], skin_tone=skin_tone, occasion=occasion)


def set_analysis_context(skin_tone, occasion=None, image_path=None):
    """
    Call this right after ANY successful analysis in the app (skin tone
    detection, outfit compatibility, etc.) so the chatbot can pick up
    the latest context automatically. This is the single standardized
    place all analysis results should be recorded for chat purposes.
    """
    st.session_state["stylist_context"] = {
        "skin_tone": skin_tone,
        "occasion": occasion,
        "image_path": image_path,
    }
    st.session_state["chat_greeted"] = False
    st.session_state["chat_messages"] = []