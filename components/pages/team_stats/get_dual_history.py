import streamlit as st
from streamlit_searchbox import st_searchbox

from components.commons.get_seasons import get_all_seasons
from utils.file_helper.reader import read_sql_file
from components.commons.get_seasons import get_seasons_by_comp
from components.queries.execute_query import execute_query
from components.pages.team_stats.get_teams_by_comp_by_season import get_teams_by_comp_by_season
from config import COMPETITIONS, DUAL_STATS


@st.cache_data(show_spinner=False)
def get_all_items(_db_conn):
    all_comps = [comp["label"] for comp in COMPETITIONS.values()]
    all_seasons = get_all_seasons(_db_conn)
    all_teams = set()

    for comp in all_comps:
        for season in all_seasons:
            teams_by_comp_by_season = set(get_teams_by_comp_by_season(_db_conn, comp, [season[7:]]))
            all_teams = all_teams | teams_by_comp_by_season

    return all_comps, all_seasons, all_teams

@st.cache_data(show_spinner=False)
def get_history(_db_conn, teamA, teamB, all_comps, all_seasons, side):
    sql_file = read_sql_file(
        "components/queries/team_stats/get_dual_history.sql",
        teamA=teamA,
        teamB=teamB,
        comps=', '.join([f"'{comp}'" for comp in all_comps]),
        seasons=', '.join([f"'{season[7:]}'" for season in all_seasons]),
        side=side
    )
    return execute_query(_db_conn, sql_file)

def make_search_function(all_teams: list[str], teamA = None):
    teams = all_teams.copy()
    if teamA:
        teams.remove(teamA)

    def search(term: str) -> list[str]:
        if not term:
            return []
        return [team for team in teams if term.lower() in team.lower()]
    return search


def get_dual_history(db_conn):
    all_comps, all_seasons, all_teams = list(get_all_items(db_conn))

    search_function = make_search_function(all_teams)

    teamA = st_searchbox(
        search_function=search_function,
        key="dual_history__teamA",
        placeholder="Choose Team A",
    )

    search_function = make_search_function(all_teams, teamA)

    teamB = st_searchbox(
        search_function=search_function,
        key="dual_history__teamB",
        placeholder="Choose Team B",
    )

    if teamA and teamB:

        side = st.radio(
            label="Side",
            options=[f"{teamA} home", "Both", f"{teamB} home"],
            horizontal=True,
            label_visibility="collapsed"
        )

        df = get_history(db_conn, teamA, teamB, all_comps, all_seasons, side)

        if side == "Both":
            df.rename(columns={
                "Wins_A": f"Wins {teamA}",
                "Wins_B": f"Wins {teamB}",
                "Goals_A": f"Goals {teamA}",
                "Goals_B": f"Goals {teamB}"
            }, inplace=True)

        st.dataframe(df, hide_index=True)