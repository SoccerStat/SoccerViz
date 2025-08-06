import streamlit as st

from components.commons.get_all_teams import get_teams_by_comp_by_season
from components.commons.get_seasons import get_seasons_by_comp
from components.commons.search_for_item import make_search_function
from components.commons.set_titles import set_sub_sub_sub_title
from components.queries.execute_query import execute_query

from utils.file_helper.reader import read_sql_file
from config import COMPETITIONS, KIND_C_CUP, KIND_CHP

@st.cache_data(show_spinner=False)
def get_players_with_given_rate_minutes(_db_conn, chosen_comp, chosen_season, chosen_team, chosen_rate, chosen_side, r=3):
    sql_file = read_sql_file(
        file_name="components/queries/team_stats/by_competition/one_team/get_players_with_given_rate_minutes.sql",
        chosen_comp=chosen_comp,
        chosen_season=chosen_season,
        name_team=chosen_team,
        rate=chosen_rate,
        in_side=chosen_side.lower(),
        r=r
    )

    return execute_query(_db_conn, sql_file)

@st.cache_data(show_spinner=False)
def get_stats_of_team(
        _db_conn,
        chosen_team,
        chosen_comp,
        chosen_season,
        side,
        first_week,
        last_week,
        first_date,
        last_date
):
    sql_file = read_sql_file(
        "components/queries/team_stats/by_competition/one_team/get_one_team_stats.sql",
        name_team=chosen_team,
        name_comp=chosen_comp,
        season=chosen_season,
        in_side=side.lower(),
        first_week=first_week,
        last_week=last_week,
        first_date=first_date,
        last_date=last_date
    )
    return execute_query(_db_conn, sql_file)


@st.cache_data(show_spinner=False)
def get_matches_of_team(
        _db_conn,
        chosen_team,
        chosen_comp,
        chosen_season,
        side,
        first_week,
        last_week,
        first_date,
        last_date,
        kind_comp
):
    sql_file = read_sql_file(
        "components/queries/team_stats/by_competition/one_team/get_one_team_matches.sql",
        name_team=chosen_team,
        name_comp=chosen_comp,
        season=chosen_season,
        in_side=side.lower(),
        first_week=first_week,
        last_week=last_week,
        first_date=first_date,
        last_date=last_date,
        kind_comp=kind_comp
    )
    return execute_query(_db_conn, sql_file)


def get_stats_and_matches_one_team(db_conn):
    comps_and_kind = {comp["label"]: comp["kind"] for comp in COMPETITIONS.values()}
    comps = list(comps_and_kind.keys())

    chosen_comp = st.selectbox(
        key="stats_one_team__comp",
        label="Choose competition...",
        options=comps
    )

    seasons_by_comp = get_seasons_by_comp(db_conn, chosen_comp)

    chosen_season = st.selectbox(
        key="stats_one_team__season",
        label="Choose season...",
        options=seasons_by_comp
    )


    all_teams_of_comp_of_season = get_teams_by_comp_by_season(db_conn, chosen_comp, [chosen_season])
    n_teams = len(all_teams_of_comp_of_season)

    search_function = make_search_function(all_teams_of_comp_of_season)

    # chosen_team = st_searchbox(
    #     search_function=search_function,
    #     key="stats_one_team__team",
    #     placeholder="Choose Team A",
    # )

    chosen_team = st.selectbox(
        key="stats_one_team__team",
        label="Choose a team...",
        options=[""] + all_teams_of_comp_of_season
    )

    if chosen_team:
        first_week = 1
        last_week = 100
        first_date = '1970-01-01'
        last_date = '2099-12-31'

        if comps_and_kind[chosen_comp] == KIND_CHP:

            filter_weeks= st.checkbox(
                key='stats_one_team__filter_weeks',
                label='Filter by week'
            )

            if filter_weeks:
                col1, col2 = st.columns(2)
                max_week = 2 * (n_teams - 1)

                with col1:
                    first_week = st.slider(
                        key='stats_one_team__first_week',
                        label="First week",
                        min_value=1,
                        max_value=max_week,
                        value=1
                    )

                if first_week == max_week:
                    last_week = max_week
                else:
                    with col2:
                        last_week = st.slider(
                            key='stats_one_team__last_week',
                            label="Last week",
                            min_value=first_week,
                            max_value=max_week,
                            value=first_week
                        )

        filter_dates = st.checkbox(
            key='stats_one_team__filter_dates',
            label='Filter by date'
        )

        if filter_dates:
            col1, col2 = st.columns(2)

            with col1:
                first_date = st.date_input(
                    key='stats_one_team__first_date',
                    label="First date",
                    value="today"
                )

            with col2:
                last_date = st.date_input(
                    key='stats_one_team__last_date',
                    label="Last date",
                    value=first_date
                )

        sides = ["Home", "Both", "Away", "Neutral", "All"] if comps_and_kind[chosen_comp] == KIND_C_CUP else ["Home", "Both", "Away"]
        side = st.radio(
            key='stats_one_team__side',
            label="Side",
            options=sides,
            horizontal=True,
            label_visibility="collapsed",
            index=1
        )

        set_sub_sub_sub_title("Basic Stats")

        team_stats = get_stats_of_team(
            db_conn,
            chosen_team,
            chosen_comp,
            chosen_season,
            side,
            first_week,
            last_week,
            first_date,
            last_date
        )

        team_stats_first_row = team_stats[["Club", "M", "W", "D", "L", "GF", "GA", "GD"]]
        team_stats_second_row = team_stats[["Club", "% Succ Passes"]]
        team_stats_third_row = team_stats[["Club", "Shots/onTarget For CR", "Shots/Goals For CR", "onTarget/Goals For CR"]]
        team_stats_fourth_row = team_stats[["Club", "Shots/onTarget Against CR", "Shots/Goals Against CR", "onTarget/Goals Against CR"]]

        st.dataframe(team_stats_first_row, hide_index=True)
        st.dataframe(team_stats_second_row, hide_index=True)
        st.dataframe(team_stats_third_row, hide_index=True)
        st.dataframe(team_stats_fourth_row, hide_index=True)

        set_sub_sub_sub_title("% of players used")

        col, _ = st.columns(2)
        with col:
            chosen_rate = st.slider(
                key="rate_players_one_season__rate",
                label="% of minutes played",
                min_value=0,
                max_value=100,
                value=100
            )

        df = get_players_with_given_rate_minutes(db_conn, chosen_comp, chosen_season, chosen_team, chosen_rate, side)
        df['Age'] = df['Age'].astype(int)
        st.dataframe(df.drop("Total number of players used", axis=1))
        if not df.empty:
            avg_age = df['Age'].mean()
            st.write(f"Average age of the club: {int(avg_age)} years, {int((avg_age % 1) * 365)} days")

            n_players = df.shape[0]
            n_players_of_team = int(df["Total number of players used"].iloc[0])

            st.write(f"{n_players} players that have played at least {int(chosen_rate)}%"
                     f" of the possible minutes played "
                     f"(or {round(100 * n_players / n_players_of_team, 2)}% of the players of the club that are involved in {chosen_comp})")

        set_sub_sub_sub_title("Selected matches")

        team_matches = get_matches_of_team(
            db_conn,
            chosen_team,
            chosen_comp,
            chosen_season,
            side,
            first_week,
            last_week,
            first_date,
            last_date,
            comps_and_kind[chosen_comp]
        )

        if comps_and_kind[chosen_comp] == KIND_CHP:
            if not team_matches.empty:
                team_matches = team_matches.drop("Round", axis=1)

        st.dataframe(team_matches, hide_index=True)
