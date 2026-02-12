"""
Input Validator module for Phase 2 - User Input
Validates user choices against the database and constraints.
"""

import logging
from typing import List, Optional, Tuple, Dict, Any
import difflib

from phase1.database_setup import DatabaseManager
from phase2.models import UserInput
from phase2.config import FUZZY_MATCH_THRESHOLD, MAX_CITIES_SUGGESTIONS

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class InputValidator:
    """
    Validates user input and provides suggestions.
    """
    
    def __init__(self, db_manager: Optional[DatabaseManager] = None):
        """
        Initialize the InputValidator.
        
        Args:
            db_manager: DatabaseManager instance for city validation
        """
        self.db_manager = db_manager or DatabaseManager()
        self.available_cities: List[str] = []
        self.available_cuisines: List[str] = []
        self._refresh_data()
        
    def _refresh_data(self):
        """
        Fetch available cities and cuisines from the database.
        """
        try:
            self.db_manager.connect()
            self.available_cities = self.db_manager.get_cities()
            self.available_cuisines = self.db_manager.get_cuisines()
            self.db_manager.close()
            logger.info(f"Loaded {len(self.available_cities)} cities and {len(self.available_cuisines)} cuisines from database")
        except Exception as e:
            logger.error(f"Failed to load data from database: {e}")
            self.available_cities = []
            self.available_cuisines = []
            
    def validate_city(self, city: str) -> Tuple[bool, Optional[str], List[str]]:
        """
        Check if a city exists in the database.
        
        Args:
            city: City name to validate
            
        Returns:
            Tuple of (is_valid, exact_match, suggestions)
        """
        if not city:
            return False, None, []
            
        city_clean = city.strip().title()
        
        # Check for exact match
        if city_clean in self.available_cities:
            return True, city_clean, []
            
        # Fuzzy matching for suggestions
        suggestions = difflib.get_close_matches(
            city_clean, 
            self.available_cities, 
            n=MAX_CITIES_SUGGESTIONS, 
            cutoff=FUZZY_MATCH_THRESHOLD
        )
        
        return False, None, suggestions
        
    def validate_user_input(self, data: Dict[str, Any]) -> Tuple[Optional[UserInput], Optional[str]]:
        """
        Validate full user input using Pydantic and database checks.
        
        Args:
            data: Raw input dictionary
            
        Returns:
            Tuple of (UserInput object, error_message)
        """
        try:
            # 1. Basic type/format validation via Pydantic
            user_input = UserInput(**data)
            
            # 2. Domain validation (City existence)
            is_valid, matched_city, suggestions = self.validate_city(user_input.city)
            
            if not is_valid:
                error_msg = f"City '{user_input.city}' not found in database."
                if suggestions:
                    error_msg += f" Did you mean: {', '.join(suggestions)}?"
                return None, error_msg
                
            # Update city with standardized name
            user_input.city = matched_city
            
            return user_input, None
            
        except ValueError as e:
            return None, str(e)
        except Exception as e:
            logger.error(f"Unexpected validation error: {e}")
            return None, "An unexpected error occurred during validation."
