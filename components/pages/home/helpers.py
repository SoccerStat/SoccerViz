import pandas as pd
import streamlit as st
from typing import List

from components.queries.execute_query import execute_query
from components.commons.set_button_style import set_button_with_style

from config import PAGES_CONFIG


def set_contents_table_buttons():
    with st.container():
        cols = st.columns(len(PAGES_CONFIG))
        for i, page in enumerate(sorted(PAGES_CONFIG)):
            with cols[i]:
                key = f"nav_{page}"
                with set_button_with_style(key):
                    if st.button(page, key=key):
                        st.switch_page(f"pages/{page}.py")


def get_numeric_columns(df: pd.DataFrame) -> List[str]:
    """Retourne les colonnes numériques d'un DataFrame"""
    return df.select_dtypes(include=['number']).columns.tolist()


def get_categorical_columns(df: pd.DataFrame) -> List[str]:
    """Retourne les colonnes catégorielles d'un DataFrame"""
    return df.select_dtypes(include=['object', 'category']).columns.tolist()


def result_query(db_conn, query: str):
    with st.spinner("Running query ..."):
        result_df = execute_query(db_conn, query)

        if result_df is not None:
            st.success(_format_query_result_info(result_df))

            st.session_state.last_query_result = result_df
            st.session_state.last_query = query

            st.subheader("Results:")
            st.dataframe(result_df, use_container_width=True)

            csv = result_df.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name="query_results.csv",
                mime="text/csv"
            )


def _format_query_result_info(df: pd.DataFrame) -> str:
    """Formate les informations sur le résultat d'une requête"""
    return f"✅ Query executed successfully! ({len(df)} rows, {len(df.columns)} columns)"
