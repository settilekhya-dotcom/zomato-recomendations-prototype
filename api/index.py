import os
import sys

# Ensure the root directory is in the python path so modules like 'phase2', 'phase6' can be imported
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from phase6.api_server import app
