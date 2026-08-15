import streamlit as st

from utils.database_helper.database import init_session_state


def set_connection_or_warning(content):
    if _ensure_connection():
        # st.success("✅ Database connected and ready to use!")
        content()
    else:
        st.warning("⚠️ Please connect to the database via the sidebar.")


def get_connection():
    """Retourne la connexion active ou None"""
    if _ensure_connection():
        return st.session_state.db_conn
    return None


def _ensure_connection():
    """Vérifie et maintient la connexion active"""
    if st.session_state.get('connected', False):
        init_session_state()

    return st.session_state.get('connected', False) and st.session_state.get('db_conn') is not None
