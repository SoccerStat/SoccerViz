import streamlit as st
from components.queries.execute_query import execute_query
from utils.file_helper.reader import read_sql_file

@st.cache_data(show_spinner=False)
def get_all_seasons(_db_conn):
    sql_file = read_sql_file("components/queries/commons/all_seasons.sql")
    result = execute_query(_db_conn, sql_file)
    return result['Schema'].to_list()

@st.cache_data(show_spinner=False)
def get_seasons_by_comp(_db_conn, name_comp):
    sql_file = read_sql_file("components/queries/basic_stats/by_comp/seasons.sql", name_comp=name_comp)
    result = execute_query(_db_conn, sql_file)
    return result['season'].to_list()