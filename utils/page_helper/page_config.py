import streamlit as st

from config import APP_CONFIG

def set_page_config(page_title, hide_sidebar=True):
    st.set_page_config(
        page_title=page_title,
        page_icon=APP_CONFIG['icon'],
        layout=APP_CONFIG['layout'],
        initial_sidebar_state="collapsed" if hide_sidebar else "expanded",
    )