"""
Unit tests for DataLoader module - Simplified Version (No Pandas)
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
from datasets import Dataset

from phase1.data_loader import DataLoader


class TestDataLoader(unittest.TestCase):
    """
    Test cases for DataLoader class
    """
    
    def setUp(self):
        """
        Set up test fixtures
        """
        self.loader = DataLoader()
    
    @patch('phase1.data_loader.load_dataset')
    def test_load_dataset_success(self, mock_load_dataset):
        """
        Test successful dataset loading
        """
        # Mock dataset
        mock_data = {'train': Dataset.from_dict({'name': ['Restaurant A'], 'city': ['City A']})}
        mock_load_dataset.return_value = mock_data
        
        # Load dataset
        dataset = self.loader.load_dataset()
        
        # Assertions
        self.assertIsNotNone(dataset)
        mock_load_dataset.assert_called_once()
    
    @patch('phase1.data_loader.load_dataset')
    def test_load_dataset_with_different_split(self, mock_load_dataset):
        """
        Test loading dataset with non-existent split falls back to first available
        """
        # Mock dataset with only 'test' split
        mock_data = {'test': Dataset.from_dict({'name': ['Restaurant A'], 'city': ['City A']})}
        mock_load_dataset.return_value = mock_data
        
        # Load dataset (expecting 'train' but only 'test' exists)
        dataset = self.loader.load_dataset()
        
        # Should use first available split
        self.assertIsNotNone(dataset)
    
    def test_to_list_without_loading(self):
        """
        Test that to_list raises error if dataset not loaded
        """
        with self.assertRaises(ValueError):
            self.loader.to_list()
    
    @patch('phase1.data_loader.load_dataset')
    def test_to_list_success(self, mock_load_dataset):
        """
        Test successful conversion to list of dicts
        """
        # Mock dataset
        mock_data = {'train': Dataset.from_dict({
            'name': ['Restaurant A', 'Restaurant B'],
            'city': ['City A', 'City B']
        })}
        mock_load_dataset.return_value = mock_data
        
        # Load and convert
        self.loader.load_dataset()
        data = self.loader.to_list()
        
        # Assertions
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 2)
        self.assertIsInstance(data[0], dict)
        self.assertIn('name', data[0])
        self.assertIn('city', data[0])
    
    @patch('phase1.data_loader.load_dataset')
    def test_get_dataset_info(self, mock_load_dataset):
        """
        Test getting dataset information
        """
        # Mock dataset
        mock_data = {'train': Dataset.from_dict({
            'name': ['Restaurant A'],
            'city': ['City A'],
            'rating': [4.5]
        })}
        mock_load_dataset.return_value = mock_data
        
        # Load and get info
        self.loader.load_dataset()
        self.loader.to_list()
        info = self.loader.get_dataset_info()
        
        # Assertions
        self.assertIn('num_records', info)
        self.assertIn('num_columns', info)
        self.assertIn('columns', info)
        self.assertEqual(info['num_records'], 1)
        self.assertEqual(info['num_columns'], 3)
    
    @patch('phase1.data_loader.load_dataset')
    @patch('builtins.open', new_callable=lambda: MagicMock())
    def test_save_raw_data(self, mock_open, mock_load_dataset):
        """
        Test saving to CSV
        """
        # Mock dataset
        mock_data = {'train': Dataset.from_dict({
            'name': ['Restaurant A'],
            'city': ['City A']
        })}
        mock_load_dataset.return_value = mock_data
        
        # Load dataset
        self.loader.load_dataset()
        self.loader.to_list()
        
        # Save to CSV
        filepath = self.loader.save_raw_data('test.csv')
        
        # Verify open was called
        self.assertTrue(mock_open.called)


class TestDataLoaderEdgeCases(unittest.TestCase):
    """
    Test edge cases for DataLoader
    """
    
    @patch('phase1.data_loader.load_dataset')
    def test_empty_dataset(self, mock_load_dataset):
        """
        Test handling of empty dataset
        """
        # Mock empty dataset
        mock_data = {'train': Dataset.from_dict({'name': [], 'city': []})}
        mock_load_dataset.return_value = mock_data
        
        loader = DataLoader()
        loader.load_dataset()
        data = loader.to_list()
        
        # Should handle empty dataset gracefully
        self.assertEqual(len(data), 0)
    
    @patch('phase1.data_loader.load_dataset')
    def test_load_dataset_failure(self, mock_load_dataset):
        """
        Test handling of dataset loading failure
        """
        # Mock loading failure
        mock_load_dataset.side_effect = Exception("Network error")
        
        loader = DataLoader()
        
        # Should raise exception
        with self.assertRaises(Exception):
            loader.load_dataset()


if __name__ == '__main__':
    unittest.main()
