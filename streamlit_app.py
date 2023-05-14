import streamlit as st

# Contents of ~/my_app/streamlit_app.py
import streamlit as st

def home():
    st.markdown("🏠")
    st.sidebar.markdown("🏠")

def loveit():
    st.markdown("❤️ IT")
    st.sidebar.markdown("#❤️ IT")

def listit():
    st.markdown("📋 IT")
    st.sidebar.markdown("📋 IT")

page_names_to_funcs = {
    "Main Page": home,
    "Love it": loveit,
    "List it": listit,
}

selected_page = st.sidebar.selectbox("Selecciona una página", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()