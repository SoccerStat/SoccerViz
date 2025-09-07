import streamlit as st

from components.pages.basic_stats.by_season_by_comp.compare_seasons import compare_seasons
from components.pages.basic_stats.by_season_by_comp.range_seasons import range_seasons

from config import COMPARE_SEASONS_MODE


def set_basic_stats_by_season_by_comp(db_conn, name_comp, season_mode, seasons_ids):
    chosen_comp, chosen_seasons, _, players_or_clubs = st.columns([1, 1, 1, 1])

    with chosen_comp:
        st.markdown(
            f"""
                <div style="display: flex; justify-content: center; align-items: center; height: 80px;">
                    <h3 style="margin: 0; font-weight: normal;"><strong>{name_comp}</strong></h3>
                </div>
                """,
            unsafe_allow_html=True
        )

    with chosen_seasons:
        if season_mode == COMPARE_SEASONS_MODE:
            seasons = ', '.join([f"Season {season.replace('_', '-')}" for season in seasons_ids])
        else:
            if min(seasons_ids) != max(seasons_ids):
                seasons = f"From {min(seasons_ids).replace('_', '-')} to {max(seasons_ids).replace('_', '-')}"
            else:
                seasons = f"Season {seasons_ids[0].replace('_', '-')}"

        st.markdown(
            f"""
                <div style="display: flex; justify-content: center; align-items: center; height: 80px;">
                    <h3 style="margin: 0; font-weight: normal;"><strong>{seasons}</strong></h3>
                </div>
                """,
            unsafe_allow_html=True
        )

    with players_or_clubs:
        st.markdown(
            """
            <div style="display: flex; justify-content: center; align-items: flex-end;">
            """,
            unsafe_allow_html=True
        )
        chosen_ranking = st.radio(
            label="Kind of ranking",
            options=["Clubs", "Players"],
            horizontal=True,
            label_visibility="collapsed"
        )
        st.markdown(
            """
            </div>
            """,
            unsafe_allow_html=True
        )

    if season_mode == COMPARE_SEASONS_MODE:
        compare_seasons(db_conn, name_comp, seasons_ids, chosen_ranking)
    else:
        range_seasons(db_conn, name_comp, seasons_ids, chosen_ranking)
