import streamlit as st

from components.pages.basic_stats.by_season_by_comp.utils import get_stats


def compare_seasons(db_conn, name_comp, seasons_ids, chosen_ranking):
    titles = ["Matches", "Goals", "Cartons" if chosen_ranking == "Clubs" else "Assists", "Outcome"]
    cols = st.columns(len(seasons_ids), gap="medium")

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

    for i, season in enumerate(seasons_ids):
        with cols[i]:
            st.markdown(
                f"<h4 style='text-align: center; color: #1f77b4; margin-bottom: 1rem;'>{season.replace('_','-')}</h4>",
                unsafe_allow_html=True
            )
            for title in titles:
                st.markdown(
                    f"<h4 style='text-align: center; color: #1f77b4; margin-bottom: 1rem;'>{title}</h4>",
                    unsafe_allow_html=True
                )
                df = get_stats(_db_conn=db_conn, name_comp=name_comp, seasons_ids=[season], chosen_ranking=chosen_ranking, ranking=title.lower())
                st.dataframe(df, use_container_width=True)