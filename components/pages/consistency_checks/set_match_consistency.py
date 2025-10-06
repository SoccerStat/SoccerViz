import streamlit as st

from components.commons.get_seasons import get_all_season_schemas
from components.commons.set_titles import set_sub_title, set_sub_sub_title
from components.queries.execute_query import execute_query


@st.cache_data(show_spinner=False)
def set_leg_precedence(_db_conn, all_season_schemas):
    union_query = " UNION ALL ".join(
        [
            f"""
                SELECT
                    '{season_schema[7:]}' as "Season",
                    m.id as "Id",
                    m.leg AS "Leg",
                    lag(m.leg) over (
                        PARTITION BY m.competition, ts.teams, round, week
                        ORDER BY date
                    ) AS "Prev. leg"
                FROM {season_schema}.match m
                JOIN (
                    SELECT match, array_agg(team ORDER BY team) AS teams
                    FROM {season_schema}.team_stats
                    GROUP BY match
                ) ts
                ON m.id = ts.match
                JOIN (
                    SELECT id
                    FROM upper.competition
                    WHERE kind IN ('domestic_cup', 'continental_cup')
                ) comp
                ON m.competition = comp.id
            """
            for season_schema
            in all_season_schemas
        ]
    )

    final_query = f"""
        WITH legs AS ({union_query})
        SELECT "Season", "Id"
        FROM legs
        WHERE "Leg" = 2 AND "Prev. leg" IS NULL
        ORDER BY "Season" DESC, "Id";
    """

    return execute_query(_db_conn, final_query)


def set_match_consistency_section(db_conn):
    all_season_schemas = get_all_season_schemas(db_conn)

    with st.container():
        set_sub_title("Match Consistency")

        set_sub_sub_title("Leg precedence")
        st.write(set_leg_precedence(db_conn, all_season_schemas))
