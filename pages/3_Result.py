import streamlit as st

from src.theme import apply_theme
from src.ui_states import empty_state

apply_theme()

st.title("📊 Results")

if "uploaded_photo" in st.session_state:
    st.write("Here's the photo you uploaded:")
    st.image(st.session_state.uploaded_photo, caption="Your photo", width=300)
else:
    empty_state(
        "📊",
        "No photo uploaded yet",
        "Head to the Upload page first, then come back to see your results here."
    )
    st.page_link("pages/2_Upload.py", label="Go to Upload", icon="📤")

if "user_name" in st.session_state and st.session_state.user_name:
    st.write(f"Results prepared for: **{st.session_state.user_name}**")
