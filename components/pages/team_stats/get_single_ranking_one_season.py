import streamlit as st
from utils.file_helper.reader import read_sql_file
from components.commons.get_seasons import get_seasons_by_comp
from components.queries.execute_query import execute_query
from config import TEAM_RANKINGS, COMPETITIONS, C_CUPS_TEAMS_EXCLUDED_RANKINGS, KIND_C_CUP


@st.cache_data(show_spinner=False)
def get_one_ranking(_db_conn, chosen_comp, chosen_season, chosen_ranking):
    sql_file = read_sql_file(
        file_name="components/queries/team_stats/get_ranking_one_season.sql",
        name_comp=chosen_comp,
        season=chosen_season,
        ranking=chosen_ranking
    )

    return execute_query(_db_conn, sql_file)

def get_single_ranking_one_season(db_conn):
    comps_and_kind = {comp["label"]: comp["kind"] for comp in COMPETITIONS.values()}
    comps = list(comps_and_kind.keys())

    chosen_comp = st.selectbox(
        key="single_ranking_one_season__comp",
        label="Choose competition...",
        options=comps
    )

    seasons_by_comp = get_seasons_by_comp(db_conn, chosen_comp)

    chosen_season = st.selectbox(
        key="single_ranking_one_season__season",
        label="Choose season...",
        options=seasons_by_comp
    )

    if comps_and_kind[chosen_comp] == KIND_C_CUP:
        rankings = [ranking for ranking in TEAM_RANKINGS if ranking not in C_CUPS_TEAMS_EXCLUDED_RANKINGS]
    else:
        rankings = TEAM_RANKINGS

    chosen_ranking = st.selectbox(
        key="single_ranking_one_season__ranking",
        label="Choose ranking...",
        options=[""] + rankings,
        index=0
    )

    if chosen_ranking != "":
        df = get_one_ranking(db_conn, chosen_comp, chosen_season, chosen_ranking)
        st.dataframe(df.set_index("Ranking"))

        csv = df.to_csv(index=False, sep='|')
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name=f"{chosen_comp.replace(' ', '_').lower()}_{chosen_season}_{chosen_ranking.replace(' ', '_').lower()}_simple_ranking.csv",
            mime="text/csv"
        )