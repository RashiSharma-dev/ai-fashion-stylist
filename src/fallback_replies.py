"""Offline fallback: gives simple stylist tips without the internet or the Groq API."""
import logging

from color_recommender import load_color_rules

# Used to record unexpected errors in the terminal (instead of print)
logger = logging.getLogger(__name__)

OFFLINE_NOTICE = "Offline mode: the AI service is unavailable, so this answer comes from built-in style rules."


def build_offline_reply(skin_tone=None, occasion=None):
    """
    Build a simple stylist reply from the color rules, with no internet needed.

    skin_tone: "warm", "neutral", or "cool" (None if no photo was analyzed yet).
    occasion: optional text such as "Casual", added to the reply if given.
    Returns {"error": None, "reply": "..."} on success, or
    {"error": "friendly message", "reply": ""} if the color rules can't be read.
    """
    try:
        rules = load_color_rules()

        if skin_tone not in rules:
            reply = (
                f"{OFFLINE_NOTICE} Please analyze a photo first on the "
                "Analyze My Look page, and I can suggest colors for your skin tone."
            )
            return {"error": None, "reply": reply}

        color_names = [color["name"] for color in rules[skin_tone]["best_colors"]]
        occasion_text = f" for a {occasion} occasion" if occasion else ""
        reply = (
            f"{OFFLINE_NOTICE} For {skin_tone} skin tones{occasion_text}, "
            f"your best colors are {', '.join(color_names)}. "
            "Pair a top in one of these with a neutral bottom such as black, white, or navy."
        )
        return {"error": None, "reply": reply}

    except Exception:
        logger.exception("Could not build the offline reply")
        return {"error": "Offline style tips are unavailable right now.", "reply": ""}
