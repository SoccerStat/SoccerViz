import streamlit as st

from components.queries.execute_query import execute_query
from components.commons.get_seasons import get_all_seasons

from utils.file_helper.reader import read_sql_file
from config import COMPETITIONS


@st.cache_data(show_spinner=False)
def get_all_teams(_db_conn):
    all_comps = [comp["label"] for comp in COMPETITIONS.values()]
    all_seasons = get_all_seasons(_db_conn)
    all_teams = set()

    for comp in all_comps:
        for season in all_seasons:
            teams_by_comp_by_season = set(get_teams_by_comp_by_season(_db_conn, comp, [season[7:]]))
            all_teams = all_teams | teams_by_comp_by_season

    return all_comps, all_seasons, all_teams


@st.cache_data(show_spinner=False)
def get_teams_by_comp_by_season(_db_conn, name_comp, seasons):
    sql_file = read_sql_file(
        "components/queries/team_stats/get_teams_by_comp_by_season.sql",
        name_comp=name_comp,
        seasons=seasons,
    )
    result = execute_query(_db_conn, sql_file)

    return result["Club"].to_list()