# src/seasonal_colors.py
# Purpose: Loads the seasonal color palette database and auto-detects
# the current season based on today's date — no ML needed, just the
# system clock.

import json
import os
import datetime

PALETTE_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "seasonal_palettes.json")


def load_seasonal_palettes():
    """Loads the full seasonal_palettes.json file.
    Returns {"error": None or "message", "palettes": dict or None}"""
    try:
        with open(PALETTE_PATH, "r") as f:
            data = json.load(f)
        return {"error": None, "palettes": data}
    except Exception as e:
        return {"error": str(e), "palettes": None}


def get_current_season():
    """
    Auto-detects the current fashion season using the system date.
    Uses standard Northern Hemisphere meteorological seasons:
    Spring (Mar-May), Summer (Jun-Aug), Autumn (Sep-Nov), Winter (Dec-Feb).
    """
    month = datetime.datetime.now().month

    if month in [3, 4, 5]:
        return "Spring"
    elif month in [6, 7, 8]:
        return "Summer"
    elif month in [9, 10, 11]:
        return "Autumn"
    else:
        return "Winter"


def get_seasonal_palette(season):
    """
    Returns the full palette (colors + fabric + pattern suggestions)
    for a given season name.
    Returns {"error": None or "message", "palette": dict or None}
    """
    result = load_seasonal_palettes()
    if result["error"]:
        return {"error": result["error"], "palette": None}

    palettes = result["palettes"]
    if season not in palettes:
        return {"error": f"Season '{season}' not found in palette data.", "palette": None}

    return {"error": None, "palette": palettes[season]}
