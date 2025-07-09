from components.queries.execute_query import execute_query
from utils.file_helper.reader import read_sql_file

def get_teams_by_comp_by_season(db_conn, name_comp, seasons):
    sql_file = read_sql_file(
        "components/queries/team_stats/get_teams_by_comp_by_season.sql",
        name_comp=name_comp,
        seasons=seasons,
    )
    result = execute_query(db_conn, sql_file)

    return result["Club"].to_list()