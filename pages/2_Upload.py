import streamlit as st
from PIL import Image

st.title("📤 Upload Photo")

# Show the name if it was saved on Home page
if "user_name" in st.session_state and st.session_state.user_name:
    st.write(f"Hi {st.session_state.user_name}! Upload your photo below.")
else:
    st.write("Please upload your photo below.")

uploaded = st.file_uploader("Upload photo", type=['jpg', 'jpeg', 'png'])

if uploaded is not None:
    # Save the uploaded file into session_state so other pages can access it
    st.session_state.uploaded_photo = uploaded
    st.image(uploaded, caption="Uploaded photo", width=300)
    st.success("Photo uploaded! Go to Results page to see it there too.")