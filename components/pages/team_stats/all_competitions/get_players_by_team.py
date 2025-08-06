import streamlit as st

from components.commons.get_all_teams import get_teams_by_comp_by_season
from components.commons.get_seasons import get_all_seasons
from components.queries.execute_query import execute_query

from utils.file_helper.reader import read_sql_file


@st.cache_data(show_spinner=False)
def get_players_with_given_rate_minutes(_db_conn, chosen_season, chosen_team, chosen_rate, chosen_side, r=3):
    sql_file = read_sql_file(
        file_name="components/queries/team_stats/all_competitions/players_by_team/get_players_with_given_rate_minutes.sql",
        chosen_season=chosen_season,
        name_team=chosen_team,
        rate=chosen_rate,
        in_side=chosen_side.lower(),
        r=r
    )

    return execute_query(_db_conn, sql_file)

def get_players_by_team(db_conn):
    chosen_season = st.selectbox(
        key="stats_one_team__season",
        label="Choose season...",
        options=get_all_seasons(db_conn)
    )

    all_teams_of_comp_of_season = get_teams_by_comp_by_season(db_conn, "all", [chosen_season])
    n_teams = len(all_teams_of_comp_of_season)