import streamlit as st

from components.commons.get_seasons import get_seasons_by_comp
from config import TEAM_RANKINGS, COMPETITIONS, C_CUPS_TEAMS_EXCLUDED_RANKINGS, KIND_C_CUP, KIND_CHP


def get_team_performance_against_top_and_bottom(db_conn):
    comps_and_kind = {comp["label"]: comp["kind"] for comp in COMPETITIONS.values()}
    comps = list(comps_and_kind.keys())

    chosen_comp = st.selectbox(
        key="global_ranking_by_season__comp",
        label="Choose competition...",
        options=comps
    )

    seasons_by_comp = get_seasons_by_comp(db_conn, chosen_comp)

    chosen_seasons = st.multiselect(
        key="global_ranking_by_season__seasons",
        label="Choose season...",
        options=seasons_by_comp
    )

    # Dataframe : Club | Against Top 5

    # Dataframe : Club | Against Bottom 5
