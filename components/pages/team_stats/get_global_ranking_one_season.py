import streamlit as st
import pandas as pd
import altair as alt

from components.pages.team_stats.get_teams_by_comp_by_season import get_teams_by_comp_by_season
from utils.file_helper.reader import read_sql_file
from components.commons.get_seasons import get_seasons_by_comp
from components.queries.execute_query import execute_query
from config import TEAM_RANKINGS, COMPETITIONS, C_CUPS_TEAMS_EXCLUDED_RANKINGS, KIND_C_CUP, KIND_CHP


@st.cache_data(show_spinner=False)
def ranking_by_chp_week(_db_conn, chosen_ranking, chosen_comp, chosen_season, nb_chp_weeks):
    complete_df = pd.DataFrame()
    
    for j in range(1, nb_chp_weeks + 1):
        sql_file = read_sql_file(
            file_name="components/queries/team_stats/get_global_ranking_one_season.sql",
            ranking=chosen_ranking,
            name_comp=chosen_comp,
            season=chosen_season,
            week=j,
        )
        df_j = execute_query(_db_conn, sql_file)
        complete_df = pd.concat([complete_df, df_j], ignore_index=True)

    return complete_df


@st.cache_data(show_spinner=False)
def ranking_by_c_cup_week(_db_conn, chosen_ranking, chosen_comp, chosen_season):
    complete_df = pd.DataFrame()

    return complete_df


def get_global_ranking_one_season(db_conn):
    comps_and_kind = {comp["label"]: comp["kind"] for comp in COMPETITIONS.values()}
    comps = list(comps_and_kind.keys())

    st.session_state.setdefault("team_stats_moving_ranking_chosen_comp", comps[0])
    st.session_state.team_stats_moving_ranking_chosen_comp = st.selectbox(
        key="comp_over_one_season",
        label="Choose competition...",
        options=comps,
        index=comps.index(st.session_state.team_stats_moving_ranking_chosen_comp)
    )
    chosen_comp = st.session_state.team_stats_moving_ranking_chosen_comp

    kind_of_comp = comps_and_kind[chosen_comp]

    seasons_by_comp = get_seasons_by_comp(db_conn, chosen_comp)

    st.session_state.setdefault("team_stats_moving_ranking_chosen_season", seasons_by_comp[0])

    if st.session_state.team_stats_moving_ranking_chosen_season not in seasons_by_comp:
        st.session_state.team_stats_moving_ranking_chosen_season = seasons_by_comp[0]

    st.session_state.team_stats_moving_ranking_chosen_season = st.selectbox(
        key="season_over_one_season",
        label="Choose season...",
        options=seasons_by_comp,
        index=seasons_by_comp.index(st.session_state.team_stats_moving_ranking_chosen_season)
    )
    chosen_season = st.session_state.team_stats_moving_ranking_chosen_season

    teams = get_teams_by_comp_by_season(db_conn, chosen_comp, [chosen_season])
    n_teams = len(teams)

    chosen_teams = st.multiselect(
        key="teams_over_one_season",
        label="Choose teams...",
        options=["All"] + teams,
    )

    if 'All' in chosen_teams:
        chosen_teams = teams

    if chosen_teams:
        with st.spinner("Data loading..."):

            if kind_of_comp == KIND_CHP:
                n_weeks = 2 * (n_teams - 1)
                complete_df = ranking_by_chp_week(
                    _db_conn=db_conn,
                    chosen_ranking="Points",
                    chosen_comp=chosen_comp,
                    chosen_season=chosen_season,
                    nb_chp_weeks=n_weeks
                )

            elif kind_of_comp == KIND_C_CUP:
                n_weeks = 100
                complete_df = ranking_by_c_cup_week(
                    _db_conn=db_conn,
                    chosen_ranking="Points",
                    chosen_comp=chosen_comp,
                    chosen_season=chosen_season
                )

            complete_df["Cumulated Points"] = complete_df.groupby("Club")["Points"].cumsum()
            complete_df = complete_df.sort_values(by=["Week", "Cumulated Points"], ascending=[True, False])

            complete_df["Ranking"] = complete_df.groupby("Week")["Cumulated Points"].rank(
                method="dense",
                ascending=False
            ).astype(int)
            complete_df = complete_df[complete_df["Club"].isin(chosen_teams)]

            line_chart = alt.Chart(complete_df).mark_line(point=True).encode(
                x=alt.X('Week:O', title='Week'),
                y=alt.Y('Cumulated Points:Q', title=f'Cumulated Points'),
                color=alt.Color('Club:N', legend=alt.Legend(title="Clubs", orient="right", labelLimit=2000)),
                tooltip=['Club', 'Week', "Points", "Cumulated Points", "Ranking"]
            ).properties(
                title=f"Evolution of points - {chosen_comp} ({chosen_season})",
                height=510 if n_teams == 20 else 460 if n_teams == 18 else 600
            )

            st.altair_chart(line_chart, use_container_width=True)
            st.write("**Only the number of points are considered for ranking => regardless the Goals Diff.**")

            # TODO: enable dataframe export for analyzes.
