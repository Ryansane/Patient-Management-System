import os
import sys
from importlib.machinery import SourceFileLoader

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
APP_PATH = os.path.join(ROOT_DIR, 'pms_app', 'RyanLevel5Hospital', 'app.py')

# Load the Flask app from a file path to avoid package import issues
module = SourceFileLoader('rl5h_app', APP_PATH).load_module()
app = getattr(module, 'app')

