import streamlit as st
import pandas as pd
import altair as alt

from components.commons.get_all_teams import get_teams_by_comp_by_season
from components.commons.get_seasons import get_seasons_by_comp
from components.queries.execute_query import execute_query

from utils.file_helper.reader import read_sql_file
from config import TEAM_RANKINGS, COMPETITIONS, C_CUPS_TEAMS_EXCLUDED_RANKINGS, KIND_C_CUP, KIND_CHP


@st.cache_data(show_spinner=False)
def ranking_by_chp_week(_db_conn, chosen_ranking, chosen_comp, chosen_season, nb_chp_weeks):
    complete_df = pd.DataFrame()
    
    for j in range(1, nb_chp_weeks + 1):
        sql_file = read_sql_file(
            file_name="components/queries/team_stats/get_cumulative_ranking_one_season.sql",
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

    chosen_comp = st.selectbox(
        key="global_ranking_one_season__comp",
        label="Choose competition...",
        options=comps
    )

    kind_of_comp = comps_and_kind[chosen_comp]

    seasons_by_comp = get_seasons_by_comp(db_conn, chosen_comp)

    chosen_season = st.selectbox(
        key="global_ranking_one_season__season",
        label="Choose season...",
        options=[""] + seasons_by_comp
    )

    if chosen_season:

        teams = get_teams_by_comp_by_season(db_conn, chosen_comp, [chosen_season])
        n_teams = len(teams)

        st.multiselect(
            key="global_ranking_one_season__teams",
            label="Choose teams...",
            options=["All"] + teams
        )

        chosen_teams = st.session_state.global_ranking_one_season__teams

        if 'All' in chosen_teams:
            chosen_teams = teams

        if chosen_teams:
            with st.spinner("Data loading..."):
                if kind_of_comp == KIND_CHP:
                    n_weeks = 2 * (n_teams - 1)
                    df = ranking_by_chp_week(
                        _db_conn=db_conn,
                        chosen_ranking="Points",
                        chosen_comp=chosen_comp,
                        chosen_season=chosen_season,
                        nb_chp_weeks=n_weeks
                    )

                elif kind_of_comp == KIND_C_CUP:
                    # n_weeks = 100
                    df = ranking_by_c_cup_week(
                        _db_conn=db_conn,
                        chosen_ranking="Points",
                        chosen_comp=chosen_comp,
                        chosen_season=chosen_season
                    )

                set_plots(df, n_teams, chosen_comp, chosen_season, chosen_teams)

                csv = df.to_csv(index=False, sep='|')
                st.download_button(
                    label="📥 Download CSV",
                    data=csv,
                    file_name=f"{chosen_comp.replace(' ', '_').lower()}_{chosen_season}_global_ranking_one_season.csv",
                    mime="text/csv"
                )


def set_plots(df, n_teams, chosen_comp, chosen_season, chosen_teams):
    df = df.sort_values(by=["Week", "Points"], ascending=[True, False])

    filtered_df = df[df["Club"].isin(chosen_teams)]

    base = alt.Chart(filtered_df).mark_line(point=True).encode(
        x=alt.X('Week:O', title='Week'),
        color=alt.Color('Club:N', legend=alt.Legend(title="Clubs", orient="right", labelLimit=2000))
    )

    points_chart = base.encode(
        y=alt.Y('Points:Q', title=f'Points'),
        tooltip=['Club', 'Week', "Points", "Ranking"]
    ).properties(
        title=f"Evolution of points - {chosen_comp} ({chosen_season})",
        height=510 if n_teams == 20 else 460 if n_teams == 18 else 600
    )

    weeks = sorted(filtered_df['Week'].unique())
    ref_df = pd.DataFrame({
        'Week': weeks,
        'y': [3 * int(w) for w in weeks],
        'label': 'Max Possible'
    })

    max_points_line = alt.Chart(ref_df).mark_line(
        color="gray",
        strokeDash=[6, 4],
    ).encode(
        x=alt.X('Week:O'),
        y=alt.Y('y:Q')
    )

    cumulative_chart = alt.layer(points_chart, max_points_line)

    actual_per_match_chart = base.encode(
        y=alt.Y('Points/Match:Q'),
        strokeDash=alt.value([1, 0]),
        tooltip=['Club', 'Week', "Points/Match", "Ranking"]
    )

    # expected_per_match_chart = base.encode(
    #     y=alt.Y('xPoints/Match:Q'),
    #     strokeDash=alt.value([4, 4]),
    #     tooltip=['Club', 'Week', "xPoints/Match", "Ranking"]
    # )

    # per_match_chart = alt.layer(actual_per_match_chart, expected_per_match_chart).encode(
    # y=alt.Y(shorthand='Points/Match:Q', axis=alt.Axis(title="Actual and Expected Points per Match"))
    # ).properties(
    #     title=f"Actual and Expected evolution of points per match - {chosen_comp} ({chosen_season})",
    #     height=510 if n_teams == 20 else 460 if n_teams == 18 else 600
    # )

    # TODO: implémenter expected points

    st.altair_chart(cumulative_chart, use_container_width=True)
    st.altair_chart(actual_per_match_chart, use_container_width=True)
