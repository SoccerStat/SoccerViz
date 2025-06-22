from components.queries.execute_query import execute_query
from utils.file_helper.reader import read_sql_file


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

def get_seasons(db_conn, name_comp):
    sql_file = read_sql_file("components/queries/basic_stats/by_comp/seasons.sql", name_comp=name_comp)
    result = execute_query(db_conn, sql_file)

    return result['season'].to_list()