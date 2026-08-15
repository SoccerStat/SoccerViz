import streamlit as st
import streamlit_shortcuts as sts

from components.pages.home.helpers import result_query


def set_query_interface(db_conn):
    """Interface de requêtage SQL"""
    st.header("📊 SQL Querying")

    st.divider()

    _display_query_editor(db_conn)


def _display_query_editor(db_conn):
    """Affiche l'éditeur de requêtes"""
    st.subheader("Execute a query")

    query = st.text_area(
        label="Your SQL query:",
        height=150,
        placeholder="SELECT * FROM upper.player LIMIT 10;",
        key="sql_query"
    )

    col1, _ = st.columns([1, 5])

    with col1:
        execute_shortcut_btn = sts.shortcut_button("▶️ Run", "Cmd+Enter")

    if execute_shortcut_btn and query.strip():
        result_query(db_conn, query)
