# src/occasion_advisor.py
# Purpose: Loads occasion-specific DO/DON'T color guidance, and maps
# the 6 specific occasions shown to the user down to the 3 broad
# categories ("Formal"/"Casual"/"Party") that OutfitRecommender uses.

import json
import os

OCCASION_RULES_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "occasion_rules.json")


def load_occasion_rules():
    """Loads the full occasion_rules.json file.
    Returns {"error": None or "message", "rules": dict or None}"""
    try:
        with open(OCCASION_RULES_PATH, "r") as f:
            data = json.load(f)
        return {"error": None, "rules": data}
    except Exception as e:
        return {"error": str(e), "rules": None}


def get_occasion_guidance(occasion):
    """Returns the DO/DON'T color guidance for one specific occasion.
    Returns {"error": None or "message", "guidance": dict or None}"""
    result = load_occasion_rules()
    if result["error"]:
        return {"error": result["error"], "guidance": None}

    rules = result["rules"]
    if occasion not in rules:
        return {"error": f"No guidance found for occasion '{occasion}'.", "guidance": None}

    return {"error": None, "guidance": rules[occasion]}


def map_to_recommender_occasion(occasion):
    """
    Maps a specific occasion (e.g. 'Wedding Guest') down to the broad
    category ('Formal') that the existing OutfitRecommender scoring
    engine was built around. Falls back to 'Casual' if anything is
    missing, so this never crashes the recommendation flow.
    """
    result = get_occasion_guidance(occasion)
    if result["error"]:
        return "Casual"
    return result["guidance"].get("maps_to_recommender", "Casual")
