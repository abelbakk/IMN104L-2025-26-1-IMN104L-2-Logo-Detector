import streamlit as st

st.set_page_config(page_title="Brand Logo Detector", layout="centered", menu_items=None)

st.markdown(
    r"""
    <style>
    .stAppDeployButton {
            visibility: hidden;
        }
    </style>
    """, unsafe_allow_html=True
)

nav = st.navigation(pages=[
    st.Page("pages/detector.py", title="Logo Detector", icon="🕵️", default=True),
    st.Page("pages/brands.py",  title="Supported Brands",  icon="📜")
], position="top")
nav.run()