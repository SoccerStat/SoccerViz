import streamlit as st
from utils.database import DatabaseConnection
from config import DATABASE_CONFIG


def sidebar_connection():
    """Interface de connexion dans la sidebar"""
    st.sidebar.header("🔐 Connexion PostgreSQL")

    with st.sidebar.form("connection_form"):
        host = st.text_input("Host", value=DATABASE_CONFIG['default_host'])
        port = st.text_input("Port", value=DATABASE_CONFIG['default_port'])
        database = st.text_input("Database", value=DATABASE_CONFIG['default_database'])
        user = st.text_input("User", value=DATABASE_CONFIG['default_user'])
        password = st.text_input("Password", type="password")

        submit = st.form_submit_button("Se connecter", type="primary")

        if submit:
            if all([host, port, user, password, database]):
                with st.spinner("Connexion en cours..."):
                    db = DatabaseConnection()
                    if db.connect(host, port, user, password, database):
                        st.session_state.db = db
                        st.session_state.connected = True
                        st.session_state.connection_info = {
                            'host': host,
                            'port': port,
                            'database': database,
                            'user': user
                        }
                        st.sidebar.success("✅ Connexion établie!")
                        st.rerun()
                    else:
                        st.session_state.connected = False
            else:
                st.sidebar.error("Veuillez remplir tous les champs")

    # Affichage des informations de connexion
    if st.session_state.get('connected', False):
        st.sidebar.divider()
        st.sidebar.subheader("📋 Connexion active")
        info = st.session_state.get('connection_info', {})
        st.sidebar.text(f"Host: {info.get('host', 'N/A')}")
        st.sidebar.text(f"Database: {info.get('database', 'N/A')}")
        st.sidebar.text(f"User: {info.get('user', 'N/A')}")

        if st.sidebar.button("🔌 Déconnecter"):
            if 'db' in st.session_state:
                st.session_state.db.close()
            st.session_state.connected = False
            st.session_state.clear()
            st.rerun()