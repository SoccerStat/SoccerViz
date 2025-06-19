import streamlit as st
from utils.database import create_database_connection, save_persistent_credentials, \
    clear_session, init_session_state
from config import DATABASE_CONFIG


def sidebar_connection():
    """Interface de connexion dans la sidebar"""

    init_session_state()

    st.sidebar.header("🔐 PostgreSQL Connection")

    if st.session_state.connected:
        st.sidebar.success("🟢 Connected")
    else:
        st.sidebar.error("🔴 Disconnected")

    if not st.session_state.connected:
        with st.sidebar.form("connection_form"):
            creds = st.session_state.db_credentials
            host = st.text_input("Host", value=creds.get('host', DATABASE_CONFIG['default_host']))
            port = st.text_input("Port", value=creds.get('port', DATABASE_CONFIG['default_port']))
            user = st.text_input("User", value=creds.get('user', DATABASE_CONFIG['default_user']))
            password = st.text_input("Password", type="password")
            database = st.text_input("Database", value=creds.get('database', DATABASE_CONFIG['default_database']))

            submit = st.form_submit_button("Connect", type="primary")

            if submit:
                if all([host, port, user, password, database]):
                    with st.spinner("Establishing database connection..."):
                        try:
                            save_persistent_credentials(host, port, database, user, password)
                            db = create_database_connection(host=host, port=port, database=database, user=user, password=password)

                            if db:
                                st.session_state.db_conn = db
                                st.session_state.connected = True

                                st.sidebar.success("✅ Connected!")
                                st.rerun()
                            else:
                                st.sidebar.error("❌ Connection failed!")
                                st.session_state.connected = False
                        except Exception as e:
                            st.sidebar.error(f"Error: {str(e)}")
                            st.session_state.connected = False
                else:
                    st.sidebar.error("Please fill these fields")

    # Affichage des informations de connexion
    if st.session_state.connected and st.session_state.db_conn is not None:
        st.sidebar.divider()
        st.sidebar.subheader("📋 Active Connection")

        info = st.session_state.db_credentials
        if info:
            st.sidebar.text(f"Host: {info.get('host', 'N/A')}")
            st.sidebar.text(f"Database: {info.get('database', 'N/A')}")
            st.sidebar.text(f"User: {info.get('user', 'N/A')}")

            # Bouton de déconnexion
            if st.sidebar.button("🔌 Disconnect"):
                clear_session()
                st.sidebar.success("Successfully disconnected")
                st.rerun()


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