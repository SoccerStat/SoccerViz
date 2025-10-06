import streamlit as st

from components.commons.get_seasons import get_all_season_schemas
from components.commons.set_titles import set_sub_title
from components.queries.execute_query import execute_query


@st.cache_data(show_spinner=False)
def get_teams_by_competition(_db_conn):
    all_season_schemas = get_all_season_schemas(_db_conn)

    union_query = " UNION ALL ".join(
        [
            f"""
                SELECT
                    '{season_schema[7:]}' AS "Season",
                    t.competition as "Competition",
                    COUNT(t. *) AS "Total From team",
                    COUNT(tp. *) AS "Total From team_player",
                    COUNT(m. *) AS "Total From match",
                    COUNT(ts.*) AS "Total From team_stats"
                FROM {season_schema}.team t
                FULL OUTER JOIN (SELECT DISTINCT team FROM {season_schema}.team_player) AS tp
                ON t.id = tp.team
                FULL OUTER JOIN (
                    SELECT competition, home_team as team FROM {season_schema}.match
                    UNION SELECT competition, away_team as team FROM {season_schema}.match
                ) AS m
                ON t.id = m.team
                FULL OUTER JOIN (
                    SELECT team
                    FROM {season_schema}.team_stats
                ) AS ts
                ON t.id = ts.team
                GROUP BY t.competition
                """
            for season_schema in all_season_schemas
        ]
    )

    final_query = f"""
            WITH seasons AS ({union_query})
            SELECT *
            FROM seasons
            WHERE
                "Competition" IN (SELECT id from upper.competition WHERE kind IN ('championship', 'continental_cup'))
                AND (
                    "Total From team" != "Total From team_player"
                    OR "Total From team" != "Total From match"
                    OR "Total From team" != "Total From team_stats"
                    OR "Total From team_player" != "Total From match"
                    OR "Total From team_player" != "Total From team_stats"
                    OR "Total From match" != "Total From team_stats"
                )
            ORDER BY "Season" desc, "Competition";
        """

    return execute_query(_db_conn, final_query)


def set_teams_by_competition_section(db_conn):
    teams_by_competition = get_teams_by_competition(db_conn)

    set_sub_title("Teams by competition in each table")
    st.write(teams_by_competition)
