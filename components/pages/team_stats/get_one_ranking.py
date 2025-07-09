import streamlit as st
from utils.file_helper.reader import read_sql_file
from components.commons.get_all_seasons import get_seasons
from components.queries.execute_query import execute_query
from config import TEAM_RANKINGS, COMPETITIONS, C_CUPS_TEAMS_EXCLUDED_RANKINGS, KIND_C_CUP


def get_one_ranking(db_conn):
    comps_and_kind = {comp["label"]: comp["kind"] for comp in COMPETITIONS.values()}
    chosen_comp = st.selectbox(label="Choose competition...",
                               options=comps_and_kind.keys())
    chosen_season = st.selectbox("Choose season...", options=get_seasons(db_conn, chosen_comp))

    if comps_and_kind[chosen_comp] == KIND_C_CUP:
        rankings = [ranking for ranking in TEAM_RANKINGS if ranking not in C_CUPS_TEAMS_EXCLUDED_RANKINGS]
    else:
        rankings = TEAM_RANKINGS

    chosen_ranking = st.selectbox("Choose ranking...", options=rankings)

    sql_file = read_sql_file(
        file_name="components/queries/team_stats/get_one_ranking.sql",
        name_comp=chosen_comp,
        season=chosen_season,
        ranking=chosen_ranking,
    )

    df = execute_query(db_conn, sql_file)
    st.dataframe(df.set_index("Ranking"))