import streamlit as st

from utils.database import init_session_state


def ensure_connection():
    """Vérifie et maintient la connexion active"""
    if st.session_state.get('connected', False):
        init_session_state()

    return st.session_state.get('connected', False) and st.session_state.get('db_conn') is not None


# Fonction pour obtenir la connexion active
def get_connection():
    """Retourne la connexion active ou None"""
    if ensure_connection():
        return st.session_state.db_conn
    return None
