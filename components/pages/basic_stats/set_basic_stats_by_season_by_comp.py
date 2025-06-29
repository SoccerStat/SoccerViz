import streamlit as st

from utils.file_helper.reader import read_sql_file
from components.queries.execute_query import execute_query

def get_stats(db_conn, name_comp, seasons_ids, chosen_ranking, ranking):
    kind = 'clubs' if chosen_ranking == 'Clubs' else 'Players'
    sql_file = read_sql_file(
        file_name=f"components/queries/basic_stats/by_season_by_comp/{kind}/{ranking}.sql",
        name_comp=name_comp,
        seasons_ids=[f"'{s}'" for s in seasons_ids]
    )
    return execute_query(db_conn, sql_file)

def set_basic_stats_by_season_by_comp(db_conn, name_comp, seasons_ids):

    chosen_comp, chosen_seasons, players_or_clubs = st.columns([1, 2, 1])

    with chosen_comp:
        st.write(name_comp)

    with chosen_seasons:
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

    titles = ["Matches", "Goals", "Cartons", "Outcome"]
    cols = st.columns(4, gap="medium")

    st.markdown("""
        <style>
        .row_heading.level0, .blank {
            width: 20px !important;
            max-width: 20px !important;
        }
        .dataframe td, .dataframe th {
            font-size: 0.80rem;
            padding: 4px 8px;
        }
        </style>
    """, unsafe_allow_html=True)

    for col, title in zip(cols, titles):
        with col:
            with st.container():
                st.markdown(
                    f"<h4 style='text-align: center; color: #1f77b4; margin-bottom: 1rem;'>{title}</h4>",
                    unsafe_allow_html=True
                )
                df = get_stats(db_conn=db_conn, name_comp=name_comp, seasons_ids=seasons_ids, chosen_ranking=chosen_ranking, ranking=title.lower())
                st.dataframe(df, use_container_width=True)
