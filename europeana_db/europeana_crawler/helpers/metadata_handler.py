import os
import json
from helpers.constants import LOG_FILE, JSON_DIR, CACHE_FILE


def load_existing_ids():
    """Load existing item IDs from the log file."""
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            return set(line.strip() for line in f.readlines())
    return set()


def save_ids_log(new_ids, is_precheck=False):
    """Save new item IDs to the log file."""
    existing_ids = load_existing_ids()
    new_ids_to_add = [item_id for item_id in new_ids if item_id not in existing_ids]

    if new_ids_to_add:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            for item_id in new_ids_to_add:
                f.write(f"{item_id}\n")

        if not is_precheck:  # Only print when new items are added in a normal run
            print(f"📝 Added {len(new_ids_to_add)} new item IDs to log.")

    return len(new_ids_to_add)


def save_metadata(item_id, data):
    """Save metadata as a JSON file."""
    safe_item_id = item_id.replace("/", "_") + ".json"
    file_path = os.path.join(JSON_DIR, safe_item_id)

    if os.path.exists(file_path):  # Prevent overwriting existing files
        return None

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    return file_path


def count_total_downloaded():
    """Count the total number of item IDs in the log file."""
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            return len(f.readlines())
    return 0


def load_cache():
    """Load cache file to get the total downloaded count."""
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"downloaded_count": 0}


def update_cache(new_files_count):
    """Update the cache file with the new total count."""
    cache = load_cache()
    cache["downloaded_count"] += new_files_count  # Only update with NEW items

    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=4)

    print(
        f"💾 Cache updated: Total downloaded count is now {cache['downloaded_count']}."
    )
