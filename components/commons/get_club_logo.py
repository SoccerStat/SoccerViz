import streamlit as st

from components.queries.execute_query import execute_query

from utils.file_helper.reader import read_sql_file


@st.cache_data(show_spinner=False)
def get_club_logo(_db_conn, club_name):
    sql_file = read_sql_file(
        file_name="components/queries/commons/get_club_logo.sql",
        club_name=club_name,
    )
    return execute_query(_db_conn, sql_file).iloc[0]
