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
    ANOMALY_DETECTION_PAGE,
    TEAM_STATS_PAGE,
    PLAYER_STATS_PAGE
]

ALL_BUTTON_CONFIG = {
    "id": "all",
    "label": "All",
    "style": {
            "bg_color": "#888888"
        }

}

COMPETITION_AND_COLORS = {
    "premier_league": {
        "label": "Premier League",
        "diminutive": "PL",
        "style": {
            "bg_color": "#6200EA"
        }
    },
    "la_liga": {
        "label": "La Liga",
        "diminutive": "LL",
        "style": {
             "bg_color": "#FBC02D"
        }
    },
    "fussball_bundesliga": {
        "label": "Bundesliga",
        "diminutive": "BL",
        "id_comp": "fussball_bundesliga",
        "style": {
            "bg_color": "#D32F2F"
        }
    },
    "serie_a": {
        "label": "Serie A",
        "diminutive": "SA",
        "style": {
            "bg_color": "#1976D2"
        }
    },
    "ligue_1": {
        "label": "Ligue 1",
        "diminutive": "L1",
        "style": {
            "bg_color": "#2E7D32"
        }
    },
    "uefa_champions_league": {
        "label": "Champions League",
        "diminutive": "UCL",
        "style": {
            "bg_color": "#0D47A1"
        }
    },
    "uefa_europa_league": {
        "label": "Europa League",
        "diminutive": "UEL",
        "style": {
            "bg_color": "#EF6C00"
        }
    },
    "uefa_conference_league": {
        "label": "Conference League",
        "diminutive": "UECL",
        "style": {
            "bg_color": "#388E3C"
        }
    }
}

START_SEASON = 2023
END_SEASON = 2025

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