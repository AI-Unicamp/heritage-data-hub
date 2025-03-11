import json
from os import makedirs
from os.path import exists, join

from helpers.constants import CACHE_FILE, LOGS_DIR


def load_cache():
    """Load global cache tracking all cursor IDs."""
    if not exists(CACHE_FILE):
        return {"cursor_count": 0, "cursors": [], "total_items": 0, "next_cursor": None}

    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        cache = json.load(f)

    cache.setdefault("cursor_count", 0)
    cache.setdefault("cursors", [])
    cache.setdefault("total_items", 0)
    cache.setdefault("next_cursor", None)

    return cache


def save_cache(cache_data, new_cursor=None, next_cursor=None):
    """Save global execution cache (tracking cursors and metadata)."""
    makedirs(LOGS_DIR, exist_ok=True)

    cache_data.setdefault("cursor_count", 0)
    cache_data.setdefault("cursors", [])
    cache_data.setdefault("total_items", 0)
    cache_data.setdefault("next_cursor", None)
    cache_data.setdefault("last_cursor", None)

    # Add new cursor to history if it's not already tracked
    if new_cursor and new_cursor not in cache_data["cursors"]:
        cache_data["cursors"].append(new_cursor)

    # Store the last processed cursor, only if it is valid and not "*"
    if new_cursor and new_cursor not in ["*", None]:
        cache_data["last_cursor"] = new_cursor

    # Update next cursor, only if it’s different from the last one
    if next_cursor and next_cursor != cache_data["next_cursor"]:
        cache_data["next_cursor"] = next_cursor
        print(f"💾 Updating next cursor: {next_cursor[:8]}...")

    cache_file = join(LOGS_DIR, "cache.json")
    with open(cache_file, "w", encoding="utf-8") as f:
        json.dump(cache_data, f, indent=4)
