import streamlit as st
import pandas as pd
import altair as alt

from components.pages.team_stats.get_teams_by_comp_by_season import get_teams_by_comp_by_season
from utils.file_helper.reader import read_sql_file
from components.commons.get_seasons import get_seasons_by_comp
from components.queries.execute_query import execute_query
from config import TEAM_RANKINGS, COMPETITIONS, C_CUPS_TEAMS_EXCLUDED_RANKINGS, KIND_C_CUP, KIND_CHP


@st.cache_data(show_spinner=False)
def ranking_by_chp_by_week_of_season(_db_conn, chosen_ranking, chosen_comp, season):
    df_season = pd.DataFrame()

    teams = get_teams_by_comp_by_season(_db_conn, chosen_comp, [season])
    nb_weeks = 2 * (len(teams) - 1)
    for week in range(1, nb_weeks + 1):
        sql_file = read_sql_file(
            file_name="components/queries/team_stats/get_global_ranking_by_season.sql",
            ranking=chosen_ranking,
            name_comp=chosen_comp,
            season=season,
            week=week
        )
        df_week = execute_query(_db_conn, sql_file)
        df_season = pd.concat([df_season, df_week], ignore_index=True)

    return df_season

@st.cache_data(show_spinner=False)
def ranking_by_chp_by_week_by_season(_db_conn, chosen_ranking, chosen_comp, chosen_seasons):
    complete_df = pd.DataFrame()

    for season in chosen_seasons:
        df_season = ranking_by_chp_by_week_of_season(_db_conn, chosen_ranking, chosen_comp, season)

        complete_df = pd.concat([complete_df, df_season], ignore_index=True)

    return complete_df


def get_global_ranking_by_season(db_conn):
    comps_and_kind = {comp["label"]: comp["kind"] for comp in COMPETITIONS.values()}
    comps = list(comps_and_kind.keys())

    st.session_state.setdefault("team_stats_global_ranking_chosen_comp", comps[0])
    st.session_state.team_stats_global_ranking_chosen_comp = st.selectbox(
        key="comp_by_season",
        label="Choose competition...",
        options=comps,
        index=comps.index(st.session_state.team_stats_global_ranking_chosen_comp)
    )
    chosen_comp = st.session_state.team_stats_global_ranking_chosen_comp
    kind_of_comp = comps_and_kind[chosen_comp]

    seasons_by_comp = get_seasons_by_comp(db_conn, chosen_comp)

    st.session_state.setdefault("team_stats_global_ranking_chosen_season", seasons_by_comp[0])

    if st.session_state.team_stats_global_ranking_chosen_season not in seasons_by_comp:
        st.session_state.team_stats_global_ranking_chosen_season = seasons_by_comp[0]

    st.session_state.team_stats_global_ranking_chosen_season = st.multiselect(
        key="season_by_season",
        label="Choose season...",
        options=seasons_by_comp
    )
    chosen_seasons = st.session_state.team_stats_global_ranking_chosen_season

    if chosen_seasons:

        n_seasons = len(seasons_by_comp)

        teams = get_teams_by_comp_by_season(db_conn, chosen_comp, chosen_seasons)
        n_teams = len(teams)

        chosen_teams = st.multiselect(
            key="teams_by_season",
            label="Choose teams...",
            options=teams
        )

        if chosen_teams:
            with st.spinner("Data loading..."):

                df = ranking_by_chp_by_week_by_season(
                    _db_conn=db_conn,
                    chosen_ranking="Points",
                    chosen_comp=chosen_comp,
                    chosen_seasons=chosen_seasons,
                )

                filtered_df = df[df["Club"].isin(chosen_teams)]
                filtered_df["Season_Club"] = filtered_df["Season"] + '-' + filtered_df["Club"]

                line_chart = alt.Chart(filtered_df).mark_line(point=True, interpolate="linear").encode(
                    x=alt.X('Week:O', title='Weeks'),
                    y=alt.Y('Points:Q', title=f'Points'),
                    color=alt.Color('Season_Club:N', legend=alt.Legend(title="Season - Club", orient="right", labelLimit=2000)),
                    tooltip=['Club', 'Season', "Points", "Ranking"]
                ).properties(
                    title=f"Number of points over weeks by season - {chosen_comp}",
                    height=510 if n_teams == 20 else 460 if n_teams == 18 else 600
                )

                line_text = line_chart.mark_text(
                    align='center',
                    baseline='bottom',
                    fontSize=12,
                    dy=-2,
                    color='black'
                ).encode(
                    text=alt.Text('Ranking:Q')
                )

                chart = alt.layer(
                    line_chart,
                    line_text
                )

                st.altair_chart(chart, use_container_width=True)

                csv = df.to_csv(index=False, sep='|')
                st.download_button(
                    label="📥 Download CSV",
                    data=csv,
                    file_name=f"{chosen_comp.replace(' ', '_').lower()}_global_ranking_by_season.csv",
                    mime="text/csv"
                )

                # TODO: enable dataframe export for analyzes.
