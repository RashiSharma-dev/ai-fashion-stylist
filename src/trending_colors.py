# src/trending_colors.py
# Purpose: Loads curated trending color data by year, surfaces the
# Pantone Color of the Year, and provides an instant skin-tone
# compatibility check for any trending color.

import json
import os
import datetime

TRENDING_COLORS_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "trending_colors.json")


def load_trending_data():
    """Returns {"error": None or "message", "data": dict or None}"""
    try:
        with open(TRENDING_COLORS_PATH, "r") as f:
            data = json.load(f)
        return {"error": None, "data": data}
    except Exception as e:
        return {"error": str(e), "data": None}


def get_trending_colors(year=None):
    """Returns the trending color list for a given year (defaults to
    the current year). Returns {"error": ..., "colors": ..., "year": ...}"""
    if year is None:
        year = str(datetime.datetime.now().year)
    else:
        year = str(year)

    result = load_trending_data()
    if result["error"]:
        return {"error": result["error"], "colors": None, "year": year}

    colors = result["data"]["trending_by_year"].get(year)
    if colors is None:
        return {"error": f"No trending colors recorded for {year}.", "colors": None, "year": year}

    return {"error": None, "colors": colors, "year": year}


def get_pantone_color_of_year(year=None):
    """Returns Pantone's Color of the Year for a given year (defaults
    to the current year). Returns {"error": ..., "pantone": ...}"""
    if year is None:
        year = str(datetime.datetime.now().year)
    else:
        year = str(year)

    result = load_trending_data()
    if result["error"]:
        return {"error": result["error"], "pantone": None}

    pantone = result["data"]["pantone_color_of_year"].get(year)
    if pantone is None:
        return {"error": f"No Pantone Color of the Year recorded for {year}.", "pantone": None}

    return {"error": None, "pantone": pantone}


def check_color_compatibility(color_undertone, skin_tone):
    """
    Instant compatibility check: matching undertones = a great pairing,
    neutral undertones work with anything, mismatched undertones get a
    gentle heads-up with a tip rather than a flat "no".
    Returns {"error": ..., "compatible": True/False/None, "message": ...}
    """
    if not skin_tone:
        return {"error": "No skin tone detected yet — analyze your look first.", "compatible": None, "message": None}

    skin_tone = skin_tone.lower()
    color_undertone = color_undertone.lower()

    if color_undertone == "neutral" or skin_tone == "neutral":
        return {"error": None, "compatible": True, "message": "This is a versatile color that works well with your skin tone."}

    if color_undertone == skin_tone:
        return {"error": None, "compatible": True, "message": f"Great match! This {color_undertone}-toned color complements your {skin_tone} skin tone beautifully."}

    return {
        "error": None,
        "compatible": False,
        "message": f"This is a {color_undertone}-toned color, which can be trickier with a {skin_tone} skin tone — try pairing it with a {skin_tone}-toned neutral to balance it out."
    }
