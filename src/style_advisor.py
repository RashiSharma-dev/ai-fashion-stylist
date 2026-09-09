# src/style_advisor.py
# Purpose: Combines skin tone + occasion + body shape into one
# cohesive piece of style advice — the "hyper-specific
# recommendation" layer described in the planner.

from occasion_advisor import get_occasion_guidance
from body_shape_advisor import get_body_shape_guidance


def get_combined_style_advice(skin_tone, occasion, body_shape):
    """
    Builds a readable, combined advice summary from all three
    context signals. Any missing piece is simply skipped, so this
    never crashes even with partial information.
    Returns {"error": None or "message", "advice": "..." or None}
    """
    lines = []

    if skin_tone:
        lines.append(f"**Skin Tone:** {skin_tone.capitalize()}")

    if occasion:
        occasion_result = get_occasion_guidance(occasion)
        if occasion_result["error"] is None:
            do_colors = ", ".join(occasion_result["guidance"]["do_colors"])
            lines.append(f"**For {occasion}, favor colors like:** {do_colors}")

    if body_shape:
        shape_result = get_body_shape_guidance(body_shape)
        if shape_result["error"] is None:
            fits = ", ".join(shape_result["guidance"]["recommended_fits"])
            lines.append(f"**For your {body_shape} body shape, look for:** {fits}")

    if not lines:
        return {"error": "Not enough information to build combined advice.", "advice": None}

    return {"error": None, "advice": "\n\n".join(lines)}
