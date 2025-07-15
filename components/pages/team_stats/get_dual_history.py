import streamlit as st

@st.cache_data(spinned=False)
def get_history(_db_conn, teamA, teamB, stat, side):
    sql_file = read_sql_file(
        "components/queries/team_stats/get_dual_history.sql",
        teamA=teamA,
        teamB=teamB,
        stat=stat,
        side=side
    )
    return execute_query(_db_conn, sql_file)

def get_dual_history(db_conn):
    all_teams = set()

    teamA = st.selectbox(
        key="dual_history__teamA",
        label="Choose competition...",
        options=all_teams
    )

    teamB = st.selectbox(
        key="dual_history__teamB",
        label="Choose competition...",
        options=all_teams.remove(teamA)
    )

    side = st.radio(
        label="Side",
        options=[f"{teamA} home", "Both", f"{teamB} home"],
        horizontal=True,
        label_visibility="collapsed"
    )

    stat_cols = st.columns([1,1,1])

    for i, stat in enumerate(stat_cols):
        with stat_cols[i]:
            df = get_history(db_conn, teamA, teamB, stat, side)
            st.dataframe(df)