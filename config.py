import os

APP_CONFIG = {
    'icon': '⚽️',
    'layout': 'wide'
}

PREFIX_PAGE = "SoccerStat-II"
HOME_PAGE = PREFIX_PAGE
BASIC_STATS_PAGE = "Basic Stats"
MONITORING_PAGE = "Monitoring"
ANOMALY_DETECTION_PAGE = "Anomaly Detection"
TEAM_STATS_PAGE = "Team Stats"
PLAYER_STATS_PAGE = "Player Stats"

PAGES_CONFIG = [
    BASIC_STATS_PAGE,
    MONITORING_PAGE,
    TEAM_STATS_PAGE,
    PLAYER_STATS_PAGE
]

ALL_BUTTON_CONFIG = {
    "id": "all",
    "label_comps": "All Competitions",
    "label_seasons": "All Seasons",
    "style": {
            "bg_color": "#888888"
        }
}

SELECTED_BUTTON_CONFIG = {
    "bg_color": "#FAFAFA",
    "font_color": "#212121",
    "border_color": "#607D8B"
}

KIND_CHP = "CHP"
KIND_C_CUP = "C_CUP"

COMPETITIONS = {
    "premier_league": {
        "label": "Premier League",
        "diminutive": "PL",
        "kind": KIND_CHP,
        "style": {
            "bg_color": "#6200EA",
            "font_color": "#6200EA",
            "border_color": "#B388FF"
        }
    },
    "la_liga": {
        "label": "La Liga",
        "diminutive": "LL",
        "kind": KIND_CHP,
        "style": {
             "bg_color": "#FBC02D",
            "font_color": "#FBC02D",
            "border_color": "#FFF176"
        }
    },
    "fussball_bundesliga": {
        "label": "Fußball-Bundesliga",
        "diminutive": "BL",
        "kind": KIND_CHP,
        "id_comp": "fussball_bundesliga",
        "style": {
            "bg_color": "#D32F2F",
            "font_color": "#D32F2F",
            "border_color": "#FF6659"
        }
    },
    "serie_a": {
        "label": "Serie A",
        "diminutive": "SA",
        "kind": KIND_CHP,
        "style": {
            "bg_color": "#2E7D32",
            "font_color": "#2E7D32",
            "border_color": "#81C784"
        }
    },
    "ligue_1": {
        "label": "Ligue 1",
        "diminutive": "L1",
        "kind": KIND_CHP,
        "style": {
            "bg_color": "#1976D2",
            "font_color": "#1976D2",
            "border_color": "#64B5F6"
        }
    },
    "uefa_champions_league": {
        "label": "UEFA Champions League",
        "diminutive": "UCL",
        "kind": KIND_C_CUP,
        "style": {
            "bg_color": "#050A30",
            "font_color": "white",
            "border_color": "#143F6B"
        }
    },
    "uefa_europa_league": {
        "label": "UEFA Europa League",
        "diminutive": "UEL",
        "kind": KIND_C_CUP,
        "style": {
            "bg_color": "#D35400",
            "font_color": "white",
            "border_color": "#ED722E"
        }
    },
    "uefa_conference_league": {
        "label": "UEFA Conference League",
        "diminutive": "UECL",
        "kind": KIND_C_CUP,
        "style": {
            "bg_color": "#2E8B57",
            "font_color": "white",
            "border_color": "#55BC39"
        }
    }
}

ALL_SEASONS_MODE = "All Seasons"
RANGE_SEASONS_MODE = "Range of Seasons"
COMPARE_SEASONS_MODE = "Compare Seasons"

DATABASE_CONFIG = {
    'default_host': os.getenv('DB_HOST', '10.0.0.1'),
    'default_port': os.getenv('DB_PORT', '5432'),
    'default_database': os.getenv('DB_NAME', 'prd_soccersql'),
    'default_user': os.getenv('DB_USER', 'thomas')
}

CHART_CONFIG = {
    'color_palette': ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57'],
    'default_height': 400
}

FALLBACK_CSS = """
<style>
    .main-title {
        text-align: center;
        color: #1f77b4;
        font-size: 2.5rem;
        margin-bottom: 2rem;
    }
    .nav-section {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .nav-title {
        text-align: center;
        color: #333;
        margin-bottom: 1rem;
    }
    .stButton > button {
        width: 100%;
        margin: 0.25rem;
    }
</style>
"""

TEAM_RANKINGS = [
    "Attendance",
    "Matches",
    "Points",
    "Points/Match",
    "Wins",
    "Draws",
    "Loses",
    "Goals For",
    "Goals Against",
    "Goals Diff",
    "Clean Sheets",
    "xG For (fbref)",
    "xG For (understat)",
    "xG For/Match (fbref)",
    "xG For/Match (understat)",
    "xG Against (fbref)",
    "xG Against (understat)",
    "xG Against/Match (fbref)",
    "xG Against/Match (understat)",
    "Yellow Cards",
    "Red Cards",
    "Incl. 2 Yellow Cards",
    "Fouls",

    "Shots For",
    "Shots on Target For",
    "Shots Against",
    "Shots on Target Against",

    "Succ Passes",
    "Att Passes",
    "Succ Passes Rate",

    "Shots Conversion Rate For",
    "Shots Conversion Rate Against",
    "Shots on Target Conversion Rate For",
    "Shots on Target Conversion Rate Against"
]

DUAL_STATS = [
    "Matches",
    "Wins",
    "Draws",
    "Loses",
    "Goals For",
    "Goals Against"
]

C_CUPS_TEAMS_EXCLUDED_RANKINGS = [
    "Points",
    "Points/Match",
    "xG For",
    "xG For/Match",
    "xG Against",
    "xG Against/Match"
]