import streamlit as st
from utils.file_helper.reader import read_sql_file
from components.queries.execute_query import execute_query

@st.cache_data(show_spinner=False)
def get_stats(_db_conn, name_comp, seasons_ids, chosen_ranking, ranking):
    kind = 'clubs' if chosen_ranking == 'Clubs' else 'Players'
    sql_file = read_sql_file(
        file_name=f"components/queries/basic_stats/by_season_by_comp/{kind}/{ranking}.sql",
        name_comp=name_comp,
        seasons_ids=[f"'{s}'" for s in seasons_ids]
    )
    return execute_query(_db_conn, sql_file)