import os
import sys

# Ensure the root directory is in the python path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from phase6.api_server import app

# For Vercel, the 'app' variable needs to be available at the top level
# of the entrypoint file.
