import json
import os
from datetime import datetime

# Build an absolute path to data/profiles/analytics.json so it works
# no matter which folder we run the app from.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ANALYTICS_PATH = os.path.join(BASE_DIR, "data", "profiles", "analytics.json")


def _empty_analytics():
    """The starting shape of our stats (all zeros)."""
    return {
        "photos_analyzed": 0,
        "outfits_viewed": 0,
        "chat_messages_sent": 0,
        "color_counts": {},      # e.g. {"Navy Blue": 4, "Coral": 2}
        "occasion_counts": {},   # e.g. {"Casual": 3, "Party": 1}
        "last_updated": None,
    }


def load_analytics():
    """Read stats from disk. Returns {"error": None/"msg", "data": {...}}."""
    try:
        if not os.path.exists(ANALYTICS_PATH):
            return {"error": None, "data": _empty_analytics()}
        with open(ANALYTICS_PATH, "r", encoding="utf-8") as f:
            saved = json.load(f)
        data = _empty_analytics()
        data.update(saved)  # fills in any missing keys with defaults
        return {"error": None, "data": data}
    except (json.JSONDecodeError, OSError) as e:
        return {"error": f"Could not read analytics: {e}", "data": _empty_analytics()}


def _save_analytics(data):
    """Write stats to disk."""
    try:
        os.makedirs(os.path.dirname(ANALYTICS_PATH), exist_ok=True)
        data["last_updated"] = datetime.now().isoformat(timespec="seconds")
        with open(ANALYTICS_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        return {"error": None}
    except OSError as e:
        return {"error": f"Could not save analytics: {e}"}


def _bump(counter_dict, key):
    """Add 1 to counter_dict[key], creating it if it's new."""
    counter_dict[key] = counter_dict.get(key, 0) + 1


def log_event(event_type, value=None):
    """
    Record one user action.
    event_type: "photo_analyzed", "outfit_viewed", "chat_message",
                "color_recommended", "occasion_selected"
    value: only needed for the last two. For "color_recommended" it can be
           one color name or a list of color names.
    """
    data = load_analytics()["data"]

    if event_type == "photo_analyzed":
        data["photos_analyzed"] += 1
    elif event_type == "outfit_viewed":
        data["outfits_viewed"] += 1
    elif event_type == "chat_message":
        data["chat_messages_sent"] += 1
    elif event_type == "color_recommended":
        colors = value if isinstance(value, list) else [value]
        for color in colors:
            if color:
                _bump(data["color_counts"], str(color))
    elif event_type == "occasion_selected":
        if value:
            _bump(data["occasion_counts"], str(value))
    else:
        return {"error": f"Unknown event type: {event_type}"}

    return _save_analytics(data)


def get_top_colors(n=5):
    """Most recommended colors, highest first."""
    data = load_analytics()
    ranked = sorted(data["data"]["color_counts"].items(), key=lambda item: item[1], reverse=True)
    return {"error": data["error"], "colors": ranked[:n]}


def get_occasion_breakdown():
    """All occasions and how often each was used."""
    data = load_analytics()
    ranked = sorted(data["data"]["occasion_counts"].items(), key=lambda item: item[1], reverse=True)
    return {"error": data["error"], "occasions": ranked}
