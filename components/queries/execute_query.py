import streamlit as st
from utils.helpers import format_query_result_info

def execute_query(db_conn, query: str):
    """Exécute une requête SQL"""
    return db_conn.execute_query(query)

def result_query(db_conn, query: str):
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