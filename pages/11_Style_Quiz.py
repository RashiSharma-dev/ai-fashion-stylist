# pages/11_Style_Quiz.py
# Purpose: 5-question style quiz that classifies the user into a
# Style Personality, stored for use in recommendations and chat.

import streamlit as st
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))
from style_quiz import load_style_quiz, calculate_style_personality, get_persona_details
from theme import apply_theme

apply_theme()

st.title("✨ What's Your Style Personality?")
st.write("Answer these 5 quick questions to find your Style Personality — it'll help personalize your recommendations and chat advice.")

quiz_result = load_style_quiz()

if quiz_result["error"]:
    st.error(quiz_result["error"])
else:
    questions = quiz_result["data"]["questions"]
    answers = []

    for i, q in enumerate(questions):
        option_texts = [opt["text"] for opt in q["options"]]
        choice_text = st.radio(f"**{i+1}. {q['question']}**", option_texts, key=f"quiz_q{i}")

        # Find which persona this chosen option text maps to
        chosen_option = next(opt for opt in q["options"] if opt["text"] == choice_text)
        answers.append(chosen_option["persona"])

    if st.button("🎉 Reveal My Style Personality"):
        result = calculate_style_personality(answers)

        if result["error"]:
            st.error(result["error"])
        else:
            personality = result["personality"]
            st.session_state["style_personality"] = personality

            details_result = get_persona_details(personality)

            st.balloons()
            st.success(f"Your Style Personality: **{personality}**")

            if details_result["error"] is None:
                details = details_result["details"]
                st.write(details["description"])
                st.markdown(f"**Colors that suit you:** {', '.join(details['preferred_colors'])}")
                st.markdown(f"**Fits to look for:** {', '.join(details['preferred_fits'])}")

            st.caption("This is now saved and will inform your outfit recommendations and AI Stylist chat.")