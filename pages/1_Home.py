import streamlit as st

st.title("🏠 Home")
st.write("Welcome to AI Fashion Color Fit Matcher!")
st.write("Use the sidebar to navigate to Upload your photo.")

# Initialize session state if it doesn't exist yet
if "user_name" not in st.session_state:
    st.session_state.user_name = ""

name = st.text_input("What's your name?", value=st.session_state.user_name)

if st.button("Save Name"):
    st.session_state.user_name = name
    st.success(f"Saved! Welcome, {name}")
