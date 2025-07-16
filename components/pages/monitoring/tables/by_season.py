import streamlit as st
import pandas as pd
import altair as alt

from components.commons.set_titles import set_sub_sub_sub_title
from components.queries.execute_query import execute_query
from utils.file_helper.reader import read_sql_file

@st.cache_data(show_spinner=False)
def get_data_by_item(_db_conn, chosen_season, column, item, frequency):
    sql_file = read_sql_file(
        file_name=f"components/queries/monitoring/tables/by_season.sql",
        in_season=f"season_{chosen_season}",
        date_column=column,
        in_tab=item,
        frequency=frequency.split(' ')[-1]
    )
    return execute_query(_db_conn, sql_file)

def get_by_season_tables(_db_conn, chosen_season, column):
    matches = "Matches"
    teams = "Teams"
    team_players = "Team Players"

    frequency = st.radio(
        key=f"by_season_table__radio__{column}",
        label="Frequency",
        options=["Last 48 hours", "Last 7 days", "Last 4 weeks", "Last 3 months"],
        horizontal=True
    )

    df_matches = get_data_by_item(_db_conn, chosen_season, column, matches.lower()[:-2], frequency)
    df_teams = get_data_by_item(_db_conn, chosen_season, column, teams.lower()[:-1], frequency)
    df_team_players = get_data_by_item(_db_conn, chosen_season, column, team_players.lower().replace(' ', '_')[:-1], frequency)


    set_sub_sub_sub_title(matches)
    st.dataframe(df_matches)

    set_sub_sub_sub_title(teams)
    st.dataframe(df_teams)

    set_sub_sub_sub_title(team_players)
    st.dataframe(df_team_players)