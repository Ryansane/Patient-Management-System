import os
import sys

# Ensure project root is on sys.path so 'pms_app' can be imported
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from pms_app.RyanLevel5Hospital.app import app  # WSGI callable

