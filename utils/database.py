import pandas as pd
import psycopg2
from sqlalchemy import create_engine
from typing import Optional
import streamlit as st


class DatabaseConnection:
    """Gestionnaire de connexion PostgreSQL"""

    def __init__(self):
        self.connection = None
        self.engine = None

    def connect(self, host: str, port: str, user: str, password: str, database: str) -> bool:
        """Établit la connexion à PostgreSQL"""
        try:
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
        except Exception as e:
            st.error(f"Erreur de connexion : {str(e)}")
            return False

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

    def get_tables(self) -> Optional[pd.DataFrame]:
        """Récupère la liste des tables"""
        query = """
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                ORDER BY table_name; \
                """
        return self.execute_query(query)

    def get_table_info(self, table_name: str) -> Optional[pd.DataFrame]:
        """Récupère les informations sur une table"""
        query = f"""
        SELECT column_name, data_type, is_nullable
        FROM information_schema.columns 
        WHERE table_name = '{table_name}'
        ORDER BY ordinal_position;
        """
        return self.execute_query(query)

    def close(self):
        """Ferme la connexion"""
        if self.connection:
            self.connection.close()
        if self.engine:
            self.engine.dispose()