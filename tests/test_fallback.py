"""Tests for the offline fallback replies."""
from fallback_replies import build_offline_reply


def test_offline_reply_names_recommended_colors():
    """A known skin tone gives a reply with no error and the offline notice."""
    result = build_offline_reply("warm", "Casual")
    assert result["error"] is None
    assert "Offline mode" in result["reply"]
    assert "warm" in result["reply"]


def test_offline_reply_without_skin_tone_asks_for_a_photo():
    """With no skin tone, the reply asks the user to analyze a photo first."""
    result = build_offline_reply(None)
    assert result["error"] is None
    assert "photo" in result["reply"].lower()
