"""
Unit tests for DatabaseManager module - Simplified Version (No Pandas)
"""

import unittest
import sqlite3
from pathlib import Path
import tempfile
import os

from phase1.database_setup import DatabaseManager


class TestDatabaseManager(unittest.TestCase):
    """
    Test cases for DatabaseManager class
    """
    
    def setUp(self):
        """
        Set up test fixtures - use temporary database
        """
        # Create temporary database file
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db_path = Path(self.temp_db.name)
        self.temp_db.close()
        
        self.db_manager = DatabaseManager(db_path=self.temp_db_path)
        
        # Sample data for testing
        self.sample_data = [
            {'name': 'Restaurant A', 'city': 'Mumbai', 'cuisines': 'Italian', 'average_cost_for_two': 500, 'aggregate_rating': 4.5, 'votes': 100, 'price_category': 'budget', 'popularity_score': 0.8, 'cuisine_diversity': 1, 'has_online_delivery': 1, 'has_table_booking': 1, 'is_popular': 1},
            {'name': 'Restaurant B', 'city': 'Delhi', 'cuisines': 'Indian', 'average_cost_for_two': 1000, 'aggregate_rating': 3.8, 'votes': 50, 'price_category': 'mid-range', 'popularity_score': 0.6, 'cuisine_diversity': 1, 'has_online_delivery': 0, 'has_table_booking': 1, 'is_popular': 1},
            {'name': 'Restaurant C', 'city': 'Mumbai', 'cuisines': 'Chinese', 'average_cost_for_two': 1500, 'aggregate_rating': 4.2, 'votes': 200, 'price_category': 'premium', 'popularity_score': 0.9, 'cuisine_diversity': 1, 'has_online_delivery': 1, 'has_table_booking': 0, 'is_popular': 1}
        ]
    
    def tearDown(self):
        """
        Clean up test database
        """
        if self.db_manager.connection:
            self.db_manager.close()
        
        # Remove temporary database file
        if self.temp_db_path.exists():
            os.unlink(self.temp_db_path)
    
    def test_connect(self):
        """
        Test database connection
        """
        connection = self.db_manager.connect()
        
        # Should return a connection object
        self.assertIsInstance(connection, sqlite3.Connection)
        self.assertIsNotNone(self.db_manager.connection)
    
    def test_create_table(self):
        """
        Test table creation
        """
        self.db_manager.connect()
        self.db_manager.create_table()
        
        # Verify table exists
        cursor = self.db_manager.connection.cursor()
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
            (self.db_manager.table_name,)
        )
        result = cursor.fetchone()
        
        self.assertIsNotNone(result)
        self.assertEqual(result[0], self.db_manager.table_name)
    
    def test_create_indexes(self):
        """
        Test index creation
        """
        self.db_manager.connect()
        self.db_manager.create_table()
        self.db_manager.create_indexes()
        
        # Verify indexes exist
        cursor = self.db_manager.connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='index'")
        indexes = [row[0] for row in cursor.fetchall()]
        
        # Should have created indexes
        self.assertIn('idx_city', indexes)
        self.assertIn('idx_price', indexes)
        self.assertIn('idx_city_price', indexes)
    
    def test_insert_data(self):
        """
        Test data insertion
        """
        self.db_manager.connect()
        self.db_manager.create_table()
        self.db_manager.insert_data(self.sample_data, if_exists='replace')
        
        # Verify data was inserted
        count = self.db_manager.get_record_count()
        self.assertEqual(count, len(self.sample_data))
    
    def test_get_record_count(self):
        """
        Test getting record count
        """
        self.db_manager.connect()
        self.db_manager.create_table()
        self.db_manager.insert_data(self.sample_data)
        
        count = self.db_manager.get_record_count()
        self.assertEqual(count, 3)
    
    def test_get_cities(self):
        """
        Test getting unique cities
        """
        self.db_manager.connect()
        self.db_manager.create_table()
        self.db_manager.insert_data(self.sample_data)
        
        cities = self.db_manager.get_cities()
        
        # Should return unique cities
        self.assertIn('Mumbai', cities)
        self.assertIn('Delhi', cities)
        self.assertEqual(len(cities), 2)  # Mumbai and Delhi
    
    def test_get_sample_data(self):
        """
        Test getting sample data
        """
        self.db_manager.connect()
        self.db_manager.create_table()
        self.db_manager.insert_data(self.sample_data)
        
        sample = self.db_manager.get_sample_data(limit=2)
        
        # Should return list with limited records
        self.assertIsInstance(sample, list)
        self.assertEqual(len(sample), 2)
    
    def test_query_by_city(self):
        """
        Test querying by city
        """
        self.db_manager.connect()
        self.db_manager.create_table()
        self.db_manager.insert_data(self.sample_data)
        
        mumbai_restaurants = self.db_manager.query_by_city('Mumbai')
        
        # Should return only Mumbai restaurants
        self.assertEqual(len(mumbai_restaurants), 2)
        for restaurant in mumbai_restaurants:
            self.assertEqual(restaurant['city'], 'Mumbai')
    
    def test_query_by_city_and_price(self):
        """
        Test querying by city and price category
        """
        self.db_manager.connect()
        self.db_manager.create_table()
        self.db_manager.insert_data(self.sample_data)
        
        results = self.db_manager.query_by_city_and_price('Mumbai', 'budget')
        
        # Should return matching restaurants
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['name'], 'Restaurant A')
    
    def test_get_database_stats(self):
        """
        Test getting database statistics
        """
        self.db_manager.connect()
        self.db_manager.create_table()
        self.db_manager.insert_data(self.sample_data)
        
        stats = self.db_manager.get_database_stats()
        
        # Should return stats dictionary
        self.assertIn('total_records', stats)
        self.assertIn('cities', stats)
        self.assertIn('price_distribution', stats)
        self.assertEqual(stats['total_records'], 3)
    
    def test_close_connection(self):
        """
        Test closing database connection
        """
        self.db_manager.connect()
        self.db_manager.close()
        
        # Connection should be None after close
        self.assertIsNone(self.db_manager.connection)
        
        # Attempting to access connection should raise AttributeError
        with self.assertRaises(AttributeError):
            cursor = self.db_manager.connection.cursor()
            cursor.execute("SELECT 1")


