import streamlit as st

from components.commons.get_seasons import get_all_season_schemas
from components.commons.set_titles import set_sub_sub_sub_title

from components.queries.execute_query import execute_query

from utils.file_helper.reader import read_sql_file


@st.cache_data(show_spinner=False)
def get_winners_by_competition(_db_conn, chosen_season):
    sql_file = read_sql_file(
        file_name="components/queries/team_stats/given_competition/history/get_winners.sql",
        season=chosen_season
    )

    return execute_query(_db_conn, sql_file)


def get_winners(db_conn):
    all_seasons = [season[7:] for season in get_all_season_schemas(db_conn)]

    chosen_season = st.selectbox(
        key="winners__season",
        label="Choose season...",
        options=[""] + all_seasons[:-1]
    )

    if chosen_season:
        set_sub_sub_sub_title(f"Winners of the season {chosen_season.replace('_', '-')}")

        df_winners = get_winners_by_competition(db_conn, chosen_season).groupby("Competition")

        col_width = '150px'

        for competition, winner_stats in df_winners:
            st.write(f"**{competition}**")
            df_winner = (
                winner_stats
                .drop("Competition", axis=1)
                .style.set_table_styles([
                    {'selector': 'th', 'props': [('min-width', col_width), ('text-align', 'center')]},
                    {'selector': 'td', 'props': [('min-width', col_width), ('text-align', 'center')]}
                ])
                .hide(axis="index")
            )

            st.dataframe(df_winner, hide_index=True, use_container_width=True)
