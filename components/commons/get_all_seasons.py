from components.queries.execute_query import execute_query
from utils.file_helper.reader import read_sql_file


def get_all_seasons(db_conn):
    sql_file = read_sql_file("components/queries/commons/all_seasons.sql")
    result = execute_query(db_conn, sql_file)
    return result['schema_name'].to_list()

def get_seasons(db_conn, name_comp):
    sql_file = read_sql_file("components/queries/basic_stats/by_comp/seasons.sql", name_comp=name_comp)
    result = execute_query(db_conn, sql_file)

    return result['season'].to_list()