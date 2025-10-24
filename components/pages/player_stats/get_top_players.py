import streamlit as st

from components.commons.set_titles import set_sub_sub_title
from components.queries.execute_query import execute_query

from utils.file_helper.reader import read_sql_file


@st.cache_data(show_spinner=False)
def get_top_scorers(_db_conn):
    sql_file = read_sql_file(
        "components/queries/player_stats/top_players/???.sql",
    )

    return execute_query(_db_conn, sql_file)


def get_top_players(db_conn):
    goals, assists = st.columns(2)

    with goals:
        set_sub_sub_title("Goals")

    with assists:
        set_sub_sub_title("Assists")
