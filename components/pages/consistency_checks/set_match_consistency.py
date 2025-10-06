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
                    '{season_schema[7:]}' AS "Season",
                    m.id AS "Id",
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


@st.cache_data(show_spinner=False)
def set_team_stats(_db_conn, all_season_schemas):
    union_query = " UNION ALL ".join(
        [
            f"""
                SELECT
                    '{season_schema[7:]}' AS "Season",
                    ts.match AS "Match",
                    ts.team AS "Team",
                    played_home AS "Played Home",
                    CASE
                        WHEN nb_shots_on_target is not null and e.id is null
                        then score <= nb_shots_on_target
                        ELSE true
                    END AS "Score <= On Target",
                    CASE
                        WHEN nb_shots_total is not null and e.id is null
                        then score <= nb_shots_total
                        ELSE true
                    END AS "Score <= Shots",
                    CASE
                        WHEN nb_shots_on_target is not null and nb_shots_total is not null
                        then nb_shots_on_target <= nb_shots_total
                        ELSE true
                    END AS "On target <= Shots",
                    CASE
                        WHEN nb_passes_succ is not null and nb_passes_total is not null
                        then nb_passes_succ <= nb_passes_total
                        ELSE true
                    END AS "Succ passes <= Total passes",
                    CASE
                        WHEN nb_saves_succ is not null and nb_saves_total is not null
                        then nb_saves_succ <= nb_saves_total
                        ELSE true
                    END AS "Succ saves <= Total saves",
                    CASE
                        WHEN penalty_shootout_scored is not null and penalty_shootout_total is not null
                        then penalty_shootout_scored <= penalty_shootout_total
                        ELSE true
                    END AS "Scored shootout <= Total shootout"
                FROM {season_schema}.team_stats ts
                LEFT JOIN (
                    SELECT
                        id,
                        match,
                        team,
                        outcome,
                        notes
                    FROM {season_schema}.event
                    WHERE outcome = 'own goal' OR notes = 'penalty kick in game'
                ) AS e
                ON ts.match = e.match and ts.team = e.team
            """
            for season_schema in all_season_schemas
        ]
    )

    final_query = f"""
        WITH checks AS ({union_query})
        SELECT
            "Season",
            "Match",
            "Played Home",
            "Team",
            "Score <= On Target",
            "Score <= Shots",
            "On target <= Shots",
            "Succ passes <= Total passes",
            "Succ saves <= Total saves"
        FROM checks
        WHERE NOT("Score <= Shots"
            AND "On target <= Shots"
            AND "Succ passes <= Total passes"
            AND "Succ saves <= Total saves"
            AND "Scored shootout <= Total shootout")
        ORDER BY "Season" DESC, "Match", "Played Home";
    """

    return execute_query(_db_conn, final_query)


def set_match_consistency_section(db_conn):
    all_season_schemas = get_all_season_schemas(db_conn)

    with st.container():
        set_sub_title("Match Consistency")

        set_sub_sub_title("Leg precedence")
        st.write(set_leg_precedence(db_conn, all_season_schemas))

        set_sub_sub_title("Shots")
        st.write(set_team_stats(db_conn, all_season_schemas))
