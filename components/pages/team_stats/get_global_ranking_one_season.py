import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
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
            label="Calculate Expected Points",
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

            if get_expected_points:
                st.write("**Note**: The expected Points are based on what Fbref provides. "
                         "The figures are different from the pioneer xG source: Understat.com. **However, the trends are similar.**")

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

    # set_plot_cumulative_points(filtered_df, chosen_comp, chosen_season, n_teams, get_expected_points)
    set_plot_cumulative_points_plotly(filtered_df, chosen_comp, chosen_season, n_teams, get_expected_points)
    # set_plot_cumulative_points_per_match(filtered_df, chosen_comp, chosen_season, get_expected_points, n_teams)
    set_plot_cumulative_points_per_match_plotly(filtered_df, chosen_comp, chosen_season, get_expected_points, n_teams)


def set_plot_cumulative_points_plotly(df, chosen_comp, chosen_season, n_teams, get_expected_points):
    weeks = sorted(df['Week'].unique())
    max_points = [3 * int(w) for w in weeks]

    # Ligne Max Possible
    max_line = go.Scatter(
        x=weeks,
        y=max_points,
        mode='lines',
        line=dict(color='gray', dash='dash'),
        name='Max Possible',
        hoverinfo='skip',
        showlegend=True
    )

    # Points réels
    df_actual = df[["Ranking", "Club", "Week", "Points"]].drop_duplicates()
    clubs = sorted(df_actual['Club'].unique())
    colors = px.colors.qualitative.D3  # palette qualitative de Plotly

    # Map club -> color
    club_colors = {club: colors[i % len(colors)] for i, club in enumerate(clubs)}

    actual_traces = []
    for club in clubs:
        df_club = df_actual[df_actual['Club'] == club].sort_values('Week')
        actual_traces.append(
            go.Scatter(
                x=df_club['Week'],
                y=df_club['Points'],
                mode='lines+markers',
                name=club,
                hovertemplate=(
                    f"<b>{club}</b><br>" +
                    "Week: %{x}<br>" +
                    "Points: %{y}<br>" +
                    "Ranking: %{customdata[0]}<extra></extra>"
                ),
                customdata=df_club[['Ranking']],
                line=dict(color=club_colors[club]),
                marker=dict(color=club_colors[club]),
                showlegend=True,
            )
        )

    data = [max_line] + actual_traces

    if get_expected_points:
        df_expected = df[df["Partition"].notna()].copy()
        df_expected["Week"] = df_expected["Partition"]

        expected_traces = []
        for club in clubs:
            df_club_exp = df_expected[df_expected['Club'] == club].sort_values('Week')
            if df_club_exp.empty:
                continue
            expected_traces.append(
                go.Scatter(
                    x=df_club_exp['Week'],
                    y=df_club_exp['xP'],
                    mode='lines+markers',
                    name=f"{club} (Expected)",
                    line=dict(dash='dot'),
                    hovertemplate=(
                        f"<b>{club} (Expected)</b><br>" +
                        "Week: %{x}<br>" +
                        "xP: %{y}<br>" +
                        "Diff Points: %{customdata[0]}<br>" +
                        "Ranking: %{customdata[1]}<extra></extra>"
                    ),
                    customdata=df_club_exp[['Diff Points', 'Ranking']],
                    showlegend=True
                )
            )
        data += expected_traces

    # Layout
    layout = go.Layout(
        title=f"Evolution of points - {chosen_comp} ({chosen_season})",
        xaxis=dict(title='Week', type='category'),
        yaxis=dict(title='Points'),
        height=510 if n_teams == 20 else 460 if n_teams == 18 else 600,
        legend=dict(title='Clubs', y=1, yanchor='top', x=1.05, xanchor='left'),
        margin=dict(l=50, r=150, t=80, b=50)
    )

    fig = go.Figure(data=data, layout=layout)

    st.plotly_chart(fig, use_container_width=True)


def set_plot_cumulative_points(df, chosen_comp, chosen_season, n_teams, get_expected_points):
    weeks = sorted(df['Week'].unique())
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

    df_actual = df[["Ranking", "Club", "Week", "Points"]].drop_duplicates()

    # TODO .mark_line(interpolate = 'step-after', point=True) for stairs plot

    actual_chart = alt.Chart(df_actual).mark_line(point=True).encode(
        x=alt.X('Week:O', title='Week'),
        y=alt.Y('Points:Q', title=f'Actual Points'),
        color=alt.Color('Club:N', legend=alt.Legend(title="Clubs", orient="right", labelLimit=2000)),
        tooltip=['Club', 'Week', "Points", "Ranking"]
    )

    if get_expected_points:
        df_expected = df[df["Partition"].notna()]
        df_expected["Week"] = df_expected["Partition"]

        expected_chart = alt.Chart(df_expected).mark_line(point=True).encode(
            x=alt.X('Week:O', title='Week'),
            y=alt.Y('xP:Q'),
            color=alt.Color('Club:N', legend=alt.Legend(title="Clubs", orient="right", labelLimit=2000)),
            strokeDash=alt.value([4, 4]),
            tooltip=["Club", "Week", "xP", "Diff Points", "Ranking"]
        )

        concat_charts = alt.layer(actual_chart, expected_chart, max_points_line).encode(
            y=alt.Y(shorthand='Points/Match:Q', title="Actual and Expected Points")
        )
    else:
        concat_charts = alt.layer(actual_chart, max_points_line)

    cumulative_chart = concat_charts.properties(
        title=f"Evolution of points - {chosen_comp} ({chosen_season})",
        height=510 if n_teams == 20 else 460 if n_teams == 18 else 600
    )
    st.altair_chart(cumulative_chart, use_container_width=True)


