"""
Main entry point for Phase 2 - User Input Module.
"""

import logging
from phase2.cli import CommandLineInterface

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_user_preferences():
    """
    Initialize CLI and collect user preferences.
    
    Returns:
        UserInput object
    """
    cli = CommandLineInterface()
    return cli.run()

if __name__ == "__main__":
    get_user_preferences()
