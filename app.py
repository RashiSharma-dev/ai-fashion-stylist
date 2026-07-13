import streamlit as st

st.title("AI Fashion Color Fit Matcher")
st.write("Welcome! Upload a photo to discover your best colors.")

name = st.text_input("What's your name?")

if st.button("Say Hello"):
    st.write(f"Hello, {name}! Let's find your perfect colors.")

st.image("data/photo.jpg", caption="Sample photo", width=300)
