import streamlit as st

from components.queries.execute_query import execute_query

from utils.file_helper.reader import read_sql_file


@st.cache_data(show_spinner=False)
def get_all_clubs(_db_conn):
    sql_file = read_sql_file("components/queries/commons/get_all_clubs.sql")
    result = execute_query(_db_conn, sql_file)

    return result["Club"].to_list()


@st.cache_data(show_spinner=False)
def get_teams_by_comp_by_season(_db_conn, name_comp, seasons):
    sql_file = read_sql_file(
        "components/queries/commons/get_teams_by_comp_by_season.sql",
        name_comp=name_comp,
        seasons=seasons,
    )
    result = execute_query(_db_conn, sql_file)

    return result["Club"].to_list()
