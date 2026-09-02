# src/chatbot.py
# Purpose: Handles all communication with the Groq AI chatbot,
# including building the context-aware system prompt and getting replies.

import os
from dotenv import load_dotenv
from groq import Groq

# Load the .env file so we can read the API key
load_dotenv()

# Create ONE client and reuse it (more efficient than creating a new one per message)
_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# The specific model we're using — free tier, fast
MODEL_NAME = "openai/gpt-oss-20b"


def build_system_prompt(skin_tone):
    """
    Builds the instruction that tells the AI who it is and what it
    already knows about this user. This is what makes the chatbot
    'context-aware' instead of generic.
    """
    if skin_tone:
        context_line = f"The user has a {skin_tone} skin tone."
    else:
        context_line = "The user's skin tone has not been detected yet."

    return (
        "You are a professional fashion color stylist working inside a "
        "styling app. Give specific, actionable advice about clothing "
        "colors, outfit choices, and color combinations. "
        f"{context_line} "
        "Keep answers focused on fashion and color styling only. "
        "Keep responses concise (3-5 sentences) unless the user asks "
        "for more detail."
    )


def get_chatbot_reply(conversation_history, skin_tone):
    """
    Sends the full conversation (plus a fresh system prompt) to Groq
    and returns the AI's reply.

    conversation_history: list of {"role": "user"/"assistant", "content": "..."}
                           (does NOT include the system message — we add
                           that fresh every time, in case skin_tone changes)
    skin_tone: string like "warm", "cool", "neutral", or None

    Returns: {"error": None or "message", "reply": "..." or None}
    """
    try:
        system_message = {"role": "system", "content": build_system_prompt(skin_tone)}

        # Put the system message first, followed by the real conversation
        full_messages = [system_message] + conversation_history

        response = _client.chat.completions.create(
            model=MODEL_NAME,
            messages=full_messages
        )

        reply_text = response.choices[0].message.content
        return {"error": None, "reply": reply_text}

    except Exception as e:
        return {"error": str(e), "reply": None}
