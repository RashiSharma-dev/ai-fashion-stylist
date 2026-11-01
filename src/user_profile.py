# src/user_profile.py
import json
import os
import re

PROFILE_DIR = "data/profiles"


def _profile_path(name):
    """
    Return the file path where a user's profile is saved, or None if the name has no usable characters.

    Creates the profiles folder if it doesn't exist. The name is turned into a safe
    file name: lowercase, spaces become underscores, and everything except letters,
    digits, underscores and hyphens is removed. This blocks tricks like "../../x"
    that would save a file outside the profiles folder.
    """
    os.makedirs(PROFILE_DIR, exist_ok=True)
    cleaned_name = name.strip().lower().replace(" ", "_")
    safe_name = re.sub(r"[^\w-]", "", cleaned_name)[:50]
    if not safe_name:
        return None
    return os.path.join(PROFILE_DIR, f"{safe_name}.json")


def save_profile(name, data):
    """Save a user's profile (a dict of their latest search settings) as a JSON file. Does nothing if the name is unusable."""
    path = _profile_path(name)
    if path is None:
        return
    with open(path, "w") as f:
        json.dump(data, f, indent=4)


def load_profile(name):
    """Load a user's saved profile as a dict, or return None if they don't have one yet."""
    path = _profile_path(name)
    if path is not None and os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return None