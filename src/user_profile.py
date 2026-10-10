# src/user_profile.py
import json
import os

PROFILE_DIR = "data/profiles"


def _profile_path(name):
    """
    Return the file path where a user's profile is saved.

    Creates the profiles folder if it doesn't exist, and turns the name into
    a safe file name (lowercase, spaces replaced with underscores).
    """
    os.makedirs(PROFILE_DIR, exist_ok=True)
    safe_name = name.strip().lower().replace(" ", "_")
    return os.path.join(PROFILE_DIR, f"{safe_name}.json")


def save_profile(name, data):
    """Save a user's profile (a dict of their latest search settings) as a JSON file."""
    path = _profile_path(name)
    with open(path, "w") as f:
        json.dump(data, f, indent=4)


def load_profile(name):
    """Load a user's saved profile as a dict, or return None if they don't have one yet."""
    path = _profile_path(name)
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return None
