import os

APP_CONFIG = {
    'title': 'PostgreSQL Data Explorer',
    'icon': '⚽️',
    'layout': 'wide'
}

PAGES_CONFIG = [
    "Basic Stats",
    "Monitoring",
    "Anomaly Detection",
    "Team Stats",
    "Player Stats"
]

COMPETITION_AND_COLORS = {
    "All": "#888888",
    "Premier League": "#6200EA",
    "La Liga": "#FBC02D",
    "Buli": "#D32F2F",
    "Serie A": "#1976D2",
    "Ligue 1": "#2E7D32",
    "Champions League": "#0D47A1",
    "Europa League": "#EF6C00",
    "Conference League": "#388E3C"
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