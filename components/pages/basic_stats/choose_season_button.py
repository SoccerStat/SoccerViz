import streamlit as st

from components.commons.get_seasons import get_seasons_by_comp
from components.queries.execute_query import execute_query
from config import ALL_SEASONS_MODE, RANGE_SEASONS_MODE, COMPARE_SEASONS_MODE


@st.cache_data(show_spinner=False)
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
    if name_comp:
        all_seasons =  get_seasons_by_comp(db_conn, name_comp)

        st.session_state.setdefault("basic_stats_seasons_selected", all_seasons)

        with st.container():
            season_modes = [RANGE_SEASONS_MODE, COMPARE_SEASONS_MODE, ALL_SEASONS_MODE]

            st.session_state.setdefault("basic_stats_season_mode_selected", season_modes[0])

            st.radio(
                key="basic_stats_season_mode_selected",
                label="Selection mode",
                options=season_modes,
                horizontal=True,
                index=season_modes.index(st.session_state["basic_stats_season_mode_selected"]),
            )

            selected_mode = st.session_state.basic_stats_season_mode_selected

            if selected_mode == RANGE_SEASONS_MODE:
                cols = st.columns(2)
                with cols[0]:
                    min_season = st.selectbox(
                        label="Min season",
                        options=all_seasons
                    )
                    max_season = st.selectbox(
                        label="Max season",
                        options=[season for season in all_seasons if season >= min_season]
                    )
                    st.session_state.basic_stats_seasons_selected = [season for season in all_seasons if min_season <= season <= max_season]

            elif selected_mode == COMPARE_SEASONS_MODE:
                cols = st.columns(2)
                with cols[0]:
                    selected_seasons = st.multiselect(
                        label="select seasons...",
                        options=all_seasons,
                        max_selections=3
                    )
                    st.session_state.basic_stats_seasons_selected = selected_seasons

            elif selected_mode == ALL_SEASONS_MODE:
                st.session_state.basic_stats_seasons_selected = all_seasons

        return st.session_state.basic_stats_season_mode_selected, st.session_state.basic_stats_seasons_selected

    return None, None