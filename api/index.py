import os
import sys

# Add the project root to the python path so imports work correctly
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Import the Flask application object
from app import app
