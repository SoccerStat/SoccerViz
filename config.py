import os

APP_CONFIG = {
    'title': 'PostgreSQL Data Explorer',
    'icon': '🐘',
    'layout': 'wide'
}

DATABASE_CONFIG = {
    'default_host': os.getenv('DB_HOST', 'localhost'),
    'default_port': os.getenv('DB_PORT', '5432'),
    'default_database': os.getenv('DB_NAME', 'prd_soccersql'),
    'default_user': os.getenv('DB_USER', 'postgres')
}

CHART_CONFIG = {
    'color_palette': ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57'],
    'default_height': 400
}