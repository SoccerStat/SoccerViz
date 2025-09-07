import streamlit as st

from components.pages.basic_stats.by_season_by_comp.get_stats import get_stats


def range_seasons(db_conn, name_comp, seasons_ids, chosen_ranking):
    titles = ["Matches", "Goals", "Cartons" if chosen_ranking == "Clubs" else "Assists", "Outcome"]
    cols = st.columns(4, gap="medium")

    # table_style = """
    #     <style>
    #     .basic_stats {
    #         border-collapse: collapse;
    #         width: 100%;
    #         font-size: 10px;
    #     }
    #     .basic_stats th, .basic_stats td {
    #         border: 1px solid #ddd;
    #         padding: 4px;
    #         text-align: center;
    #     }
    #     </style>
    # """

    for col, title in zip(cols, titles):
        with col:
            with st.container():
                st.markdown(
                    f"<h4 style='text-align: center; color: #1f77b4; margin-bottom: 1rem;'>{title}</h4>",
                    unsafe_allow_html=True
                )
                df = get_stats(
                    _db_conn=db_conn,
                    name_comp=name_comp,
                    seasons_ids=seasons_ids,
                    chosen_ranking=chosen_ranking,
                    ranking=title.lower()
                )

                st.dataframe(df, use_container_width=True)
