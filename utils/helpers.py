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

def get_sample_queries() -> str:
    """Retourne des exemples de requêtes SQL"""
    return """
-- Lister les tables
SELECT table_name FROM information_schema.tables 
WHERE table_schema = 'public';

-- Compter les lignes d'une table
SELECT COUNT(*) FROM ma_table;

-- Sélectionner avec limite
SELECT * FROM ma_table LIMIT 10;

-- Grouper et compter
SELECT colonne1, COUNT(*) as nb 
FROM ma_table 
GROUP BY colonne1 
ORDER BY nb DESC;

-- Jointure simple
SELECT t1.*, t2.colonne 
FROM table1 t1 
JOIN table2 t2 ON t1.id = t2.table1_id;
"""