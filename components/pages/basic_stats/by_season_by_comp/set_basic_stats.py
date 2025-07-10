import streamlit as st

from components.queries.execute_query import execute_query
from components.pages.basic_stats.by_season_by_comp.compare_seasons import compare_seasons
from components.pages.basic_stats.by_season_by_comp.range_seasons import range_seasons

from config import COMPARE_SEASONS_MODE
from utils.file_helper.reader import read_sql_file

# @st.cache_data(show_spinner=False)
# def get_stats(db_conn, name_comp, seasons_ids, chosen_ranking, ranking):
#     kind = 'clubs' if chosen_ranking == 'Clubs' else 'Players'
#     sql_file = read_sql_file(
#         file_name=f"components/queries/basic_stats/by_season_by_comp/{kind}/{ranking}.sql",
#         name_comp=name_comp,
#         seasons_ids=[f"'{s}'" for s in seasons_ids]
#     )
#     return execute_query(db_conn, sql_file)


def set_basic_stats_by_season_by_comp(db_conn, name_comp, season_mode, seasons_ids):
    chosen_comp, chosen_seasons, players_or_clubs = st.columns([1, 2, 1])

    with chosen_comp:
        st.write(name_comp)

    with chosen_seasons:
        if season_mode == COMPARE_SEASONS_MODE:
            st.write(', '.join([f"Season {season}" for season in seasons_ids]))
        else:
            if min(seasons_ids) != max(seasons_ids):
                seasons = f"From {min(seasons_ids).replace('_', '-')} to {max(seasons_ids).replace('_', '-')}"
            else:
                seasons = f"Season {seasons_ids[0].replace('_', '-')}"
            st.write(seasons)

    with players_or_clubs:
        chosen_ranking = st.radio(
            "Kind of ranking",
            options=["Clubs", "Players"],
            horizontal=True,
            label_visibility="collapsed"
        )

    if season_mode == COMPARE_SEASONS_MODE:
        compare_seasons(db_conn, name_comp, seasons_ids, chosen_ranking)
    else:
        range_seasons(db_conn, name_comp, seasons_ids, chosen_ranking)