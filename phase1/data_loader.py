"""
Data Loader module for Phase 1 - Simplified Version (No Pandas)
Loads the Zomato dataset from Hugging Face using only standard library.
"""

import logging
import csv
from typing import Optional, Dict, Any, List

from datasets import load_dataset, Dataset

from phase1.config import DATASET_NAME, DATASET_SPLIT, RAW_DATA_DIR

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataLoader:
    """
    Loads and manages the Zomato restaurant dataset from Hugging Face.
    Uses standard library instead of pandas.
    """
    
    def __init__(self, dataset_name: str = DATASET_NAME, split: str = DATASET_SPLIT):
        """
        Initialize the DataLoader.
        
        Args:
            dataset_name: Name of the dataset on Hugging Face
            split: Dataset split to load (train, test, etc.)
        """
        self.dataset_name = dataset_name
        self.split = split
        self.dataset: Optional[Dataset] = None
        self.data: List[Dict[str, Any]] = []
    
    def load_dataset(self) -> Dataset:
        """
        Load the dataset from Hugging Face.
        
        Returns:
            Dataset object from Hugging Face
            
        Raises:
            Exception: If dataset loading fails
        """
        try:
            logger.info(f"Loading dataset: {self.dataset_name}, split: {self.split}")
            ds = load_dataset(self.dataset_name)
            
            # Get the specified split or the first available split
            if self.split in ds:
                self.dataset = ds[self.split]
            else:
                available_splits = list(ds.keys())
                logger.warning(
                    f"Split '{self.split}' not found. Available splits: {available_splits}. "
                    f"Using first available split: {available_splits[0]}"
                )
                self.dataset = ds[available_splits[0]]
            
            if self.dataset is not None:
                logger.info(f"Dataset loaded successfully. Total records: {len(self.dataset)}")
            return self.dataset
            
        except Exception as e:
            logger.error(f"Failed to load dataset: {str(e)}")
            raise
    
    def to_list(self) -> List[Dict[str, Any]]:
        """
        Convert the Hugging Face Dataset to a list of dictionaries with column mapping.
        
        Returns:
            List of dictionaries containing the dataset
            
        Raises:
            ValueError: If dataset hasn't been loaded yet
        """
        if self.dataset is None:
            raise ValueError("Dataset not loaded. Call load_dataset() first.")
        
        logger.info("Converting dataset to list of dictionaries with column mapping")
        self.data = []
        
        # Column mapping from Hugging Face dataset to our internal format
        # Features: ['url', 'address', 'name', 'online_order', 'book_table', 'rate', 'votes', 
        #           'phone', 'location', 'rest_type', 'dish_liked', 'cuisines', 
        #           'approx_cost(for two people)', 'reviews_list', 'menu_item', 
        #           'listed_in(type)', 'listed_in(city)']
        mapping = {
            "listed_in(city)": "city",
            "approx_cost(for two people)": "average_cost_for_two",
            "rate": "aggregate_rating",
            "online_order": "online_order",
            "book_table": "book_table"
        }
        
        # Convert dataset to list of dicts with mapping
        dataset = self.dataset
        assert dataset is not None  # Type hint for IDE
        for item in dataset:
            mapped_item = dict(item)
            
            # Apply mapping
            for raw_col, target_col in mapping.items():
                if raw_col in mapped_item:
                    mapped_item[target_col] = mapped_item.pop(raw_col)
            
            self.data.append(mapped_item)
        
        logger.info(f"Converted {len(self.data)} records with mapping")
        return self.data
    
    def get_dataset_info(self) -> Dict[str, Any]:
        """
        Get information about the loaded dataset.
        
        Returns:
            Dictionary containing dataset information
        """
        if not self.data:
            raise ValueError("Data not converted. Call to_list() first.")
        
        # Get column names from first record
        columns = list(self.data[0].keys()) if self.data else []
        
        info = {
            "num_records": len(self.data),
            "num_columns": len(columns),
            "columns": columns
        }
        
        return info
    
    def save_raw_data(self, filename: str = "raw_data.csv") -> str:
        """
        Save the raw dataset to a CSV file.
        
        Args:
            filename: Name of the file to save
            
        Returns:
            Path to the saved file
        """
        if not self.data:
            raise ValueError("Data not converted. Call to_list() first.")
        
        filepath = RAW_DATA_DIR / filename
        logger.info(f"Saving raw data to: {filepath}")
        
        # Get all column names
        if not self.data:
            logger.warning("No data to save")
            return str(filepath)
        
        columns = list(self.data[0].keys())
        
        # Write to CSV
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=columns)
            writer.writeheader()
            writer.writerows(self.data)
        
        logger.info("Raw data saved successfully")
        return str(filepath)
    
    def load_from_csv(self, filepath: str) -> List[Dict[str, Any]]:
        """
        Load data from a CSV file.
        
        Args:
            filepath: Path to the CSV file
            
        Returns:
            List of dictionaries
        """
        logger.info(f"Loading data from CSV: {filepath}")
        self.data = []
        
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.data.append(dict(row))
        
        logger.info(f"Data loaded successfully. Records: {len(self.data)}")
        return self.data


def main():
    """
    Main function to demonstrate data loading.
    """
    loader = DataLoader()
    
    # Load dataset
    dataset = loader.load_dataset()
    
    # Convert to list
    data = loader.to_list()
    
    # Get dataset info
    info = loader.get_dataset_info()
    logger.info(f"Dataset Info: {info}")
    
    # Save raw data
    filepath = loader.save_raw_data()
    logger.info(f"Raw data saved to: {filepath}")


if __name__ == "__main__":
    main()
