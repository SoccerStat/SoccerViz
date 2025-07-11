import streamlit as st
import pandas as pd
import altair as alt

from components.queries.execute_query import execute_query
from utils.file_helper.reader import read_sql_file

@st.cache_data(show_spinner=False)
def get_data_by_item(_db_conn, chosen_season, column, item):
    sql_file = read_sql_file(
        file_name=f"components/queries/monitoring/tables/by_season.sql",
        in_season=f"season_{chosen_season}",
        date_column=column,
        in_tab=item
    )
    return execute_query(_db_conn, sql_file)

def get_by_season_tables(_db_conn, chosen_season, column):
    matches = "Matches"
    teams = "Teams"
    team_players = "Team Players"

    df_matches = get_data_by_item(_db_conn, chosen_season, column, matches.lower()[:-2])
    df_teams = get_data_by_item(_db_conn, chosen_season, column, teams.lower()[:-1])
    df_team_players = get_data_by_item(_db_conn, chosen_season, column, team_players.lower().replace(' ', '_')[:-1])

    st.markdown(
        f"""<h4><strong>{matches}</strong></h4>
        """,unsafe_allow_html = True
    )
    st.dataframe(df_matches)

    st.markdown(
        f"""<h4><strong>{teams}</strong></h4>
            """, unsafe_allow_html=True
    )
    st.dataframe(df_teams)

    st.markdown(
        f"""<h4><strong>{team_players}</strong></h4>
            """, unsafe_allow_html=True
    )
    st.dataframe(df_team_players)