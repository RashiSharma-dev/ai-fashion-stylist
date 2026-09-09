# src/body_shape_advisor.py
# Purpose: Loads body-shape-specific fit guidance. Body shape is
# user-selected, not auto-detected — see README Future Scope for why.

import json
import os

BODY_SHAPE_RULES_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "body_shape_rules.json")


def load_body_shape_rules():
    """Returns {"error": None or "message", "rules": dict or None}"""
    try:
        with open(BODY_SHAPE_RULES_PATH, "r") as f:
            data = json.load(f)
        return {"error": None, "rules": data}
    except Exception as e:
        return {"error": str(e), "rules": None}


def get_body_shape_guidance(body_shape):
    """Returns {"error": None or "message", "guidance": dict or None}"""
    result = load_body_shape_rules()
    if result["error"]:
        return {"error": result["error"], "guidance": None}

    rules = result["rules"]
    if body_shape not in rules:
        return {"error": f"No guidance found for body shape '{body_shape}'.", "guidance": None}

    return {"error": None, "guidance": rules[body_shape]}
