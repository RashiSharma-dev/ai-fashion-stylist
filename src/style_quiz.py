# src/style_quiz.py
# Purpose: Loads the style quiz questions, tallies a user's answers
# into a final Style Personality, and provides persona details.

import json
import os

STYLE_QUIZ_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "style_quiz.json")


def load_style_quiz():
    """Returns {"error": None or "message", "data": dict or None}"""
    try:
        with open(STYLE_QUIZ_PATH, "r") as f:
            data = json.load(f)
        return {"error": None, "data": data}
    except Exception as e:
        return {"error": str(e), "data": None}


def calculate_style_personality(answers):
    """
    answers: list of persona strings, one per question answered
    (e.g. ["Classic Minimalist", "Boho Chic", "Classic Minimalist", ...])

    Tallies how many times each persona was picked and returns the
    winner. Ties are broken by whichever persona appeared FIRST in
    the user's answers, so the result is always deterministic.

    Returns {"error": ..., "personality": "...", "scores": {persona: count}}
    """
    if not answers:
        return {"error": "No answers provided.", "personality": None, "scores": None}

    scores = {}
    for persona in answers:
        scores[persona] = scores.get(persona, 0) + 1

    top_score = max(scores.values())
    top_personas = [p for p, s in scores.items() if s == top_score]

    if len(top_personas) == 1:
        winner = top_personas[0]
    else:
        winner = next(p for p in answers if p in top_personas)

    return {"error": None, "personality": winner, "scores": scores}


def get_persona_details(personality):
    """Returns {"error": ..., "details": dict or None}"""
    result = load_style_quiz()
    if result["error"]:
        return {"error": result["error"], "details": None}

    personas = result["data"]["personas"]
    if personality not in personas:
        return {"error": f"No details found for personality '{personality}'.", "details": None}

    return {"error": None, "details": personas[personality]}
