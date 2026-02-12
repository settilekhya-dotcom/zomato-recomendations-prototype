"""
Unit tests for FeatureEngineer module - Simplified Version (No Pandas/Numpy)
"""

import unittest

from phase1.feature_engineer import FeatureEngineer


class TestFeatureEngineer(unittest.TestCase):
    """
    Test cases for FeatureEngineer class
    """
    
    def setUp(self):
        """
        Set up test fixtures
        """
        self.sample_data = [
            {'name': 'Restaurant A', 'city': 'Mumbai', 'cuisines': 'Italian, Chinese', 'average_cost_for_two': 400, 'aggregate_rating': 4.5, 'votes': 1000, 'online_order': 'Yes', 'book_table': 'Yes'},
            {'name': 'Restaurant B', 'city': 'Delhi', 'cuisines': 'Indian', 'average_cost_for_two': 1200, 'aggregate_rating': 3.8, 'votes': 50, 'online_order': 'No', 'book_table': 'Yes'},
            {'name': 'Restaurant C', 'city': 'Bangalore', 'cuisines': 'Mexican, Thai, Japanese', 'average_cost_for_two': 2000, 'aggregate_rating': 4.2, 'votes': 500, 'online_order': 'Yes', 'book_table': 'No'}
        ]
    
    def test_create_price_category(self):
        """
        Test price category creation
        """
        engineer = FeatureEngineer(self.sample_data)
        result = engineer.create_price_category()
        
        # Should create price_category field
        self.assertIn('price_category', result[0])
        
        # Check categorization
        self.assertEqual(result[0]['price_category'], 'budget')  # 400
        self.assertEqual(result[1]['price_category'], 'mid-range')  # 1200
        self.assertEqual(result[2]['price_category'], 'premium')  # 2000
    
    def test_create_popularity_score(self):
        """
        Test popularity score creation
        """
        engineer = FeatureEngineer(self.sample_data)
        result = engineer.create_popularity_score()
        
        # Should create popularity_score field
        self.assertIn('popularity_score', result[0])
        
        # Scores should be between 0 and 1
        for item in result:
            score = item['popularity_score']
            self.assertGreaterEqual(score, 0)
            self.assertLessEqual(score, 1)
        
        # Restaurant A (high rating + high votes) should have highest score
        scores = [item['popularity_score'] for item in result]
        max_score_idx = scores.index(max(scores))
        self.assertEqual(result[max_score_idx]['name'], 'Restaurant A')
    
    def test_create_cuisine_diversity_index(self):
        """
        Test cuisine diversity index creation
        """
        engineer = FeatureEngineer(self.sample_data)
        result = engineer.create_cuisine_diversity_index()
        
        # Should create cuisine_diversity field
        self.assertIn('cuisine_diversity', result[0])
        
        # Check counts
        self.assertEqual(result[0]['cuisine_diversity'], 2)  # Italian, Chinese
        self.assertEqual(result[1]['cuisine_diversity'], 1)  # Indian
        self.assertEqual(result[2]['cuisine_diversity'], 3)  # Mexican, Thai, Japanese
    
    def test_create_has_online_delivery(self):
        """
        Test online delivery feature creation
        """
        engineer = FeatureEngineer(self.sample_data)
        result = engineer.create_has_online_delivery()
        
        # Should create has_online_delivery field
        self.assertIn('has_online_delivery', result[0])
        
        # Check binary values
        self.assertEqual(result[0]['has_online_delivery'], 1)  # Yes
        self.assertEqual(result[1]['has_online_delivery'], 0)  # No
    
    def test_create_has_table_booking(self):
        """
        Test table booking feature creation
        """
        engineer = FeatureEngineer(self.sample_data)
        result = engineer.create_has_table_booking()
        
        # Should create has_table_booking field
        self.assertIn('has_table_booking', result[0])
        
        # Check binary values
        self.assertEqual(result[0]['has_table_booking'], 1)  # Yes
        self.assertEqual(result[2]['has_table_booking'], 0)  # No
    
    def test_create_is_popular(self):
        """
        Test is_popular feature creation
        """
        engineer = FeatureEngineer(self.sample_data)
        result = engineer.create_is_popular()
        
        # Should create is_popular field
        self.assertIn('is_popular', result[0])
        
        # Check based on MIN_VOTES_THRESHOLD (default 10)
        # Restaurant A (1000 votes) and C (500 votes) should be popular
        self.assertEqual(result[0]['is_popular'], 1)
        self.assertEqual(result[2]['is_popular'], 1)
    
    def test_complete_feature_engineering_pipeline(self):
        """
        Test the complete feature engineering pipeline
        """
        engineer = FeatureEngineer(self.sample_data)
        result = engineer.engineer_features()
        
        # Should create all feature fields
        expected_features = [
            'price_category',
            'popularity_score',
            'cuisine_diversity',
            'has_online_delivery',
            'has_table_booking',
            'is_popular'
        ]
        
        for feature in expected_features:
            self.assertIn(feature, result[0])
    
    def test_get_feature_summary(self):
        """
        Test feature summary generation
        """
        engineer = FeatureEngineer(self.sample_data)
        engineer.engineer_features()
        summary = engineer.get_feature_summary()
        
        # Should return a dictionary with feature summaries
        self.assertIsInstance(summary, dict)
        self.assertIn('price_category', summary)
        self.assertIn('popularity_score', summary)


class TestFeatureEngineerEdgeCases(unittest.TestCase):
    """
    Test edge cases for FeatureEngineer
    """
    
    def test_missing_columns(self):
        """
        Test handling of missing columns
        """
        # Data without optional columns
        minimal_data = [
            {'name': 'Restaurant A', 'city': 'Mumbai'}
        ]
        
        engineer = FeatureEngineer(minimal_data)
        result = engineer.engineer_features()
        
        # Should handle gracefully without errors
        self.assertIsInstance(result, list)
    
    def test_unknown_cuisines(self):
        """
        Test handling of unknown/missing cuisines
        """
        data_with_unknown = [
            {'name': 'Restaurant A', 'city': 'Mumbai', 'cuisines': 'Unknown', 'average_cost_for_two': 500, 'aggregate_rating': 4.5, 'votes': 100},
            {'name': 'Restaurant B', 'city': 'Delhi', 'cuisines': None, 'average_cost_for_two': 1000, 'aggregate_rating': 3.8, 'votes': 50}
        ]
        
        engineer = FeatureEngineer(data_with_unknown)
        result = engineer.create_cuisine_diversity_index()
        
        # Unknown cuisines should have diversity of 0
        self.assertEqual(result[0]['cuisine_diversity'], 0)
    
    def test_zero_votes(self):
        """
        Test handling of restaurants with zero votes
        """
        data_with_zero_votes = [
            {'name': 'Restaurant A', 'city': 'Mumbai', 'average_cost_for_two': 500, 'aggregate_rating': 4.5, 'votes': 0}
        ]
        
        engineer = FeatureEngineer(data_with_zero_votes)
        result = engineer.create_popularity_score()
        
        # Should handle zero votes without errors
        self.assertIn('popularity_score', result[0])
        self.assertGreaterEqual(result[0]['popularity_score'], 0)


if __name__ == '__main__':
    unittest.main()
