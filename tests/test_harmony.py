"""Tests for the color harmony checker."""
from color_harmony import hex_to_rgb, color_distance, is_good_combination


def test_hex_to_rgb_converts_correctly():
    """A hex code should convert to the right (r, g, b) numbers."""
    assert hex_to_rgb("#ff8800") == (255, 136, 0)


def test_identical_colors_have_zero_distance():
    """Two identical colors should be 0 apart."""
    assert color_distance((10, 20, 30), (10, 20, 30)) == 0


def test_complementary_colors_give_great_contrast():
    """Navy and mustard are a complementary pair, so they should be a good combination."""
    assert is_good_combination("#000080", "#ffdb58") == (True, "Great Contrast")


def test_near_identical_colors_are_too_matchy():
    """Two almost identical navy shades should be flagged as too matchy."""
    assert is_good_combination("#000080", "#000090") == (False, "Too Matchy")
