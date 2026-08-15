import streamlit as st

from components.commons.seasons import get_seasons_by_comp
from config import ALL_SEASONS_MODE, RANGE_SEASONS_MODE, COMPARE_SEASONS_MODE


def choose_season(db_conn, name_comp):
    if name_comp:
        all_seasons_of_comp = get_seasons_by_comp(db_conn, name_comp)

        st.session_state.setdefault("basic_stats__seasons_selected", all_seasons_of_comp)

        with st.container():
            season_modes = [RANGE_SEASONS_MODE, COMPARE_SEASONS_MODE, ALL_SEASONS_MODE]

            st.session_state.setdefault("basic_stats__season_mode_selected", season_modes[0])

            st.radio(
                key="basic_stats__season_mode_selected",
                label="Selection mode",
                options=season_modes,
                horizontal=True,
                index=season_modes.index(st.session_state["basic_stats__season_mode_selected"]),
            )

            selected_mode = st.session_state.basic_stats__season_mode_selected

            if selected_mode == RANGE_SEASONS_MODE:
                cols = st.columns(2)
                with cols[0]:
                    min_season = st.selectbox(
                        label="Min season",
                        options=all_seasons_of_comp
                    )
                    max_season = st.selectbox(
                        label="Max season",
                        options=[season for season in all_seasons_of_comp if season >= min_season]
                    )
                    st.session_state.basic_stats__seasons_selected = \
                        [season for season in all_seasons_of_comp if min_season <= season <= max_season]

            elif selected_mode == COMPARE_SEASONS_MODE:
                cols = st.columns(2)
                with cols[0]:
                    chosen_seasons = st.multiselect(
                        key="basic_stats__chosen_seasons",
                        label="select seasons...",
                        options=all_seasons_of_comp,
                        max_selections=3
                    )
                    st.session_state.basic_stats__seasons_selected = chosen_seasons

            elif selected_mode == ALL_SEASONS_MODE:
                st.session_state.basic_stats__seasons_selected = all_seasons_of_comp

        return st.session_state.basic_stats__season_mode_selected, st.session_state.basic_stats__seasons_selected

    return None, None
