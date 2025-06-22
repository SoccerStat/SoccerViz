from components.queries.execute_query import execute_query

def get_all_seasons(db_conn):
    query = """
            SELECT schema_name 
            FROM information_schema.schemata 
            WHERE schema_name LIKE 'season_%%'
            AND EXISTS (
                SELECT 1
                FROM information_schema.tables
                WHERE table_schema = schema_name
                  AND table_name = 'match'
            )
            ORDER BY schema_name;
    """
    result = execute_query(db_conn, query)
    return result['schema_name'].to_list()