import streamlit as st
import numpy as np

from components.commons.get_all_teams import get_teams_by_comp_by_season
from components.commons.get_seasons import get_seasons_by_comp
from components.commons.streamlit_widgets import select__get_one_season, select__generic, slider__generic
from components.queries.execute_query import execute_query

from utils.file_helper.reader import read_sql_file


@st.cache_data(show_spinner=False)
def get_players_with_given_rate_minutes(_db_conn, chosen_season, chosen_team, r=3):
    sql_file = read_sql_file(
        file_name="components/queries/team_stats/all_competitions/players_by_team/get_players_with_given_rate.sql",
        chosen_season=chosen_season,
        name_team=chosen_team,
        r=r
    )

    return execute_query(_db_conn, sql_file)


def get_players_by_team(db_conn):
    prefix = "all_comps_players_by_team"

    chosen_season = select__get_one_season(
        prefix=prefix,
        custom_options=get_seasons_by_comp(db_conn, name_comp="All Competitions")
    )

    if chosen_season:
        all_teams_of_comp_of_season = get_teams_by_comp_by_season(db_conn, "all", [chosen_season])
        # n_teams = len(all_teams_of_comp_of_season)

        chosen_team = select__generic(
            prefix=prefix,
            suffix="team",
            label="Choose a team...",
            options=all_teams_of_comp_of_season
        )

        if chosen_team:
            df_team = get_players_with_given_rate_minutes(db_conn, chosen_season, chosen_team)

            col, _ = st.columns(2)
            with col:
                max_nb_matches = int(df_team["Total number of matches"].unique())
                chosen_nb_matches = slider__generic(
                    prefix=prefix,
                    suffix="nb_matches",
                    label="Minimum number of matches played",
                    min_value=0,
                    max_value=max_nb_matches,
                    default_value=0
                )

            df_team = df_team[df_team["Matches"] >= chosen_nb_matches]
            avg_age = df_team['Age'].mean()
            df_team['Age'] = df_team['Age'].astype(int)
            df_team.index = np.arange(1, len(df_team) + 1)

            st.dataframe(df_team.drop(["Total number of matches", "Total number of players used"], axis=1))

            if not df_team.empty:
                st.write(f"Average age of the club: **{int(avg_age)} years, {int((avg_age % 1) * 365)} days**")

                n_players = df_team.shape[0]
                n_players_of_team = int(df_team["Total number of players used"].iloc[0])

                st.write(f"{n_players} player{'s' if n_players > 1 else ''} that ha{'ve' if n_players > 1 else 's'} played "
                         f"at least {chosen_nb_matches} match{'es' if chosen_nb_matches > 1 else ''} "
                         f"(or {round(100 * n_players / n_players_of_team, 2)}% of the players of the club "
                         f"that are involved in all competitions).")
