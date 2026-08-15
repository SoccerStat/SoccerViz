import streamlit as st
from streamlit_searchbox import st_searchbox

from components.commons.players import get_all_players
from components.commons.search_for_item import search_for_player


def get_player_info(db_conn):
    prefix = "player_info"
    all_players = list(get_all_players(db_conn))
    search_function = search_for_player(all_players)

    player = st_searchbox(
        search_function=search_function,
        key=f"{prefix}__player",
        placeholder="Choose Player",
    )

    st.write(player)
