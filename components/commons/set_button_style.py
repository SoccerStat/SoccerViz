from streamlit_extras.stylable_container import stylable_container

from config import SELECTED_BUTTON_CONFIG


def set_button_with_style(
        key,
        bg_color="white",
        font_color="black",
        border_color="black",
        width="100%",
        height='60px',
        is_selected=False
):
    """
    Crée un bouton stylé avec possibilité de forcer l'état sélectionné

    Args:
        font_color:
        border_color:
        is_selected:
        :param key: Clé unique du bouton
        :param bg_color: Couleur de fond par défaut
        :param font_color: Couleur de police par défaut
        :param border_color: Couleur de bordure par défaut
        :param width: largeur du bouton
        :param height: longueur du bouton
        :param is_selected: Force l'apparence sélectionnée si True
    """
    selected_bg_color = SELECTED_BUTTON_CONFIG["bg_color"]
    selected_font_color = SELECTED_BUTTON_CONFIG["font_color"]
    selected_border_color = SELECTED_BUTTON_CONFIG["border_color"]

    # Si le bouton est sélectionné, utiliser les couleurs de sélection
    if is_selected:
        current_bg_color = selected_bg_color
        current_font_color = selected_font_color
        current_border_color = selected_border_color
    else:
        current_bg_color = bg_color
        current_font_color = font_color
        current_border_color = border_color

    return stylable_container(
        key=key,
        css_styles=f"""
            .stButton > button {{
                background: {current_bg_color};
                color: {current_font_color};
                border: 2px solid {current_border_color};
                border-radius: 12px;
                padding: 0.4em 1em;
                font-weight: 600;
                font-size: 0.9rem;
                transition: all 0.2s ease-in-out;
                cursor: pointer;
                width: {width};
                height: {height};
                outline: none;
            }}
            .stButton > button:hover {{
                transform: scale(1.05);
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            }}
            .stButton > button:focus,
            .stButton > button:active {{
                background: {selected_bg_color} !important;
                color: {selected_font_color} !important;
                border: 2px solid {selected_border_color} !important;
                box-shadow: none !important;
                outline: none !important;
                transform: scale(0.96);
            }}
        """
    )
