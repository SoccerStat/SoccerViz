import streamlit as st

from components.commons.seasons import get_all_season_schemas
from components.commons.streamlit.titles import set_sub_title, set_sub_sub_title, set_sub_sub_sub_title
from components.queries.execute_query import execute_query


@st.cache_data(show_spinner=False)
def _get_leg_precedence(_db_conn, all_season_schemas):
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
def _get_team_stats(_db_conn, all_season_schemas):
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


@st.cache_data(show_spinner=False)
def _get_duplicated_subs(_db_conn, all_season_schemas):
    union_query = " UNION ALL ".join(
        [
            f"""
                SELECT
                    '{season_schema[7:]}' AS "Season",
                    match as "Match",
                    CASE
                        WHEN regexp_count(id, '_') = 2
                        THEN substring(id FROM '[^_]+_(.*)')
                        ELSE id
                    END AS "Id Sub"
                FROM {season_schema}.event se
                WHERE outcome = 'substitute'
            """
            for season_schema in all_season_schemas
        ]
    )

    final_query = f"""
        WITH subs AS ({union_query})
        SELECT *, count(*)
        FROM subs
        GROUP BY "Season", "Match", "Id Sub"
        HAVING count(*) > 1
        ORDER BY "Season" desc, "Match", "Id Sub"
    """

    return execute_query(_db_conn, final_query)


@st.cache_data(show_spinner=False)
def _get_subs_with_unknown_players(_db_conn, all_season_schemas):
    union_query = " UNION ALL ".join(
        [
            f"""
                SELECT
                    '{season_schema[7:]}' AS "Season",
                    id as "Id Sub",
                    match as "Match",
                    team as "Team"
                FROM {season_schema}.event se
                WHERE id like '%unknown%'
            """
            for season_schema in all_season_schemas
        ]
    )

    final_query = f"""
            WITH subs AS ({union_query})
            SELECT *
            FROM subs
            ORDER BY "Season" desc, "Match", "Id Sub"
        """

    return execute_query(_db_conn, final_query)


def set_match_consistency_section(db_conn):
    all_season_schemas = get_all_season_schemas(db_conn)

    with st.container():
        set_sub_title("Match Consistency")

        set_sub_sub_title("Leg precedence")
        st.write(_get_leg_precedence(db_conn, all_season_schemas))

        set_sub_sub_title("Team Stats")
        st.write(_get_team_stats(db_conn, all_season_schemas))

        set_sub_sub_title("Substitutions")

        cols = st.columns([3, 5])
        with cols[0]:
            set_sub_sub_sub_title("Duplicated substitutions")
            st.write(_get_duplicated_subs(db_conn, all_season_schemas))

        with cols[1]:
            set_sub_sub_sub_title("Substitutions with unknown players")
            st.write(_get_subs_with_unknown_players(db_conn, all_season_schemas))
