"""
Unit tests for DataCleaner module - Simplified Version (No Pandas)
"""

import unittest

from phase1.data_cleaner import DataCleaner


class TestDataCleaner(unittest.TestCase):
    """
    Test cases for DataCleaner class
    """
    
    def setUp(self):
        """
        Set up test fixtures
        """
        # Create sample data with various issues
        self.sample_data = [
            {'name': 'Restaurant A', 'city': 'Mumbai', 'cuisines': 'Italian, Chinese', 'average_cost_for_two': 500, 'aggregate_rating': 4.5, 'votes': 100},
            {'name': 'Restaurant B', 'city': 'delhi', 'cuisines': 'Indian', 'average_cost_for_two': 1000, 'aggregate_rating': 3.8, 'votes': 50},
            {'name': 'Restaurant A', 'city': 'Mumbai', 'cuisines': 'Italian, Chinese', 'average_cost_for_two': 500, 'aggregate_rating': 4.5, 'votes': 100},  # Duplicate
            {'name': 'Restaurant C', 'city': 'Bangalore', 'cuisines': 'Mexican', 'average_cost_for_two': -100, 'aggregate_rating': 6.0, 'votes': 200},  # Invalid
            {'name': None, 'city': 'Chennai', 'cuisines': 'Thai', 'average_cost_for_two': 2000, 'aggregate_rating': 2.5, 'votes': -10}  # Missing name
        ]
    
    def test_remove_duplicates(self):
        """
        Test duplicate removal
        """
        cleaner = DataCleaner(self.sample_data)
        result = cleaner.remove_duplicates()
        
        # Should remove exact duplicate (Restaurant A in Mumbai)
        self.assertLess(len(result), len(self.sample_data))
        
        # Check cleaning report
        self.assertGreater(cleaner.cleaning_report['duplicates_removed'], 0)
    
    def test_handle_missing_values(self):
        """
        Test missing value handling
        """
        cleaner = DataCleaner(self.sample_data)
        result = cleaner.handle_missing_values()
        
        # Should drop rows with missing name
        for item in result:
            self.assertIsNotNone(item.get('name'))
            self.assertTrue(item.get('name'))
    
    def test_standardize_text_fields(self):
        """
        Test text field standardization
        """
        cleaner = DataCleaner(self.sample_data)
        result = cleaner.standardize_text_fields()
        
        # City names should be title case
        cities = [item['city'] for item in result]
        self.assertIn('Delhi', cities)
        self.assertNotIn('delhi', cities)
    
    def test_remove_invalid_entries(self):
        """
        Test removal of invalid entries
        """
        cleaner = DataCleaner(self.sample_data)
        result = cleaner.remove_invalid_entries()
        
        # Should remove negative prices
        for item in result:
            self.assertGreater(float(item.get('average_cost_for_two', 0)), 0)
        
        # Should remove invalid ratings (> 5.0)
        for item in result:
            rating = float(item.get('aggregate_rating', 0))
            self.assertLessEqual(rating, 5.0)
        
        # Should remove negative votes
        for item in result:
            self.assertGreaterEqual(int(item.get('votes', 0)), 0)
    
    def test_complete_cleaning_pipeline(self):
        """
        Test the complete cleaning pipeline
        """
        cleaner = DataCleaner(self.sample_data)
        result = cleaner.clean()
        
        # Should return a list
        self.assertIsInstance(result, list)
        
        # Should have fewer or equal records
        self.assertLessEqual(len(result), len(self.sample_data))
        
        # Should have cleaning report
        report = cleaner.get_cleaning_report()
        self.assertIn('original_records', report)
        self.assertIn('final_records', report)
    
    def test_cleaning_report(self):
        """
        Test cleaning report generation
        """
        cleaner = DataCleaner(self.sample_data)
        cleaner.clean()
        report = cleaner.get_cleaning_report()
        
        # Check report structure
        self.assertIn('original_records', report)
        self.assertIn('duplicates_removed', report)
        self.assertIn('missing_values_handled', report)
        self.assertIn('invalid_records_removed', report)
        self.assertIn('final_records', report)


class TestDataCleanerEdgeCases(unittest.TestCase):
    """
    Test edge cases for DataCleaner
    """
    
    def test_empty_list(self):
        """
        Test cleaning an empty list
        """
        empty_data = []
        cleaner = DataCleaner(empty_data)
        result = cleaner.clean()
        
        # Should handle empty list gracefully
        self.assertEqual(len(result), 0)
    
    def test_all_valid_data(self):
        """
        Test cleaning already clean data
        """
        clean_data = [
            {'name': 'Restaurant A', 'city': 'Mumbai', 'cuisines': 'Italian', 'average_cost_for_two': 500, 'aggregate_rating': 4.5, 'votes': 100},
            {'name': 'Restaurant B', 'city': 'Delhi', 'cuisines': 'Indian', 'average_cost_for_two': 1000, 'aggregate_rating': 3.8, 'votes': 50}
        ]
        
        cleaner = DataCleaner(clean_data)
        result = cleaner.clean()
        
        # Should retain all records
        self.assertEqual(len(result), len(clean_data))
    
    def test_all_duplicates(self):
        """
        Test list with all duplicate rows
        """
        duplicate_data = [
            {'name': 'Restaurant A', 'city': 'Mumbai', 'cuisines': 'Italian', 'average_cost_for_two': 500, 'aggregate_rating': 4.5, 'votes': 100},
            {'name': 'Restaurant A', 'city': 'Mumbai', 'cuisines': 'Italian', 'average_cost_for_two': 500, 'aggregate_rating': 4.5, 'votes': 100},
            {'name': 'Restaurant A', 'city': 'Mumbai', 'cuisines': 'Italian', 'average_cost_for_two': 500, 'aggregate_rating': 4.5, 'votes': 100},
        ]
        
        cleaner = DataCleaner(duplicate_data)
        result = cleaner.clean()
        
        # Should keep only one record
        self.assertEqual(len(result), 1)


if __name__ == '__main__':
    unittest.main()
