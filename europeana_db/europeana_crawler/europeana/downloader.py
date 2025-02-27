from concurrent.futures import ThreadPoolExecutor
import json
import os
from tqdm import tqdm
from europeana.api import fetch_item_ids, fetch_item_metadata, load_cursor, save_cursor
from helpers.constants import BATCH_SIZE, JSON_DIR, LOG_FILE, CACHE_FILE


def load_existing_ids():
    """Load existing item IDs from the log file to avoid duplicates."""
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            return set(line.strip() for line in f.readlines())
    return set()


def load_cache():
    """Load cache from JSON file, ensuring `item_ids` is always a list."""
    if not os.path.exists(CACHE_FILE):
        return {"downloaded_count": 0, "item_ids": []}  # ✅ Ensure it's a list

    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        cache = json.load(f)

    # ✅ Ensure `item_ids` is a list before returning
    if "item_ids" not in cache:
        cache["item_ids"] = []
    elif isinstance(cache["item_ids"], set):
        cache["item_ids"] = list(cache["item_ids"])

    return cache


def save_cache(cache_data):
    """Ensure item_ids is converted to a list before saving."""
    cache_data["item_ids"] = list(cache_data.get("item_ids", []))  # ✅ Convert to list
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache_data, f, indent=4)


def save_ids_log(downloaded_ids):
    """Append only successfully downloaded item IDs to the log file."""
    cache = load_cache()  # Load cache from file
    existing_ids = set(load_existing_ids())  # Convert existing IDs to a set
    new_ids = [item_id for item_id in downloaded_ids if item_id not in existing_ids]

    if new_ids:
        # Append to ids.log
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            for item_id in new_ids:
                f.write(f"{item_id}\n")
        print(f"📝 Added {len(new_ids)} new item IDs to log.")

        # ✅ Ensure item_ids is stored as a **list**
        if "item_ids" not in cache:
            cache["item_ids"] = []  # Initialize if missing
        elif isinstance(cache["item_ids"], set):
            cache["item_ids"] = list(cache["item_ids"])  # Convert to list if it's a set

        cache["item_ids"].extend(new_ids)  # ✅ Use .extend() for lists
        save_cache(cache)  # Persist changes

    else:
        print("✅ No new IDs to add. Skipping log update.")


def item_json_exists(item_id):
    """Check if the JSON metadata file for an item already exists."""
    safe_item_id = item_id.replace("/", "_")
    file_path = os.path.join(JSON_DIR, f"{safe_item_id}.json")
    return os.path.exists(file_path)


def save_metadata(item_id, data):
    """Save metadata as a JSON file only if it doesn't already exist."""
    safe_item_id = item_id.replace("/", "_")
    file_path = os.path.join(JSON_DIR, f"{safe_item_id}.json")

    if os.path.exists(file_path):
        tqdm.write(f"⚠️ Item {item_id} already exists in JSON folder. Skipping save.")
        return None

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    return file_path  # Return file path for counting


def fetch_and_save(item_id):
    """Fetch metadata and save it."""
    metadata = fetch_item_metadata(item_id)
    if metadata:
        return save_metadata(item_id, metadata)
    return None


