import streamlit as st

st.title("📊 Results")

if "uploaded_photo" in st.session_state:
    st.write("Here's the photo you uploaded:")
    st.image(st.session_state.uploaded_photo, caption="Your photo", width=300)
else:
    st.warning("No photo uploaded yet! Go to the Upload page first.")

if "user_name" in st.session_state and st.session_state.user_name:
    st.write(f"Results prepared for: **{st.session_state.user_name}**")