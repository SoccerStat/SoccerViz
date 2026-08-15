from sqlalchemy import text


def execute_query(db_conn, query: str):
    """Exécute une requête SQL"""
    return db_conn.execute_query(text(query))