def set_plot_cumulative_points_per_match_plotly(df, chosen_comp, chosen_season, get_expected_points, n_teams):
    df_actual = df[["Ranking", "Club", "Week", "Points/Match"]].drop_duplicates()

    weeks = sorted(df['Week'].unique())
    # Ticks toutes les 2 semaines (ex: impaires)
    tickvals = [w for w in weeks if int(w) % 2 == 1]
    clubs = sorted(df_actual['Club'].unique())
    colors = px.colors.qualitative.D3  # palette qualitative de Plotly

    # Map club -> color
    club_colors = {club: colors[i % len(colors)] for i, club in enumerate(clubs)}

    actual_traces = []
    for club in clubs:
        df_club = df_actual[df_actual['Club'] == club].sort_values('Week')
        actual_traces.append(
            go.Scatter(
                x=df_club['Week'],
                y=df_club['Points/Match'],
                mode='lines+markers',
                name=club,
                hovertemplate=(
                    f"<b>{club}</b><br>" +
                    "Week: %{x}<br>" +
                    "Points/Match: %{y:.2f}<br>" +
                    "Ranking: %{customdata[0]}<extra></extra>"
                ),
                customdata=df_club[['Ranking']],
                line=dict(color=club_colors[club]),
                marker=dict(color=club_colors[club]),
                showlegend=True
            )
        )

    data = actual_traces

    if get_expected_points:
        df_expected = df[df["Partition"].notna()].copy()
        df_expected["Week"] = df_expected["Partition"]

        expected_traces = []
        for club in clubs:
            df_club_exp = df_expected[df_expected['Club'] == club].sort_values('Week')
            if df_club_exp.empty:
                continue
            expected_traces.append(
                go.Scatter(
                    x=df_club_exp['Week'],
                    y=df_club_exp['xP/Match'],
                    mode='lines+markers',
                    name=f"{club} (Expected)",
                    line=dict(dash='dot'),
                    hovertemplate=(
                        f"<b>{club} (Expected)</b><br>" +
                        "Week: %{x}<br>" +
                        "xP/Match: %{y:.2f}<br>" +
                        "Diff Points: %{customdata[0]}<br>" +
                        "Ranking: %{customdata[1]}<extra></extra>"
                    ),
                    customdata=df_club_exp[['Diff Points', 'Ranking']],
                    showlegend=True
                )
            )
        data += expected_traces

    layout = go.Layout(
        title=f"Actual and Expected evolution of points per match - {chosen_comp} ({chosen_season})",
        xaxis=dict(
            title='Week',
            type='category',
            tickmode='array',
            tickvals=tickvals,
            ticktext=[str(w) for w in tickvals],
        ),
        yaxis=dict(title='Points per Match'),
        height=510 if n_teams == 20 else 460 if n_teams == 18 else 600,
        legend=dict(title='Clubs', y=1, yanchor='top', x=1.05, xanchor='left'),
        margin=dict(l=50, r=150, t=80, b=50),
    )

    fig = go.Figure(data=data, layout=layout)
    st.plotly_chart(fig, use_container_width=True)


def set_plot_cumulative_points_per_match(df, chosen_comp, chosen_season, get_expected_points, n_teams):
    df_actual = df[["Ranking", "Club", "Week", "Points/Match"]].drop_duplicates()

    actual_per_match_chart = alt.Chart(df_actual).mark_line(point=True).encode(
        x=alt.X('Week:O', title='Week'),
        y=alt.Y('Points/Match:Q', title="ActualPoints per Match"),
        color=alt.Color('Club:N', legend=alt.Legend(title="Clubs", orient="right", labelLimit=2000)),
        strokeDash=alt.value([1, 0]),
        tooltip=['Club', 'Week', "Points/Match", "Ranking"]
    )

    if get_expected_points:
        df_expected = df[df["Partition"].notna()]
        df_expected["Week"] = df_expected["Partition"]

        expected_per_match_chart = alt.Chart(df_expected).mark_line(point=True).encode(
            x=alt.X('Week:O', title='Week'),
            y=alt.Y('xP/Match:Q'),
            color=alt.Color('Club:N', legend=alt.Legend(title="Clubs", orient="right", labelLimit=2000)),
            strokeDash=alt.value([4, 4]),
            tooltip=["Club", "Week", "xP/Match", "Diff Points", "Ranking"]
        )

        per_match_chart = alt.layer(actual_per_match_chart, expected_per_match_chart).encode(
            y=alt.Y(shorthand='Points/Match:Q', title="Actual and Expected Points per Match")
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