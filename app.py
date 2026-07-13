import streamlit as st

st.title("AI Fashion Color Fit Matcher")

# ---- SIDEBAR ----
st.sidebar.title("Navigation")
st.sidebar.write("Use this menu to move around the app")
page_choice = st.sidebar.radio("Go to:", ["Home", "Upload", "Results"])

# ---- COLUMNS ----
st.write("### Columns Example")
col1, col2 = st.columns(2)

with col1:
    st.write("This is the left column")
    st.button("Left Button")

with col2:
    st.write("This is the right column")
    st.button("Right Button")

# ---- TABS ----
st.write("### Tabs Example")
tab1, tab2, tab3 = st.tabs(["Upload", "Results", "Chatbot"])

with tab1:
    st.write("This is the Upload tab")
    st.file_uploader("Upload your photo here")

with tab2:
    st.write("This is the Results tab")
    st.write("Your color recommendations will appear here")

with tab3:
    st.write("This is the Chatbot tab")
    st.write("Chat with your AI stylist here")

st.write(f"You selected from sidebar: **{page_choice}**")
