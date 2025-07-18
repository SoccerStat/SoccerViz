import streamlit as st


@st.cache_data(show_spinner=False)
def get_all_teams(_db_conn):
    sql_file = read_sql_file("components/queries/commons/all_players.sql")
    result = execute_query(_db_conn, sql_file)
    return result['schema_name'].to_list()
