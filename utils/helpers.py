import pandas as pd
from typing import List

def get_numeric_columns(df: pd.DataFrame) -> List[str]:
    """Retourne les colonnes numériques d'un DataFrame"""
    return df.select_dtypes(include=['number']).columns.tolist()

def get_categorical_columns(df: pd.DataFrame) -> List[str]:
    """Retourne les colonnes catégorielles d'un DataFrame"""
    return df.select_dtypes(include=['object', 'category']).columns.tolist()

def format_query_result_info(df: pd.DataFrame) -> str:
    """Formate les informations sur le résultat d'une requête"""
    return f"✅ Requête exécutée avec succès! ({len(df)} lignes, {len(df.columns)} colonnes)"