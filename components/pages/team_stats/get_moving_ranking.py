import streamlit as st
import pandas as pd
import altair as alt

from components.pages.team_stats.get_teams_by_comp_by_season import get_teams_by_comp_by_season
from utils.file_helper.reader import read_sql_file
from components.commons.get_all_seasons import get_seasons
from components.queries.execute_query import execute_query
from config import TEAM_RANKINGS, COMPETITIONS, C_CUPS_TEAMS_EXCLUDED_RANKINGS, KIND_C_CUP


def ranking_by_week(db_conn, chosen_ranking, chosen_comp, chosen_season, week):
    sql_file = read_sql_file(
        file_name="components/queries/team_stats/get_moving_ranking.sql",
        ranking=chosen_ranking,
        name_comp=chosen_comp,
        season=chosen_season,
        week=week,
    )
    return execute_query(db_conn, sql_file)

def get_moving_ranking(db_conn):
    comps_and_kind = {comp["label"]: comp["kind"] for comp in COMPETITIONS.values()}
    chosen_comp = st.selectbox(
        key="moving_ranking_comp",
        label="Choose competition...",
        options=comps_and_kind.keys())

    chosen_season = st.selectbox(
        key="moving_ranking_season",
        label="Choose season...",
        options=get_seasons(db_conn, chosen_comp)
    )

    teams = get_teams_by_comp_by_season(db_conn, chosen_comp, [chosen_season])
    nb_weeks = 2 * (len(teams) - 1)

    chosen_teams = st.multiselect(
        key="moving_ranking_teams",
        label="Choose teams...",
        options=["All"] + teams
    )

    if 'All' in chosen_teams:
        chosen_teams = teams

    if chosen_teams:
        complete_df = pd.DataFrame()

        with st.spinner("Data loading..."):
            for j in range(1, nb_weeks + 1):
                df_j = ranking_by_week(db_conn, "Points", chosen_comp, chosen_season, j)
                complete_df = pd.concat([complete_df, df_j], ignore_index=True)

            complete_df = complete_df.sort_values(by=["Club", "Week"])
            complete_df["Cumulated Points"] = complete_df.groupby("Club")["Points"].cumsum()
            complete_df = complete_df.sort_values(by=["Week", "Cumulated Points"], ascending=[True, False])
            complete_df["Ranking"] = complete_df.groupby("Week")["Cumulated Points"].rank(
                method="dense",  # ou 'min', 'first' selon ton besoin
                ascending=False
            ).astype(int)
            complete_df = complete_df[complete_df["Club"].isin(chosen_teams)]
            st.write(complete_df)

            line_chart = alt.Chart(complete_df).mark_line(point=True).encode(
                x=alt.X('Week:O', title='Week'),
                y=alt.Y('Cumulated Points:Q', title=f'Cumulated Points'),
                color='Club:N',
                tooltip=['Club', 'Week', "Points", "Cumulated Points", "Ranking"]
            ).properties(
                title=f"Évolution des points - {chosen_comp} ({chosen_season})"
            )

            st.altair_chart(line_chart, use_container_width=True)
            st.write("**Only the number of points are considered for ranking => regardless the Goals Diff.**")
