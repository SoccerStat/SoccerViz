import streamlit as st

from components.queries.execute_query import execute_query

from utils.file_helper.reader import read_sql_file


@st.cache_data(show_spinner=False)
def get_all_players(_db_conn):
    sql_file = read_sql_file("components/queries/commons/get_all_recent_players.sql")
    result = execute_query(_db_conn, sql_file)

    return result["Player"].to_list()
