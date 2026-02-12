"""
Configuration constants for Phase 2 - User Input
"""

from phase1.config import DATABASE_PATH

# Price category numerical mappings (Average cost for two)
PRICE_CATEGORIES = {
    "budget": (0, 500),
    "mid-range": (500, 1500),
    "premium": (1500, float('inf'))
}

# Validation thresholds
MIN_RATING = 0.0
MAX_RATING = 5.0
MAX_CITIES_SUGGESTIONS = 3
FUZZY_MATCH_THRESHOLD = 0.6

# Default values
DEFAULT_TOP_N = 10
