import streamlit as st

from components.commons.get_all_teams import get_teams_by_comp_by_season
from components.commons.get_seasons import get_seasons_by_comp
from components.queries.execute_query import execute_query

from utils.file_helper.reader import read_sql_file


@st.cache_data(show_spinner=False)
def get_players_with_given_rate_minutes(_db_conn, chosen_season, chosen_team, r=3):
    sql_file = read_sql_file(
        file_name="components/queries/team_stats/all_competitions/players_by_team/get_players_with_given_rate_minutes.sql",
        chosen_season=chosen_season,
        name_team=chosen_team,
        r=r
    )

    return execute_query(_db_conn, sql_file)

def get_players_by_team(db_conn):
    chosen_season = st.selectbox(
        key="all_comps_players_by_team__season",
        label="Choose season...",
        options=get_seasons_by_comp(db_conn, "All Competitions")
    )

    all_teams_of_comp_of_season = get_teams_by_comp_by_season(db_conn, "all", [chosen_season])
    n_teams = len(all_teams_of_comp_of_season)

    chosen_team = st.selectbox(
        key="all_comps_players_by_team__team",
        label="Choose a team...",
        options=[""] + all_teams_of_comp_of_season
    )

    if chosen_team:
        df_team = get_players_with_given_rate_minutes(db_conn, chosen_season, chosen_team)

        col, _ = st.columns(2)
        with col:
            max_nb_matches = int(df_team["Total number of matches"].unique())
            chosen_nb_matches = st.slider(
                key="all_comps_players_by_team__nb_matches",
                label="Number of matches played",
                min_value=0,
                max_value=max_nb_matches,
                value=0
            )

        df_team = df_team[df_team["Matches"] >= chosen_nb_matches]
        avg_age = df_team['Age'].mean()
        df_team['Age'] = df_team['Age'].astype(int)

        st.dataframe(df_team.drop(["Total number of matches", "Total number of players used"], axis=1))

        if not df_team.empty:
            st.write(f"Average age of the club: {int(avg_age)} years, {int((avg_age % 1) * 365)} days")

            n_players = df_team.shape[0]
            n_players_of_team = int(df_team["Total number of players used"].iloc[0])

            st.write(f"{n_players} players that have played at least {chosen_nb_matches} matche{'s' if chosen_nb_matches == 0 else ''} "
                     f"(or {round(100 * n_players / n_players_of_team, 2)}% of the players of the club "
                     f"that are involved in all competitions)")
