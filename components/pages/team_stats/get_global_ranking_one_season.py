import streamlit as st
import pandas as pd
import altair as alt

from components.commons.get_all_teams import get_teams_by_comp_by_season
from components.commons.get_seasons import get_seasons_by_comp
from components.queries.execute_query import execute_query

from components.pages.team_stats.expected_performance.get_expected_performance_ranking import build_expected_performance_ranking, merge_rankings

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
def expected_ranking_by_chp_week(_db_conn, chosen_comp, chosen_season, nb_chp_weeks):
    complete_df = pd.DataFrame()

    for week in range(5, nb_chp_weeks+5, 5):
        if week > nb_chp_weeks:
            week = nb_chp_weeks
        st.write(f"Range 1-{week}")
        sql_file = read_sql_file(
            file_name="components/queries/team_stats/get_cumulative_expected_ranking_one_season.sql",
            name_comp=chosen_comp,
            season=chosen_season,
            week=week,
        )
        df_week = execute_query(_db_conn, sql_file)
        complete_df = pd.concat([complete_df, build_expected_performance_ranking(df_week)], ignore_index=True)

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

        get_expected_points = st.checkbox(
            key="global_ranking_one_season__xp",
            label="Calculate Expected Points ?",
            value=False
        )

        teams = get_teams_by_comp_by_season(db_conn, chosen_comp, [chosen_season])
        n_teams = len(teams)

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

                if get_expected_points:
                    df_expected = expected_ranking_by_chp_week(
                        _db_conn=db_conn,
                        chosen_comp=chosen_comp,
                        chosen_season=chosen_season,
                        nb_chp_weeks=n_weeks
                    )

                    final_df = merge_rankings(df, df_expected)
                else:
                    final_df = df

            elif kind_of_comp == KIND_C_CUP:
                # n_weeks = 100
                df = ranking_by_c_cup_week(
                    _db_conn=db_conn,
                    chosen_ranking="Points",
                    chosen_comp=chosen_comp,
                    chosen_season=chosen_season
                )

                final_df = df

        st.dataframe(final_df)
        st.multiselect(
            key="global_ranking_one_season__teams",
            label="Choose teams...",
            options=["All"] + teams
        )

        chosen_teams = st.session_state.global_ranking_one_season__teams

        if 'All' in chosen_teams:
            chosen_teams = teams

        if chosen_teams:
            set_plots(final_df, n_teams, chosen_comp, chosen_season, chosen_teams, get_expected_points)


            csv = df.to_csv(index=False, sep='|')
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"{chosen_comp.replace(' ', '_').lower()}_{chosen_season}_global_ranking_one_season.csv",
                mime="text/csv"
            )


def set_plots(df, n_teams, chosen_comp, chosen_season, chosen_teams, get_expected_points):
    df = df.sort_values(by=["Week", "Points"], ascending=[True, False])

    filtered_df = df[df["Club"].isin(chosen_teams)]

    set_plot_cumulative_points(filtered_df, chosen_comp, chosen_season, n_teams)
    set_plot_cumulative_points_per_match(filtered_df, chosen_comp, chosen_season, get_expected_points, n_teams)


def set_plot_cumulative_points(df, chosen_comp, chosen_season, n_teams):
    df_copy = df.copy()
    df_copy = df_copy[["Ranking", "Club", "Week", "Points"]].drop_duplicates()

    base_chart = alt.Chart(df_copy).mark_line(point=True).encode(
        x=alt.X('Week:O', title='Week'),
        color=alt.Color('Club:N', legend=alt.Legend(title="Clubs", orient="right", labelLimit=2000))
    ).properties(
        height=510 if n_teams == 20 else 460 if n_teams == 18 else 600
    )

    points_chart = base_chart.encode(
        y=alt.Y('Points:Q', title=f'Points'),
        tooltip=['Club', 'Week', "Points", "Ranking"]
    )

    weeks = sorted(df_copy['Week'].unique())
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

    cumulative_chart = alt.layer(points_chart, max_points_line).properties(
        title=f"Evolution of points - {chosen_comp} ({chosen_season})"
    )
    st.altair_chart(cumulative_chart, use_container_width=True)


def set_plot_cumulative_points_per_match(df, chosen_comp, chosen_season, get_expected_points, n_teams):
    df_copy = df.copy()

    base_chart = alt.Chart(df_copy).mark_line(point=True).encode(
        x=alt.X('Week:O', title='Week'),
        color=alt.Color('Club:N', legend=alt.Legend(title="Clubs", orient="right", labelLimit=2000))
    )

    actual_per_match_chart = base_chart.encode(
        y=alt.Y('Points/Match:Q'),
        strokeDash=alt.value([1, 0]),
        tooltip=['Club', 'Week', "Points/Match", "Ranking"]
    )

    if get_expected_points:
        df_copy = df_copy[df_copy["Partition"].notna()]
        df_copy["Week"] = df_copy["Partition"]

        expected_per_match_chart = alt.Chart(df_copy).mark_line(point=True).encode(
            x=alt.X('Week:O', title='Week'),
            y=alt.Y('xP/Match:Q'),
            color=alt.Color('Club:N', legend=alt.Legend(title="Clubs", orient="right", labelLimit=2000)),
            strokeDash=alt.value([4, 4]),
            tooltip=["Club", "Week", "xP/Match", "Diff Points", "Ranking"]
        )

        per_match_chart = alt.layer(actual_per_match_chart, expected_per_match_chart).encode(
        y=alt.Y(shorthand='Points/Match:Q', axis=alt.Axis(title="Actual and Expected Points per Match"))
        )
    else:
        per_match_chart = actual_per_match_chart

    st.altair_chart(
        per_match_chart.properties(
            title=f"Actual and Expected evolution of points per match - {chosen_comp} ({chosen_season})",
            height=510 if n_teams == 20 else 460 if n_teams == 18 else 600
        ),
        use_container_width=True
    )

    if get_expected_points:
        st.write("**Note**: The expected Points are based on what Fbref provides. "
                 "The figures are different from the pioneer xG source: Understat.com. **However, the trends are similar.**")