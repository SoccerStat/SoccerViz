import streamlit as st

from components.queries.execute_query import execute_query

from utils.file_helper.reader import read_sql_file


@st.cache_data(show_spinner=False)
def get_distinct_slots(_db_conn, chosen_comp, chosen_seasons):
    sql_file = read_sql_file(
        file_name="components/queries/commons/slots_by_comp_by_season.sql",
        name_comp=chosen_comp,
        seasons=chosen_seasons
    )
    result = execute_query(_db_conn, sql_file)

    return result["Slot"].to_list()