class TestDatabaseManagerEdgeCases(unittest.TestCase):
    """
    Test edge cases for DatabaseManager
    """
    
    def setUp(self):
        """
        Set up test fixtures
        """
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db_path = Path(self.temp_db.name)
        self.temp_db.close()
        self.db_manager = DatabaseManager(db_path=self.temp_db_path)
    
    def tearDown(self):
        """
        Clean up
        """
        if self.db_manager.connection:
            self.db_manager.close()
        if self.temp_db_path.exists():
            os.unlink(self.temp_db_path)
    
    def test_empty_database(self):
        """
        Test operations on empty database
        """
        self.db_manager.connect()
        self.db_manager.create_table()
        
        count = self.db_manager.get_record_count()
        self.assertEqual(count, 0)
        
        cities = self.db_manager.get_cities()
        self.assertEqual(len(cities), 0)
    
    def test_query_nonexistent_city(self):
        """
        Test querying for a city that doesn't exist
        """
        self.db_manager.connect()
        self.db_manager.create_table()
        
        # Insert some data
        sample_data = [
            {'name': 'Restaurant A', 'city': 'Mumbai', 'cuisines': 'Italian', 'average_cost_for_two': 500, 'aggregate_rating': 4.5, 'votes': 100, 'price_category': 'budget', 'popularity_score': 0.8, 'cuisine_diversity': 1, 'has_online_delivery': 1, 'has_table_booking': 1, 'is_popular': 1}
        ]
        self.db_manager.insert_data(sample_data)
        
        # Query for non-existent city
        results = self.db_manager.query_by_city('NonExistentCity')
        self.assertEqual(len(results), 0)


if __name__ == '__main__':
    unittest.main()
