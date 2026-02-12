"""
Configuration module for Phase 1 - Zomato Data Pipeline
Contains all configuration parameters for data loading, processing, and storage.
"""

import os
from pathlib import Path

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent
PHASE1_ROOT = Path(__file__).parent

# Data directories
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
DATABASE_DIR = DATA_DIR / "database"

# Create directories if they don't exist
for directory in [DATA_DIR, RAW_DATA_DIR, PROCESSED_DATA_DIR, DATABASE_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Dataset configuration
DATASET_NAME = "ManikaSaini/zomato-restaurant-recommendation"
DATASET_SPLIT = "train"  # Default split to load

# Database configuration
DATABASE_PATH = DATABASE_DIR / "zomato.db"
DATABASE_TABLE_NAME = "restaurants"

# Data cleaning configuration
REQUIRED_COLUMNS = [
    "name",
    "city",
    "cuisines",
    "average_cost_for_two",
    "aggregate_rating",
    "votes"
]

# Price categories (in INR for average cost for two)
PRICE_CATEGORIES = {
    "budget": (0, 500),
    "mid-range": (500, 1500),
    "premium": (1500, float('inf'))
}

# Feature engineering configuration
MIN_VOTES_THRESHOLD = 10  # Minimum votes for a restaurant to be considered
MIN_RATING = 0.0
MAX_RATING = 5.0

# Logging configuration
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
