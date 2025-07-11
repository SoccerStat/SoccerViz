import pandas as pd
import psycopg2
from sqlalchemy import create_engine
from typing import Optional
import streamlit as st
import hashlib


class DatabaseConnection:
    """Gestionnaire de connexion PostgreSQL"""

    def __init__(self):
        self.connection = None
        self.engine = None

    def connect(self, host: str, port: str, user: str, password: str, database: str) -> bool:
        """Établit la connexion à PostgreSQL"""
        # Connexion avec psycopg2
        self.connection = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )

        # Engine SQLAlchemy pour pandas
        connection_string = f"postgresql://{user}:{password}@{host}:{port}/{database}"
        self.engine = create_engine(connection_string)

        return True

    def execute_query(self, query: str) -> Optional[pd.DataFrame]:
        """Exécute une requête et retourne un DataFrame"""
        try:
            if self.engine is None:
                st.error("Pas de connexion à la base de données")
                return None

            df = pd.read_sql_query(query, self.engine)
            return df
        except Exception as e:
            st.error(f"Erreur lors de l'exécution de la requête : {str(e)}")
            return None

    def close(self):
        """Ferme la connexion"""
        if self.connection:
            self.connection.close()
        if self.engine:
            self.engine.dispose()

@st.cache_resource
def create_database_connection(host, port, user, password, database):
    """Crée et cache une connexion à la base de données"""
    db = DatabaseConnection()
    if db.connect(host, port, user, password, database):
        return db
    return None


def init_session_state():
    """Initialise les variables de session avec persistance"""
    # Initialisation des variables de base
    st.session_state.setdefault("db_conn", None)

    st.session_state.setdefault("connected", False)

    st.session_state.setdefault("db_credentials", {})

    # Clé unique pour identifier la session de connexion
    st.session_state.setdefault("connection_hash", None)

    # Tentative de restauration de la connexion si les credentials existent
    if st.session_state.db_credentials and not st.session_state.connected:
        restore_connection()


def restore_connection():
    """Restaure la connexion depuis les credentials en cache"""
    creds = st.session_state.db_credentials

    if all(key in creds for key in ['host', 'port', 'user', 'password', 'database']) and creds['password']:
        try:
            # Génère un hash unique pour cette configuration de connexion
            config_str = f"{creds['host']}:{creds['port']}:{creds['database']}:{creds['user']}"
            connection_hash = hashlib.md5(config_str.encode()).hexdigest()

            # Si le hash correspond, tente de restaurer la connexion
            db = create_database_connection(
                creds['host'],
                creds['port'],
                creds['user'],
                creds['password'],
                creds['database']
            )
            if db:
                st.session_state.db_conn = db
                st.session_state.connected = True
                st.session_state.connection_hash = connection_hash
                return True

        except Exception as e:
            clear_session()
    else:
        st.warning("Impossible de restaurer la connexion : mot de passe absent ou incomplet.")

    return False


def save_persistent_credentials(host, port, database, user, password):
    """Sauvegarde les credentials de manière persistante"""
    credentials = {
        'host': host,
        'port': port,
        'database': database,
        'user': user,
        'password': password  # En production, chiffrez ce mot de passe
    }

    # Génère un hash pour cette configuration
    config_str = f"{host}:{port}:{database}:{user}"
    connection_hash = hashlib.md5(config_str.encode()).hexdigest()

    # Sauvegarde dans session_state
    st.session_state.db_credentials = credentials
    st.session_state.connection_hash = connection_hash

    # Optionnel: Sauvegarde dans le cache navigateur (attention sécurité)
    # En production, utilisez un système de session sécurisé
    try:
        # Utilise les secrets Streamlit pour le chiffrement (optionnel)
        st.session_state.persistent_connection = True
    except Exception as e:
        st.sidebar.warning("Session persistante non disponible")

def clear_session():
    """Nettoie complètement la session"""
    if st.session_state.db_conn:
        try:
            st.session_state.db_conn.close()
        except:
            pass

    st.session_state.db_conn = None
    st.session_state.connected = False
    st.session_state.db_credentials = {}
    st.session_state.connection_hash = None

    # Nettoie également le cache
    # st.cache_resource.clear()