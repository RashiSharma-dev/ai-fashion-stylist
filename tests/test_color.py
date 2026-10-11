"""Tests for skin tone classification and the photo analysis pipeline."""
from color_recommender import classify_skin_tone, analyze_and_recommend


def test_classify_warm_skin():
    """Low hue with strong saturation should be classified as warm."""
    assert classify_skin_tone(15, 70, 200) == "warm"


def test_classify_neutral_skin():
    """Low hue with weak saturation should be classified as neutral."""
    assert classify_skin_tone(15, 50, 200) == "neutral"


def test_classify_cool_skin():
    """A higher hue should be classified as cool."""
    assert classify_skin_tone(25, 70, 200) == "cool"


def test_missing_photo_returns_error_dict():
    """A photo that doesn't exist should give an {"error": ...} dict, never None or a crash."""
    result = analyze_and_recommend("data/this_file_does_not_exist.jpg")

    assert result is not None
    assert result.get("error")
