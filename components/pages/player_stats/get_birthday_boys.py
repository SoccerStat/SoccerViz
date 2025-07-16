import streamlit as st

from components.queries.execute_query import execute_query
from utils.file_helper.reader import read_sql_file


def get_birthday_boys(db_conn):
    sql_file = read_sql_file(
        file_name=f"components/queries/player_stats/birthday_boys.sql"
    )
    return st.dataframe(execute_query(db_conn, sql_file), hide_index=True)