def collect_data(limit=10, force_download=False):
    """Ensure dataset consistency first, re-download missing JSON files, then fetch more items."""

    cursor = None if force_download else load_cursor() or "*"

    if not os.listdir(JSON_DIR):  # If the JSON directory is empty
        print("⚠️ Data folder is empty! Resetting cache...")
        cache = {"downloaded_count": 0, "item_ids": []}  # ✅ Use list instead of set
        save_cache(cache)  # Ensure it's saved immediately
    saved_files = []
    downloaded_ids = []  # Track only IDs of successfully downloaded files

    # Load cache to see total downloaded count & stored IDs
    cache = load_cache()
    cached_ids = set(cache.get("item_ids", []))  # Get stored IDs
    existing_ids = load_existing_ids()
    total_downloaded = cache["downloaded_count"]

    print("\n🛠️ **Pre-Download Check: Ensuring dataset consistency...**")

    items, cursor = fetch_item_ids(cursor)  # Now fetch_item_ids() always returns a list
    if not items:  # Ensure items is not empty
        print("✅ No new items found in API response. Stopping download.")
        return

    json_files = set(os.listdir(JSON_DIR))  # Check JSON files in storage

    missing_log_entries = 0
    missing_json_items = []
    missing_in_log = []

    # Step 1: Fix missing logs & detect missing JSON files
    all_logged_and_cached_ids = existing_ids | cached_ids  # Combine both sets

    for item_id in all_logged_and_cached_ids:
        safe_item_id = item_id.replace("/", "_") + ".json"
        json_exists = safe_item_id in json_files
        log_exists = item_id in existing_ids

        # Fix missing log entries (if JSON exists but ID is missing from log)
        if json_exists and not log_exists:
            missing_in_log.append(item_id)
            downloaded_ids.append(item_id)
            missing_log_entries += 1

        # If JSON is missing but in cache/logs, mark it for re-download
        if not json_exists and item_id in cached_ids:
            missing_json_items.append(item_id)

    total_log_count = len(existing_ids)  # Define total_log_count before condition

    # Display missing log entries if any exist
    if missing_in_log:
        print(f"🔸 **{len(missing_in_log)} missing item(s) found in `ids.log`.**")
        print("❌ **Missing Log IDs:**")
        for item_id in missing_in_log:
            print(f"      - {item_id}")
        print("\n🛠️ Fixing missing IDs in `ids.log`...\n")

        save_ids_log(
            set(missing_in_log) | (cached_ids - existing_ids)
        )  # Ensure all types are sets

        json_files = set(os.listdir(JSON_DIR))  # Re-check JSON files after re-download
        total_json_count = len(json_files)

        print(f"✅ Finished re-adding {len(missing_in_log)} missing IDs to `ids.log`.")
        print(f"📊 **Total items in `ids.log` now: {total_log_count}**\n")
    else:
        total_log_count = len(existing_ids)
        print(f"✅ IDs log is ok. No new IDs to add. Skipping log update.")
        print(f"📊 **Total items in `ids.log` now: {total_log_count}**\n")

    # Step 2: Detect and print missing JSON files before downloading
    if missing_json_items:
        print(f"🔸 **{len(missing_json_items)} missing JSON file(s) detected.**")
        print("❌ **Missing JSON file IDs:**")
        for item_id in missing_json_items:
            print(f"      - {item_id}")
        print("\n🛠️ Re-downloading missing JSON files...")

        with ThreadPoolExecutor(max_workers=5) as executor:
            results = list(
                tqdm(
                    executor.map(fetch_and_save, missing_json_items),
                    total=len(missing_json_items),
                    desc="🔄 Fetching missing metadata...",
                    ncols=80,
                    ascii=" ░▒▓█",
                )
            )

        saved_files = [file for file in results if file]

        total_json_count = len(os.listdir(JSON_DIR))  # Updated JSON file count
        print(f"✅ Finished re-downloading {len(saved_files)} JSON files.")
        print(f"📊 **Total items in the `json` folder now: {total_json_count}**\n")
    else:
        total_json_count = len(json_files)
        print(f"✅ JSON files are up-to-date. No missing files detected.")
        print(f"📊 **Total items in the `json` folder now: {total_json_count}**\n")

    # Step 3: Ask the user before downloading the first batch
    first_run = True  # Track if it's the first batch

    cursor = load_cursor()  # Load previous cursor if exists

    while True:
        if first_run and limit is not None:
            user_input = (
                input("\n🔹 Do you want to download more new items? (yes/no): ")
                .strip()
                .lower()
            )
            download_more = user_input in ["yes", "y"]
            if not download_more:
                print(
                    f"✅ No new downloads requested. **Total items downloaded (tracked in cache): {total_downloaded}**\n"
                )
                return

        print("\n🔍 Fetching new items...")

        items, next_cursor = fetch_item_ids(cursor)  # Fetch new items using pagination
        if not items:
            print("✅ No more new items found. Stopping download.")
            return
        cursor = next_cursor  # ✅ Ensure cursor is updated
        new_download_items = [
            item["id"]
            for item in items
            if "id" in item
            and item["id"] not in existing_ids
            and item["id"] not in cached_ids
        ]

        if not new_download_items:
            print("✅ No new items available for download.")
            return

        # Apply batch size: BATCH_SIZE for --all, otherwise use limit
        batch_size = BATCH_SIZE if limit is None else limit
        new_download_items = new_download_items[:batch_size]

        print(
            f"🚀 Fetching metadata for **{len(new_download_items)}** new items in parallel...\n"
        )

        # Step 4: Fetch new items in parallel
        downloaded_ids = []  # Reset this list to track only new downloads

        with ThreadPoolExecutor(max_workers=5) as executor:
            results = list(
                tqdm(
                    executor.map(fetch_and_save, new_download_items),
                    total=len(new_download_items),
                    desc="🚀 Fetching new metadata...",
                    ncols=80,
                    ascii=" ░▒▓█",
                )
            )

        saved_files = [file for file in results if file]
        downloaded_ids.extend(
            [item_id for item_id, result in zip(new_download_items, results) if result]
        )

        # ✅ Log new downloaded IDs
        save_ids_log(downloaded_ids)

        # ✅ Step 5: Properly Update Cache
        cache["downloaded_count"] += len(downloaded_ids)  # ✅ Increment count
        cache["item_ids"] = list(
            set(cache.get("item_ids", [])) | set(downloaded_ids)
        )  # ✅ Merge and ensure a list
        save_cache(cache)  # ✅ Save immediately after update

        print(f"✅ Finished fetching metadata for **{len(saved_files)}** new items!")
        print(
            f"📊 **Total items downloaded so far (tracked in cache): {cache['downloaded_count']}**\n"
        )

        # ✅ Save the cursor after a successful batch fetch
        if next_cursor:
            save_cursor(next_cursor)  # ✅ Save the next cursor
            cursor = next_cursor  # ✅ Update the cursor for the next fetch
        else:
            print("✅ No more items to fetch.")
            return
