import streamlit as st
import pandas as pd
import altair as alt

from components.queries.execute_query import execute_query
from utils.file_helper.reader import read_sql_file

@st.cache_data(show_spinner=False)
def get_counts_by_item(_db_conn, column, item, frequency):
    sql_file = read_sql_file(
        file_name=f"components/queries/monitoring/tables/upper.sql",
        date_column=column,
        in_tab=item,
        frequency=frequency.split(' ')[-1]
    )
    return execute_query(_db_conn, sql_file)

def get_upper_tables(_db_conn, column):
    clubs = "Clubs"
    players = "Players"

    frequency = st.radio(
        key=f"upper_table__radio__{column}",
        label="Frequency",
        options=["Last 48 hours", "Last 7 days", "Last 4 weeks", "Last 3 months"],
        horizontal=True
    )

    df_clubs = get_counts_by_item(_db_conn, column, clubs.lower()[:-1], frequency)
    df_players = get_counts_by_item(_db_conn, column, players.lower()[:-1], frequency)

    st.write(clubs)
    st.dataframe(df_clubs)

    st.write(players)
    st.dataframe(df_players)