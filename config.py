# Configuration settings for the TV Shows Dashboard

# Data settings
EPISODE_THRESHOLD = 20  # Maximum episodes to consider as "one season"
DATA_FILES = {
    'basics': 'title.basics.tsv',
    'episodes': 'title.episode.tsv'
}

# Visualization settings
COLOR_PALETTES = {
    'primary': 'viridis',
    'secondary': 'pastel',
    'accent': 'magma',
    'cool': 'coolwarm'
}

# Layout settings
PAGE_CONFIG = {
    'page_title': 'TV Shows Analysis Dashboard',
    'page_icon': '📺',
    'layout': 'wide',
    'initial_sidebar_state': 'expanded'
}

# Chart settings
CHART_CONFIG = {
    'figure_size': (12, 6),
    'dpi': 100,
    'style': 'whitegrid'
}

# Data processing settings
NULL_VALUES = ['\\N', 'N/A', '', ' ']
NUMERIC_COLUMNS = ['startYear', 'endYear', 'runtimeMinutes']
