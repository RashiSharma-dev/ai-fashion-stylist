# src/chatbot.py
import os
from dotenv import load_dotenv
from groq import Groq
import streamlit as st

load_dotenv()
_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL_NAME = "openai/gpt-oss-20b"


def build_system_prompt(skin_tone, occasion=None, body_shape=None):
    if skin_tone:
        context_line = f"The user has a {skin_tone} skin tone."
    else:
        context_line = "The user's skin tone has not been detected yet."

    occasion_line = ""
    if occasion:
        occasion_line = f" They are currently interested in outfits for: {occasion}."

    body_shape_line = ""
    if body_shape:
        body_shape_line = f" Their self-selected body shape is: {body_shape}."

    return (
        "You are a professional fashion color stylist working inside a "
        "styling app. Give specific, actionable advice about clothing "
        "colors, outfit choices, and color combinations. "
                f"{context_line}{occasion_line}{body_shape_line} "
        "Whenever it's relevant to the question, actively incorporate ALL "
        "of the context you have — skin tone, occasion, and body shape — "
        "into your advice, not just in your first message. For example, "
        "fit-related questions (like interview outfits) should reference "
        "body shape, not just skin tone. "
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


def get_chatbot_reply(conversation_history, skin_tone, occasion=None, body_shape=None):
    try:
        system_message = {"role": "system", "content": build_system_prompt(skin_tone, occasion, body_shape)}
        full_messages = [system_message] + conversation_history

        response = _client.chat.completions.create(
            model=MODEL_NAME,
            messages=full_messages
        )
        reply_text = response.choices[0].message.content
        return {"error": None, "reply": reply_text}

    except Exception as e:
        return {"error": str(e), "reply": None}


def get_greeting_reply(skin_tone, occasion=None, body_shape=None):
    occasion_note = ""
    if occasion:
        occasion_note = (
            f" I'm dressing for a specific occasion: {occasion}. "
            "Include one tip that's specifically relevant to that occasion."
        )

    body_shape_note = ""
    if body_shape:
        body_shape_note = f" My body shape is {body_shape} — include one fit tip suited to that."

    kickoff_instruction = {
        "role": "user",
        "content": (
            "Greet me warmly and briefly introduce yourself as my personal "
            "stylist. Summarize my skin tone analysis result in one sentence, "
            f"then give 2-3 quick top color tips based on it.{occasion_note}"
            f"{body_shape_note} Keep it short and friendly, like the start "
            "of a conversation, not a report."
        )
    }
    return get_chatbot_reply(
        conversation_history=[kickoff_instruction],
        skin_tone=skin_tone,
        occasion=occasion,
        body_shape=body_shape
    )


def set_analysis_context(skin_tone, occasion=None, image_path=None, body_shape=None):
    st.session_state["stylist_context"] = {
        "skin_tone": skin_tone,
        "occasion": occasion,
        "image_path": image_path,
        "body_shape": body_shape,
    }
    st.session_state["chat_greeted"] = False
    st.session_state["chat_messages"] = []