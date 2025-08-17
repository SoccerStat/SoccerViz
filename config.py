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
TEAM_STATS_PAGES = "Team Stats"
TEAM_STATS_ALL_PAGE = "Team Stats - All Competitions"
TEAM_STATS_SPECIFIC_PAGE = "Team Stats - Given Competition"
PLAYER_STATS_PAGE = "Player Stats"

PAGES_CONFIG = [
    BASIC_STATS_PAGE,
    MONITORING_PAGE,
    TEAM_STATS_ALL_PAGE,
    TEAM_STATS_SPECIFIC_PAGE,
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
            "bg_color": "#B388FF",
            "font_color": "#6200EA",
            "border_color": "#6200EA"
        }
    },
    "la_liga": {
        "label": "La Liga",
        "diminutive": "LL",
        "kind": KIND_CHP,
        "style": {
             "bg_color": "#FFF176",
            "font_color": "#FBC02D",
            "border_color": "#FBC02D"
        }
    },
    "fussball_bundesliga": {
        "label": "Fußball-Bundesliga",
        "diminutive": "BL",
        "kind": KIND_CHP,
        "id_comp": "fussball_bundesliga",
        "style": {
            "bg_color": "#FF6659",
            "font_color": "#D32F2F",
            "border_color": "#D32F2F"
        }
    },
    "serie_a": {
        "label": "Serie A",
        "diminutive": "SA",
        "kind": KIND_CHP,
        "style": {
            "bg_color": "#81C784",
            "font_color": "#2E7D32",
            "border_color": "#2E7D32"
        }
    },
    "ligue_1": {
        "label": "Ligue 1",
        "diminutive": "L1",
        "kind": KIND_CHP,
        "style": {
            "bg_color": "#64B5F6",
            "font_color": "#1976D2",
            "border_color": "#1976D2"
        }
    },
    "uefa_champions_league": {
        "label": "UEFA Champions League",
        "diminutive": "UCL",
        "kind": KIND_C_CUP,
        "style": {
            "bg_color": "#143F6B",
            "font_color": "white",
            "border_color": "#050A30"
        }
    },
    "uefa_europa_league": {
        "label": "UEFA Europa League",
        "diminutive": "UEL",
        "kind": KIND_C_CUP,
        "style": {
            "bg_color": "#ED722E",
            "font_color": "white",
            "border_color": "#D35400"
        }
    },
    "uefa_conference_league": {
        "label": "UEFA Conference League",
        "diminutive": "UECL",
        "kind": KIND_C_CUP,
        "style": {
            "bg_color": "#55BC39",
            "font_color": "white",
            "border_color": "#2E8B57"
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

    "Shots/onTarget Conversion Rate For",
 	"Shots/onTarget Conversion Rate Against",
 	"Shots/Goals Conversion Rate For",
 	"Shots/Goals Conversion Rate Against",
 	"onTarget/Goals Conversion Rate For",
 	"onTarget/Goals Conversion Rate Against",
]

TEAM_STATS_RANKINGS_PLOTTABLE = [
    "Attendance",
    "Points",
    "Goals For",
    "Goals Against",
    "Goals Diff",
    "Clean Sheets",
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