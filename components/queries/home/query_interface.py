import streamlit as st
import streamlit_shortcuts as sts

from components.queries.execute_query import result_query


def query_interface(db_conn):
    """Interface de requêtage SQL"""
    st.header("📊 SQL Querying")

    st.divider()

    _display_query_editor(db_conn)


def _display_query_editor(db_conn):
    """Affiche l'éditeur de requêtes"""
    st.subheader("Exécuter une requête")

    query = st.text_area(
        "Votre requête SQL:",
        height=150,
        placeholder="SELECT * FROM upper.player LIMIT 10;",
        key="sql_query"
    )

    col1, col2, col3 = st.columns([1, 1, 4])

    with col1:
        execute_shortcut_btn = sts.shortcut_button("▶️ Run", "cmd+Enter")

    if execute_shortcut_btn and query.strip():
        result_query(db_conn, query)
