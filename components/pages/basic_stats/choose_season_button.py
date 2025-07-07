import streamlit as st

from components.commons.get_all_seasons import get_seasons
from components.queries.execute_query import execute_query
from config import ALL_SEASONS_MODE, RANGE_SEASONS_MODE, COMPARE_SEASONS_MODE


def select_all_seasons_by_comp(db_conn, all_seasons, id_comp):
    if id_comp != "all_comps":
        condition_comp = f"WHERE competition = '{id_comp}'"
    else:
        condition_comp = ""

    union_query = " UNION ALL ".join(
        [
            f"(SELECT '{schema[7:]}' as season FROM {schema}.match {condition_comp} LIMIT 1)"
            for schema in all_seasons
        ]
    )
    final_query = f"""
        SELECT DISTINCT season AS distinct_season
        FROM ({union_query}) AS all_counts 
        ORDER BY season;
    """
    result = execute_query(db_conn, final_query)
    return result['distinct_season'].tolist()

def choose_season_button(db_conn, name_comp):
    all_seasons =  get_seasons(db_conn, name_comp) # get_all_seasons(db_conn)
    # all_seasons_by_comp = select_all_seasons_by_comp(db_conn, all_seasons, id_comp)

    if "selected_seasons" not in st.session_state:
        st.session_state.selected_seasons = all_seasons

    with st.container():
        mode = st.radio("Selection mode", [RANGE_SEASONS_MODE, COMPARE_SEASONS_MODE, ALL_SEASONS_MODE], horizontal=True)


        if mode == ALL_SEASONS_MODE:
            st.session_state.selected_seasons = all_seasons

        if mode == RANGE_SEASONS_MODE:
            cols = st.columns(2)
            with cols[0]:
                min_season = st.selectbox(label="Min season", options=all_seasons)
                max_season = st.selectbox(label="Max season", options=[season for season in all_seasons if season >= min_season])
                st.session_state.selected_seasons = [season for season in all_seasons if min_season <= season <= max_season]

        if mode == COMPARE_SEASONS_MODE:
            cols = st.columns(2)
            with cols[0]:
                selected_seasons = st.multiselect(label="select seasons...", options=all_seasons, max_selections=3)
                st.session_state.selected_seasons = selected_seasons

    return mode, st.session_state.selected_seasons