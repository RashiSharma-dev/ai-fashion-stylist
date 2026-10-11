"""Tests for the outfit recommender and its match scoring."""
import pytest

from recommender import OutfitRecommender


@pytest.fixture(scope="module")
def recommender():
    """Create one OutfitRecommender and share it between the tests (loading the data takes a moment)."""
    return OutfitRecommender()


def test_recommend_returns_outfits_for_the_skin_tone(recommender):
    """recommend() should return 1-5 outfits, each tagged with the skin tone and a match level."""
    outfits = recommender.recommend("warm", "Casual", "Summer", top_n=5)

    assert 0 < len(outfits) <= 5
    for outfit in outfits:
        assert outfit["skin_tone"] == "warm"
        assert outfit["match_level"] in ("exact", "season_relaxed", "color_only")


def test_match_score_follows_the_40_30_30_formula(recommender):
    """The total score must equal 40% skin match + 30% harmony + 30% occasion fit, within 0-100."""
    outfit = recommender.recommend("warm", "Casual", "Summer", top_n=1)[0]
    scores = recommender.calculate_match_score(outfit)

    expected_total = round(
        scores["skin_match"] * 0.4 + scores["color_harmony"] * 0.3 + scores["occasion_fit"] * 0.3
    )
    assert scores["total"] == expected_total
    assert 0 <= scores["total"] <= 100
