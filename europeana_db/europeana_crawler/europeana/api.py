import asyncio
import json
from os.path import exists, join

import aiofiles
import aiohttp
from helpers.cache_handler import load_cache, save_cache
from helpers.constants import (
    API_PARAMS,
    CACHE_FILE,
    FAILED_REQUESTS_FILE,
    LOGS_DIR,
    RECORD_URL,
    SEARCH_URL,
)


async def save_failed_request(url, params, status="UNKNOWN", message="No details"):
    """Save failed API requests for future retries."""
    failed_request = {
        "url": url,
        "params": params,
        "status": status,
        "error_message": message,
    }

    if exists(FAILED_REQUESTS_FILE):
        with open(FAILED_REQUESTS_FILE, "r", encoding="utf-8") as f:
            failed_requests = json.load(f)
    else:
        failed_requests = []

    failed_requests.append(failed_request)

    with open(FAILED_REQUESTS_FILE, "w", encoding="utf-8") as f:
        json.dump(failed_requests, f, indent=4)

    print(f"💾 Failed request saved: {url} (Status: {status})")


async def save_cursor(cursor):
    """Save cursor inside cache.json instead of separate files."""
    if cursor and cursor not in ["*", None]:
        cache = load_cache()

        # Update next cursor inside cache.json
        cache["next_cursor"] = cursor
        save_cache(cache)

        print(f"💾 Next cursor saved: {cursor}")
    else:
        print("⚠️ Not saving cursor because it is empty or invalid.")


async def save_log(cursor, message):
    """Save logs in a separate file per cursor."""
    log_file = join(LOGS_DIR, f"{cursor}.log")
    async with aiofiles.open(log_file, "a", encoding="utf-8") as f:
        await f.write(message + "\n")
    print(message)


def load_cursor():
    """Load the last saved cursor from cache.json to resume from the correct position."""
    if exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)

                last_cursor = data.get("last_cursor")
                next_cursor = data.get("next_cursor")

                # Always start from last_cursor if it's valid
                if last_cursor and last_cursor not in ["*", None]:
                    print(f"🔄 Resuming from last processed cursor: `{last_cursor}`")

                    return last_cursor

                # Otherwise, fallback to next_cursor only if it's valid
                if next_cursor and next_cursor not in ["*", None]:
                    print(
                        f"🔄 No pending work on last cursor. Moving to next: `{next_cursor}`"
                    )

                    return next_cursor

                print("⚠️ No valid cursor found. Restarting fresh.")
                return "*"

        except (json.JSONDecodeError, FileNotFoundError):
            print("⚠️ Cursor file corrupted. Resetting cursor.")

            return "*"

    return "*"


async def fetch_with_retries(session, url, params, max_retries=5):
    """Fetch API data asynchronously with retry logic to handle rate limits and server failures."""
    retries = 0
    while retries < max_retries:
        try:
            async with session.get(url, params=params, timeout=15) as response:
                if response.status == 200:
                    return await response.json()

                elif response.status in [
                    429,
                    502,
                    503,
                    504,
                    520,
                ]:
                    wait_time = 2**retries  # Exponential backoff
                    print(f"⚠️ API Error {response.status}. Retrying in {wait_time}s...")
                    await asyncio.sleep(wait_time)
                    retries += 1

                else:  # Non-retryable API errors (e.g., 400, 404)
                    error_message = await response.text()
                    print(
                        f"❌ API Error {response.status} | Message: {error_message} | Skipping item."
                    )
                    await save_failed_request(
                        url, params, response.status, error_message
                    )

                    return None

        except (
            aiohttp.ClientError,
            asyncio.TimeoutError,
        ) as e:  # Handle network failures
            wait_time = 2**retries
            print(f"⚠️ Network Error: {e}. Retrying in {wait_time}s...")
            await asyncio.sleep(wait_time)
            retries += 1

    print(f"🚨 Max retries ({max_retries}) reached. Skipping this item.")
    await save_failed_request(url, params, "MAX_RETRIES", "Maximum retries reached")

    return None


# This is not running right now. To add this
# add the following to the beggining of collect_data RequestException
# in the downloader.py
"""
async with aiohttp.ClientSession() as session:
    await retry_failed_requests(session)  # Retry previous failures first
"""


async def retry_failed_requests(session):
    """Retry API requests that previously failed."""
    if not exists(FAILED_REQUESTS_FILE):
        print("✅ No failed requests to retry.")
        return

    async with aiofiles.open(FAILED_REQUESTS_FILE, "r", encoding="utf-8") as f:
        lines = await f.readlines()

    if not lines:
        print("✅ No failed requests to retry.")
        return

    print(f"🔄 Retrying {len(lines)} failed requests...")

    async with aiofiles.open(FAILED_REQUESTS_FILE, "w", encoding="utf-8") as f:
        await f.write("")

    for line in lines:
        try:
            failed_request = json.loads(line)
            url, params = failed_request["url"], failed_request["params"]

            print(f"🔄 Retrying: {url}")
            data = await fetch_with_retries(session, url, params)
            if data:
                print(f"✅ Successfully retrieved: {url}")
            else:
                print(f"❌ Still failed: {url}, will re-log for next retry.")
                await save_failed_request(url, params)

        except json.JSONDecodeError:
            print(f"⚠️ Skipping corrupted log entry: {line}")


async def fetch_item_ids(session, cursor=None):
    """Fetch item IDs using cursor-based pagination."""
    if cursor is None:
        cursor = load_cursor()

    print(f"🔍 Querying API with cursor: `{cursor}`")

    params = API_PARAMS.copy()
    params["cursor"] = cursor

    data = await fetch_with_retries(session, SEARCH_URL, params)
    if not data:
        print("❌ API returned no valid response. Stopping download.")
        return [], None, None

    raw_items = data.get("items", [])
    next_cursor = data.get("nextCursor")
    total_items = data.get("totalResults", None)  # Get total available items

    print(f"📊 API Returned: {len(raw_items)} items for cursor `{cursor}`")

    if next_cursor:
        await save_cursor(next_cursor)

    return raw_items, next_cursor, total_items


async def fetch_item_metadata(session, item_id, verbose=False):
    """Fetch full metadata for a specific item asynchronously with retry logic."""
    url = f"{RECORD_URL}{item_id}.json"
    params = {"wskey": API_PARAMS["wskey"]}

    metadata = await fetch_with_retries(session, url, params)

    if not metadata:
        print(f"❌ ERROR: No metadata returned for `{item_id}`. Check API response.")
    elif verbose:
        print(
            f"✅ Metadata successfully retrieved for `{item_id}`"
        )  # Only prints if verbose=True is set

    return metadata
