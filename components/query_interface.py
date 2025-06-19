import streamlit as st
import streamlit_shortcuts as sts
import pandas as pd
from utils.helpers import format_query_result_info, get_sample_queries


def query_interface(db_conn):
    """Interface de requêtage SQL"""
    st.header("📊 SQL Querying")

    st.divider()

    # Zone de requête
    _display_query_editor(db_conn)


def _display_query_editor(db_conn):
    """Affiche l'éditeur de requêtes"""
    st.subheader("Exécuter une requête")

    # Éditeur de requête
    query = st.text_area(
        "Votre requête SQL:",
        height=150,
        placeholder="SELECT * FROM upper.player LIMIT 10;",
        key="sql_query"
    )

    col1, col2, col3 = st.columns([1, 1, 4])

    with col1:
        execute_shortcut_btn = sts.shortcut_button("▶️ Run", "cmd+Enter", type="primary")

    if execute_shortcut_btn and query.strip():
        _execute_query(db_conn, query)


def _execute_query(db_conn, query: str):
    """Exécute une requête SQL"""
    with st.spinner("Running query ..."):
        result_df = db_conn.execute_query(query)

        if result_df is not None:
            st.success(format_query_result_info(result_df))

            # Sauvegarde du résultat pour les graphiques
            st.session_state.last_query_result = result_df
            st.session_state.last_query = query

            # Affichage des résultats
            st.subheader("Results:")
            st.dataframe(result_df, use_container_width=True)

            csv = result_df.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name="query_results.csv",
                mime="text/csv"
            )