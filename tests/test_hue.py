"""Tests for the wrap-aware hue average."""
import numpy as np

from color_recommender import wrap_aware_mean_hue


def test_reds_on_both_ends_average_near_zero():
    """Reds at 5 and 175 are the same color family, so the average must stay near red, not green."""
    result = wrap_aware_mean_hue(np.array([5, 175]))
    assert abs(result) < 10


def test_orange_hues_without_wrap_are_unchanged():
    """Hues that do not wrap around keep their normal average."""
    result = wrap_aware_mean_hue(np.array([10, 20, 30]))
    assert result == 20
