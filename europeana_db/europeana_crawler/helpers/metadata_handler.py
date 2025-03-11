import json
from os import makedirs
from os.path import exists, join

import aiofiles
from helpers.constants import CACHE_FILE, JSON_DIR, LOG_FILE, LOGS_DIR
from tqdm import tqdm


async def save_metadata(item_id, data, cursor):
    """Save metadata as a JSON file in the correct cursor folder asynchronously."""
    safe_item_id = item_id.replace("/", "_")
    safe_cursor = cursor.replace("/", "_")

    cursor_folder = join(JSON_DIR, safe_cursor)
    makedirs(cursor_folder, exist_ok=True)

    file_path = join(cursor_folder, f"{safe_item_id}.json")

    if exists(file_path):
        tqdm.write(f"⚠️ Item {item_id} already exists. Skipping save.")
        return None

    try:
        async with aiofiles.open(file_path, "w", encoding="utf-8") as f:
            await f.write(json.dumps(data, indent=4, ensure_ascii=False))

        return file_path
    except Exception as e:
        print(f"❌ ERROR: Failed to save metadata for `{item_id}`. Exception: {e}")
        return None


async def count_total_downloaded():
    """Asynchronously count the total number of item IDs in the log file."""
    if exists(LOG_FILE):
        count = 0
        async with aiofiles.open(LOG_FILE, "r", encoding="utf-8") as f:
            async for _ in f:  # Iterate over lines asynchronously
                count += 1
        return count
    return 0


async def load_cache(cursor):
    """Load the cache for a specific cursor asynchronously."""
    cache_file = join(LOGS_DIR, f"{cursor}_cache.json")
    if exists(cache_file):
        async with aiofiles.open(cache_file, "r", encoding="utf-8") as f:
            return json.loads(await f.read())
    return {"downloaded_count": 0, "item_ids": []}


async def update_cache(cursor, new_files_count):
    """Update the cache file with the new total count asynchronously."""
    cache = await load_cache(cursor)
    cache["downloaded_count"] += new_files_count  # Only update with NEW items

    async with aiofiles.open(CACHE_FILE, "w", encoding="utf-8") as f:
        await f.write(json.dumps(cache, indent=4))

    print(
        f"💾 Cache updated: Total downloaded count is now {cache['downloaded_count']}."
    )
