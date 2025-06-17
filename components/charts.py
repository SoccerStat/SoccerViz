import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils.helpers import get_numeric_columns, get_categorical_columns
from config import CHART_CONFIG


def visualization_interface():
    """Interface de visualisation des données"""
    st.header("📈 Visualisations")

    if 'last_query_result' not in st.session_state:
        st.info("💡 Exécutez d'abord une requête dans l'onglet 'Requêtes' pour générer des graphiques")
        return

    df = st.session_state.last_query_result

    if df.empty:
        st.warning("Aucune donnée à visualiser")
        return

    st.subheader(f"Données de la dernière requête ({len(df)} lignes)")

    # Analyse des colonnes
    numeric_columns = get_numeric_columns(df)
    categorical_columns = get_categorical_columns(df)

    # Interface de visualisation
    _display_basic_charts(df, numeric_columns, categorical_columns)
    _display_advanced_charts(df, numeric_columns, categorical_columns)


def _display_basic_charts(df, numeric_columns, categorical_columns):
    """Affiche les graphiques de base"""
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Graphique en barres")
        if categorical_columns and numeric_columns:
            x_col = st.selectbox("Axe X (catégorie):", categorical_columns, key="bar_x")
            y_col = st.selectbox("Axe Y (valeur):", numeric_columns, key="bar_y")

            if st.button("Générer graphique en barres"):
                fig = px.bar(
                    df, x=x_col, y=y_col,
                    title=f"{y_col} par {x_col}",
                    color_discrete_sequence=CHART_CONFIG['color_palette']
                )
                fig.update_layout(height=CHART_CONFIG['default_height'])
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Besoin de colonnes catégorielles et numériques")

    with col2:
        st.subheader("📈 Graphique linéaire")
        if len(numeric_columns) >= 2:
            x_col = st.selectbox("Axe X:", numeric_columns, key="line_x")
            y_col = st.selectbox("Axe Y:", numeric_columns, key="line_y")

            if st.button("Générer graphique linéaire"):
                fig = px.line(
                    df, x=x_col, y=y_col,
                    title=f"{y_col} vs {x_col}",
                    color_discrete_sequence=CHART_CONFIG['color_palette']
                )
                fig.update_layout(height=CHART_CONFIG['default_height'])
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Besoin d'au moins 2 colonnes numériques")


def _display_advanced_charts(df, numeric_columns, categorical_columns):
    """Affiche les graphiques avancés"""
    st.subheader("📊 Autres visualisations")

    chart_type = st.selectbox(
        "Type de graphique:",
        ["Histogramme", "Scatter plot", "Box plot", "Heatmap (corrélation)"]
    )

    if chart_type == "Histogramme" and numeric_columns:
        col = st.selectbox("Colonne:", numeric_columns, key="hist_col")
        bins = st.slider("Nombre de bins:", 10, 100, 30)

        if st.button("Générer histogramme"):
            fig = px.histogram(
                df, x=col, nbins=bins,
                title=f"Distribution de {col}",
                color_discrete_sequence=CHART_CONFIG['color_palette']
            )
            fig.update_layout(height=CHART_CONFIG['default_height'])
            st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Scatter plot" and len(numeric_columns) >= 2:
        col1, col2 = st.columns(2)
        with col1:
            x_col = st.selectbox("Axe X:", numeric_columns, key="scatter_x")
            y_col = st.selectbox("Axe Y:", numeric_columns, key="scatter_y")
        with col2:
            color_col = st.selectbox("Couleur (optionnel):", ["Aucune"] + categorical_columns, key="scatter_color")
            size_col = st.selectbox("Taille (optionnel):", ["Aucune"] + numeric_columns, key="scatter_size")

        if st.button("Générer scatter plot"):
            color = None if color_col == "Aucune" else color_col
            size = None if size_col == "Aucune" else size_col

            fig = px.scatter(
                df, x=x_col, y=y_col, color=color, size=size,
                title=f"{y_col} vs {x_col}",
                color_discrete_sequence=CHART_CONFIG['color_palette']
            )
            fig.update_layout(height=CHART_CONFIG['default_height'])
            st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Box plot" and numeric_columns:
        y_col = st.selectbox("Variable numérique:", numeric_columns, key="box_y")
        x_col = st.selectbox("Catégorie (optionnel):", ["Aucune"] + categorical_columns, key="box_x")

        if st.button("Générer box plot"):
            x = None if x_col == "Aucune" else x_col
            fig = px.box(
                df, x=x, y=y_col,
                title=f"Box plot de {y_col}" + (f" par {x_col}" if x else ""),
                color_discrete_sequence=CHART_CONFIG['color_palette']
            )
            fig.update_layout(height=CHART_CONFIG['default_height'])
            st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Heatmap (corrélation)" and len(numeric_columns) >= 2:
        if st.button("Générer heatmap de corrélation"):
            corr_matrix = df[numeric_columns].corr()
            fig = px.imshow(
                corr_matrix,
                text_auto=True,
                aspect="auto",
                title="Matrice de corrélation",
                color_continuous_scale="RdBu"
            )
            fig.update_layout(height=CHART_CONFIG['default_height'])
            st.plotly_chart(fig, use_container_width=True)