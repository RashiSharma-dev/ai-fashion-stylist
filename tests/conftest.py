"""Shared setup for all tests: lets tests import from src/ and find the data/ folder."""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Make "from color_recommender import ..." work, the same way it does in the app
sys.path.insert(0, os.path.join(ROOT, "src"))

# Our code opens files like "data/color_rules.json", so run from the project root
os.chdir(ROOT)
