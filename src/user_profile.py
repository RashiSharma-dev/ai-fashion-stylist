import json
import os

PROFILE_DIR = "data/profiles"


def _profile_path(name):
    os.makedirs(PROFILE_DIR, exist_ok=True)
    safe_name = name.strip().lower().replace(" ", "_")
    return os.path.join(PROFILE_DIR, f"{safe_name}.json")


def save_profile(name, data):
    path = _profile_path(name)
    with open(path, "w") as f:
        json.dump(data, f, indent=4)


def load_profile(name):
    path = _profile_path(name)
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return None
