"""Tests for the two safety fixes: HTML escaping in reports and safe profile file names."""
import os

from report_generator import generate_style_report
from user_profile import PROFILE_DIR, _profile_path


def test_report_escapes_html_in_the_name():
    """A name containing HTML must appear as harmless text, not as real HTML."""
    outfits = [{
        "outfit_id": 1,
        "top_color": "Red",
        "bottom_color": "Black",
        "occasion": "Casual",
        "style_type": "Modern",
        "scores": {"total": 80},
    }]
    report = generate_style_report("<script>alert(1)</script>", "warm", outfits)
    assert "<script>" not in report
    assert "&lt;script&gt;" in report


def test_profile_path_blocks_folder_tricks():
    """A name with path characters must still save inside the profiles folder."""
    path = _profile_path("../../evil name")
    assert os.path.dirname(path) == PROFILE_DIR
    assert ".." not in path
    assert path.endswith("evil_name.json")


def test_profile_path_is_none_for_unusable_names():
    """A name made only of symbols has no safe file name, so no path is returned."""
    assert _profile_path("  ../ ") is None
