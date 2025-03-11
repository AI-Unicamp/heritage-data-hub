import asyncio
import json
import time
from os import makedirs, walk
from os.path import exists, join

import aiohttp
from europeana.api import fetch_item_ids, fetch_item_metadata, load_cursor
from helpers.cache_handler import load_cache, save_cache
from helpers.constants import ANALYSIS_LOG, JSON_DIR, LOGS_DIR, MAX_CONCURRENT_REQUESTS
from helpers.metadata_handler import save_metadata
from helpers.mongo_handler import collection, insert_bulk_metadata


def save_cursor_cache(cursor, cursor_cache):
    """Save cache for each cursor separately."""
    makedirs(LOGS_DIR, exist_ok=True)
    safe_cursor = cursor.replace("/", "_")
    cache_file = join(LOGS_DIR, f"{safe_cursor}_cache.json")

    with open(cache_file, "w", encoding="utf-8") as f:
        json.dump(cursor_cache, f, indent=4)

    print(f"💾 Cursor cache saved: {cache_file}")


async def fetch_and_save(session, item_id, cursor):
    """Fetch metadata and save both locally and return for batch MongoDB insertion."""
    metadata = await fetch_item_metadata(session, item_id)

    if not metadata:
        print(f"⚠️ No metadata returned for `{item_id}`. Skipping.")

        return None

    # First, save locally as JSON
    await save_metadata(item_id, metadata, cursor)

    # Return metadata and its item_id (to be used as _id in MongoDB)
    return metadata, item_id


def get_mongo_count():
    """Return the total count of items in MongoDB."""

    return collection.count_documents({})


def get_local_count():
    """Return the total count of JSON files stored locally."""
    json_files = sum(len(files) for _, _, files in walk(JSON_DIR))

    return json_files


async def collect_data(limit: int | None = None, force_download: bool = False):
    """Ensure dataset consistency, re-download missing JSON files, and fetch new items asynchronously."""
    start_time = time.time()

    cache = load_cache()
    cursor = None if force_download else load_cursor()
    total_downloaded_session = 0

    async with aiohttp.ClientSession() as session:
        # await retry_failed_requests(session)  # Retry previous failures first
        while cursor:
            print(f"\n🔹 Processing batch from cursor `{cursor}`...")
            print(
                f"🔄 Retry Cursor → `{cursor}` (Restart will begin here if interrupted)\n"
            )

            # Save last_cursor in cache before downloading
            cache["last_cursor"] = cursor
            save_cache(cache)

            safe_cursor = cursor.replace("/", "_")

            cursor_cache_file = join(LOGS_DIR, f"{safe_cursor}_cache.json")
            cursor_cache = {"downloaded_count": 0, "item_ids": []}

            if exists(cursor_cache_file):
                with open(cursor_cache_file, "r", encoding="utf-8") as f:
                    cursor_cache = json.load(f)

            cursor_dir = join(JSON_DIR, safe_cursor)
            makedirs(cursor_dir, exist_ok=True)

            if limit is not None and total_downloaded_session >= limit:
                print(f"🛑 Download limit of {limit} reached. Stopping.")
                break

            # Fetch items, next cursor, and total items count
            items, next_cursor, total_items_for_cursor = await fetch_item_ids(
                session, cursor
            )

            # Ensure `total_available_items` is updated, only if it increases
            if total_items_for_cursor is not None:
                if (
                    cache.get("total_available_items") is None
                    or cache["total_available_items"] < total_items_for_cursor
                ):
                    cache["total_available_items"] = total_items_for_cursor
                    save_cache(cache)
                    print(f"💾 Total available items → {total_items_for_cursor}")

            # Handle API errors or empty results
            if items is None:
                print(f"⚠️ ERROR: `fetch_item_ids({cursor})` returned None. Stopping.")
                break

            if not items:
                print(f"⚠️ `{cursor}`: No items retrieved from API. Investigate why.")
                cursor = next_cursor
                continue

            # Filter out already downloaded items
            already_downloaded = set(cursor_cache.get("item_ids", []))
            new_download_items = [
                item["id"]
                for item in items
                if "id" in item and item["id"] not in already_downloaded
            ]

            print(f"🔍 After filtering, {len(new_download_items)} new items remain.")

            if not new_download_items:
                print(f"✅ `{cursor}`: All items already downloaded. Skipping.")
                cursor = next_cursor
                continue

            if limit is not None:
                remaining_limit = limit - total_downloaded_session
                new_download_items = new_download_items[:remaining_limit]

            print(f"🚀 `{cursor}`: Downloading {len(new_download_items)} new items...")

            # Process items in batches to limit concurrent API requests
            all_downloaded_metadata = []
            all_downloaded_ids = []

            for i in range(0, len(new_download_items), MAX_CONCURRENT_REQUESTS):
                batch = new_download_items[i : i + MAX_CONCURRENT_REQUESTS]

                # Create async tasks
                tasks = [fetch_and_save(session, item_id, cursor) for item_id in batch]

                results = await asyncio.gather(*tasks) or []

                valid_results = [
                    (meta, item_id)
                    for res in results
                    if res and isinstance(res, tuple)
                    for meta, item_id in [res]
                ]

                metadata_batch = []
                item_ids_batch = []

                if valid_results:
                    metadata_batch, item_ids_batch = zip(
                        *valid_results
                    )  # Unpack only if valid
                    all_downloaded_metadata.extend(metadata_batch)
                    all_downloaded_ids.extend(item_ids_batch)

                # Ensure downloaded_ids always has a valid list
                downloaded_ids = list(item_ids_batch) if item_ids_batch else []
                total_downloaded_session += len(downloaded_ids)
                cursor_cache["downloaded_count"] += len(downloaded_ids)
                cursor_cache["item_ids"].extend(downloaded_ids)

                with open(cursor_cache_file, "w", encoding="utf-8") as f:
                    json.dump(cursor_cache, f, indent=4)

                # Update global cache
                cache["cursor_count"] += 1
                cache["total_items"] += len(downloaded_ids)
                save_cache(cache, new_cursor=cursor, next_cursor=next_cursor)

            # Insert batch into MongoDB
            if all_downloaded_metadata:
                inserted_count = (
                    insert_bulk_metadata(all_downloaded_metadata, all_downloaded_ids)
                    or 0
                )
                duplicates = len(all_downloaded_metadata) - inserted_count

                if duplicates > 0:
                    print(
                        f"⚠️ Skipped {duplicates} duplicates. Inserted {inserted_count} new items."
                    )

                print(
                    f"📊 MongoDB total: {get_mongo_count()} items | Local total: {get_local_count()} items"
                )

            print(
                f"\n📝 Fetching metadata completed. {len(all_downloaded_metadata)} results retrieved."
            )

            if limit is not None and total_downloaded_session >= limit:
                print(f"🛑 Download limit of {limit} reached. Stopping.")
                break

            if next_cursor:
                print(f"💾 Cursor `{cursor}` processed. Next: `{next_cursor[:8]}...`")
                cursor = next_cursor
            else:
                print(f"✅ `{cursor}`: No more items.")
                break

    # Summary analysis
    end_time = time.time()
    execution_time = round(end_time - start_time, 2)

    analysis_data = {
        "total_cursors": cache["cursor_count"],
        "total_items": cache["total_items"],
        "execution_time_seconds": execution_time,
    }

    with open(ANALYSIS_LOG, "w", encoding="utf-8") as f:
        json.dump(analysis_data, f, indent=4)

    print(f"\n📊 Execution summary saved. Time elapsed: {execution_time} seconds.")
