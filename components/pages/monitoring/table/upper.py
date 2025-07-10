import streamlit as st
import pandas as pd
import altair as alt

from components.queries.execute_query import execute_query
from utils.file_helper.reader import read_sql_file

@st.cache_data(show_spinner=False)
def get_counts_by_item(db_conn, column, item):
    sql_file = read_sql_file(
        file_name=f"components/queries/monitoring/tables/upper.sql",
        date_column=column,
        in_tab=item
    )
    return execute_query(db_conn, sql_file)

def get_upper_tables(db_conn, column):
    clubs = "Clubs"
    players = "Players"

    df_clubs = get_counts_by_item(db_conn, column, clubs.lower()[:-1])
    df_players = get_counts_by_item(db_conn, column, players.lower()[:-1])

    st.write(clubs)
    st.dataframe(df_clubs)

    st.write(players)
    st.dataframe(df_players)