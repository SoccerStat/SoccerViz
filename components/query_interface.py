import streamlit as st
import streamlit_shortcuts as sts
import pandas as pd
from utils.helpers import format_query_result_info, get_sample_queries


def query_interface():
    """Interface de requêtage SQL"""
    st.header("📊 Requêtes SQL")

    # Informations sur la base
    _display_database_info()

    st.divider()

    # Zone de requête
    _display_query_editor()


def _display_database_info():
    """Affiche les informations sur la base de données"""
    col1, col2 = st.columns(2)

    with col1:
        if st.button("📋 Voir les tables", use_container_width=True):
            with st.spinner("Récupération des tables..."):
                tables_df = st.session_state.db.get_tables()
                if tables_df is not None:
                    st.subheader("Tables disponibles:")
                    st.dataframe(tables_df, use_container_width=True)

    with col2:
        table_name = st.text_input("Infos sur la table:", placeholder="nom_table")
        if table_name and st.button("ℹ️ Détails table", use_container_width=True):
            with st.spinner(f"Récupération des infos de {table_name}..."):
                info_df = st.session_state.db.get_table_info(table_name)
                if info_df is not None:
                    st.subheader(f"Structure de la table '{table_name}':")
                    st.dataframe(info_df, use_container_width=True)


def _display_query_editor():
    """Affiche l'éditeur de requêtes"""
    st.subheader("Exécuter une requête")

    # Exemples de requêtes
    # with st.expander("💡 Exemples de requêtes"):
    #     st.code(get_sample_queries(), language="sql")

    # Éditeur de requête
    query = st.text_area(
        "Votre requête SQL:",
        height=150,
        placeholder="SELECT * FROM upper.player LIMIT 10;",
        key="sql_query"
    )

    col1, col2, col3 = st.columns([1, 1, 4])

    with col1:
        execute_shortcut_btn = sts.shortcut_button("▶️ Exécuter", "cmd+Enter", type="primary")

    with col2:
        if st.button("🗑️ Effacer"):
            st.session_state.sql_query = ""
            st.rerun()

    # Exécution de la requête
    if execute_shortcut_btn and query.strip():
        _execute_query(query)


def _execute_query(query: str):
    """Exécute une requête SQL"""
    with st.spinner("Exécution de la requête..."):
        result_df = st.session_state.db.execute_query(query)

        if result_df is not None:
            st.success(format_query_result_info(result_df))

            # Sauvegarde du résultat pour les graphiques
            st.session_state.last_query_result = result_df
            st.session_state.last_query = query

            # Affichage des résultats
            st.subheader("Résultats:")
            st.dataframe(result_df, use_container_width=True)

            # Statistiques rapides si données numériques
            numeric_cols = result_df.select_dtypes(include=['number']).columns
            if len(numeric_cols) > 0:
                with st.expander("📊 Statistiques rapides"):
                    st.dataframe(result_df[numeric_cols].describe())

            # Bouton de téléchargement
            csv = result_df.to_csv(index=False)
            st.download_button(
                label="📥 Télécharger CSV",
                data=csv,
                file_name="query_results.csv",
                mime="text/csv"
            )