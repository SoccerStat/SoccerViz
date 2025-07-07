import streamlit as st
from utils.file_helper.reader import read_sql_file
from components.commons.get_all_seasons import get_seasons
from components.queries.execute_query import execute_query
from config import TEAM_RANKINGS, COMPETITIONS

def get_one_ranking(db_conn):
    chosen_comp = st.selectbox(label="Choose competition...",
                               options=[comp["label"] for comp in COMPETITIONS.values()])
    chosen_season = st.selectbox("Choose season...", options=get_seasons(db_conn, chosen_comp))
    chosen_ranking = st.selectbox("Choose ranking...", options=TEAM_RANKINGS)

    sql_file = read_sql_file(
        file_name="components/queries/team_stats/get_one_ranking.sql",
        name_comp=chosen_comp,
        season=chosen_season,
        ranking=chosen_ranking,
    )

    df = execute_query(db_conn, sql_file)
    st.dataframe(df)