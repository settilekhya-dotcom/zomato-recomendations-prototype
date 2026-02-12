import logging
from typing import List, Optional, Tuple, Any
from phase1.database_setup import DatabaseManager
from phase2.models import UserInput
from phase3.models import RestaurantRecommendation, RecommendationResponse

logger = logging.getLogger(__name__)

class RecommendationEngine:
    """
    Engine responsible for querying the database and ranking restaurant recommendations.
    """
    def __init__(self, db_manager: Optional[DatabaseManager] = None):
        """
        Initialize the engine.
        
        Args:
            db_manager: DatabaseManager instance for database operations.
        """
        self.db_manager = db_manager or DatabaseManager()

    def _calculate_match_score(self, rating: float, votes: int, user_input: UserInput, restaurant_cuisine: str) -> float:
        """
        Calculate a match score (0-10) for a restaurant based on user preferences.
        """
        quality_score: float = (float(rating) / 5.0) * 7.0
        popularity_score: float = (min(float(votes), 1000.0) / 1000.0) * 3.0
        
        score: float = quality_score + popularity_score
        
        # Check if any of the preferred cuisines match
        if user_input.cuisine:
            for cuisine in user_input.cuisine:
                if cuisine.lower() in restaurant_cuisine.lower():
                    score += 1.0
                    break # Only add bonus once
            
        return float(min(round(score, 2), 10.0))

    def get_recommendations(self, user_input: UserInput, limit: int = 5) -> RecommendationResponse:
        """
        Fetch and rank recommendations from the database.
        
        Args:
            user_input: Validated user preferences.
            limit: Maximum number of recommendations to return.
            
        Returns:
            RecommendationResponse object.
        """
        try:
            self.db_manager.connect()
            
            # Build query
            query = f"SELECT name, city, address, cuisines, average_cost_for_two, price_category, aggregate_rating, votes FROM {self.db_manager.table_name} WHERE city = ?"
            params: List[Any] = [user_input.city]
            
            # Filtering by price category
            query += " AND price_category = ?"
            params.append(user_input.price_range)
            
            # Filtering by min rating
            query += " AND aggregate_rating >= ?"
            params.append(user_input.min_rating)
            
            # Optional cuisine filter (SQL level for efficiency)
            if user_input.cuisine:
                cuisine_clauses = " OR ".join(["cuisines LIKE ?" for _ in user_input.cuisine])
                query += f" AND ({cuisine_clauses})"
                for c in user_input.cuisine:
                    params.append(f"%{c}%")
            
            # Sorting by rating and votes as a baseline
            query += " ORDER BY aggregate_rating DESC, votes DESC LIMIT 50" # Fetch more for scoring
            
            assert self.db_manager.connection is not None
            cursor = self.db_manager.connection.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            recommendations: List[RestaurantRecommendation] = []
            
            for row in rows:
                name, city, address, cuisines, avg_cost, price_cat, rating, votes = row
                
                match_score = self._calculate_match_score(rating, votes, user_input, cuisines)
                
                rec = RestaurantRecommendation(
                    name=name,
                    city=city,
                    address=address,
                    cuisines=cuisines,
                    average_cost=avg_cost,
                    price_category=price_cat,
                    rating=rating,
                    votes=votes,
                    match_score=match_score
                )
                recommendations.append(rec)
            
            # Re-sort by match score
            recommendations.sort(key=lambda x: x.match_score, reverse=True)
            
            # Apply limit
            final_recs = recommendations[:limit]
            
            logger.info(f"Found {len(final_recs)} recommendations for {user_input.city}")
            
            return RecommendationResponse(
                user_city=user_input.city,
                count=len(final_recs),
                recommendations=final_recs
            )
            
        except Exception as e:
            logger.error(f"Error getting recommendations: {e}")
            return RecommendationResponse(user_city=user_input.city, count=0, recommendations=[])
        finally:
            self.db_manager.close()
