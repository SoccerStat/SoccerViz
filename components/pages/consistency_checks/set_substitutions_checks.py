import streamlit as st

from components.commons.get_seasons import get_all_season_schemas
from components.commons.set_titles import set_sub_title, set_sub_sub_title
from components.queries.execute_query import execute_query


@st.cache_data(show_spinner=False)
def set_duplicated_subs(_db_conn, all_season_schemas):
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
def set_subs_with_unknown_players(_db_conn, all_season_schemas):
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


def set_substitutions_checks_section(db_conn):
    all_season_schemas = get_all_season_schemas(db_conn)
    with st.container():
        set_sub_title("Substitutions")
        cols = st.columns([3, 5])
        with cols[0]:
            duplicated_subs = set_duplicated_subs(db_conn, all_season_schemas)

            set_sub_sub_title("Duplicated substitutions")
            st.write(duplicated_subs)

        with cols[1]:
            subs_unknown_players = set_subs_with_unknown_players(db_conn, all_season_schemas)

            set_sub_sub_title("Substitutions with unknown players")
            st.write(subs_unknown_players)
