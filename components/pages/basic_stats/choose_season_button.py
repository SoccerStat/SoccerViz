import streamlit as st

from components.commons.set_button_style import set_button_with_style
from components.commons.get_all_seasons import get_all_seasons
from components.queries.execute_query import execute_query
from config import ALL_BUTTON_CONFIG

def select_all_seasons_by_comp(db_conn, all_seasons, id_comp):
    if id_comp != "all_comps":
        condition_comp = f"WHERE competition = '{id_comp}'"
    else:
        condition_comp = ""

    union_query = " UNION ALL ".join(
        [
            f"(SELECT '{schema[7:]}' as season FROM {schema}.match {condition_comp} LIMIT 1)"
            for schema in all_seasons]
    )
    final_query = f"SELECT DISTINCT season AS distinct_season FROM ({union_query}) AS all_counts;"
    result = execute_query(db_conn, final_query)
    return result['distinct_season'].tolist()

def choose_season_button(db_conn, id_comp):
    all_seasons = get_all_seasons(db_conn)

    key_all_seasons = f"{ALL_BUTTON_CONFIG["id"]}_seasons"

    if "selected_seasons" not in st.session_state:
        st.session_state.selected_seasons = select_all_seasons_by_comp(db_conn, all_seasons, id_comp)

    with st.container():
        col_all, col_range, col_compare = st.columns([1, 1, 1], gap="large")

        with col_all:
            with set_button_with_style(key_all_seasons):
                if st.button(ALL_BUTTON_CONFIG["label_seasons"], key=key_all_seasons):
                    st.session_state.selected_seasons = select_all_seasons_by_comp(db_conn, all_seasons, id_comp)

        with col_range:
            pass

        with col_compare:
            pass

    return st.session_state.selected_seasons