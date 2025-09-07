import streamlit as st

from components.connection import ensure_connection


def set_connection_or_warning(content):
    if ensure_connection():
        # st.success("✅ Database connected and ready to use!")
        content()
    else:
        st.warning("⚠️ Please connect to the database via the sidebar.")
