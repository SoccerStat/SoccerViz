import streamlit as st
from components.connection import sidebar_connection
from components.query_interface import query_interface
from components.charts import visualization_interface
from config import APP_CONFIG

def main():
    """Fonction principale de l'application"""
    st.set_page_config(
        page_title=APP_CONFIG['title'],
        page_icon=APP_CONFIG['icon'],
        layout=APP_CONFIG['layout']
    )

    st.title("SoccerStat-II")

    # Initialisation des variables de session
    if 'connected' not in st.session_state:
        st.session_state.connected = False

    # Sidebar pour la connexion
    sidebar_connection()

    if st.button("Basic Stats"):
        st.switch_page("pages/Basic Stats.py")
    if st.button("Monitoring"):
        st.switch_page("pages/Monitoring.py")
    if st.button("Anomaly Detection"):
        st.switch_page("pages/Anomaly Detection.py")
    if st.button("Team Stats"):
        st.switch_page("pages/Team Stats.py")
    if st.button("Player Stats"):
        st.switch_page("pages/Player Stats.py")

    # Interface principale selon l'état de connexion
    if not st.session_state.connected:
        st.info("👈 Veuillez vous connecter à votre base PostgreSQL via la sidebar")

        # Informations d'aide
        with st.expander("ℹ️ Aide à la connexion"):
            st.write("""
            **Paramètres de connexion requis:**
            - **Host**: Adresse IP ou nom de domaine de votre serveur PostgreSQL
            - **Port**: Port de connexion (généralement 5432)
            - **Database**: Nom de la base de données
            - **User**: Nom d'utilisateur PostgreSQL
            - **Password**: Mot de passe
            """)
    else:
        # Interface principale avec onglets
        tab1, tab2 = st.tabs(["🔍 Requêtes", "📊 Graphiques"])

        with tab1:
            query_interface()

        with tab2:
            visualization_interface()


if __name__ == "__main__":
    main()
