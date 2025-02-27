import json
import os
import time
import requests
from helpers.constants import (
    CURSOR_FILE,
    SEARCH_URL,
    EXCLUDED_DC_TYPES,
    RECORD_URL,
    API_PARAMS,
)
from requests.exceptions import RequestException, ChunkedEncodingError


def save_cursor(cursor):
    """Save the current cursor to a file so downloads can resume."""
    if cursor and cursor not in ["*", None]:  # ✅ Ensure cursor is valid before saving
        with open(CURSOR_FILE, "w", encoding="utf-8") as f:
            json.dump({"cursor": cursor}, f)
        print(f"💾 Cursor saved: {cursor}")  # ✅ Debugging
    else:
        print("⚠️ Not saving cursor because it is empty or invalid.")


def load_cursor():
    """Load the last saved cursor from file and ensure it's valid."""
    if os.path.exists(CURSOR_FILE):
        try:
            with open(CURSOR_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                cursor = data.get("cursor")
                if cursor and cursor not in ["*", None]:  # ✅ Ensure cursor is valid
                    print(f"🔄 Resuming from cursor: {cursor}")
                    return cursor
                else:
                    print("⚠️ Cursor file is empty or invalid. Resetting cursor.")
                    return None  # ✅ Reset if the cursor is invalid
        except (json.JSONDecodeError, FileNotFoundError):
            print("⚠️ Cursor file corrupted. Resetting cursor.")
            return None  # ✅ Reset cursor if corrupted
    return None  # ✅ No cursor file exists yet, start fresh


def fetch_with_retries(url, params, max_retries=5):
    """Fetch API data with retry logic to handle rate limits and server failures."""
    retries = 0
    while retries < max_retries:
        try:
            response = requests.get(url, params=params, timeout=15)
            if response.status_code == 200:
                return response.json()
            elif response.status_code in [429, 502, 503, 504, 520]:  # Handle failures
                wait_time = 2**retries  # Exponential backoff
                print(
                    f"⚠️ API Error {response.status_code}. Retrying in {wait_time}s..."
                )
                time.sleep(wait_time)
                retries += 1
            else:
                print(
                    f"❌ API Error: {response.status_code} | Message: {response.text}"
                )
                return None  # Don't retry for other errors
        except (RequestException, ChunkedEncodingError) as e:
            wait_time = 2**retries
            print(f"⚠️ Network Error: {e}. Retrying in {wait_time}s...")
            time.sleep(wait_time)
            retries += 1

    print("🚨 Max retries reached. Skipping request.")
    return None


def find_excluded_dctype(data, path=""):
    """Recursively search for excluded dcType values in the JSON data."""
    if isinstance(data, dict):
        for key, value in data.items():
            new_path = f"{path}.{key}" if path else key

            # Check if the current key is "dcType" and value contains an excluded type
            if key == "dcType" and isinstance(value, dict):
                dc_types = value.get("def", []) + value.get("en", [])
                normalized_types = [dc_type.lower() for dc_type in dc_types]
                if any(
                    excluded_type.lower() in normalized_types
                    for excluded_type in EXCLUDED_DC_TYPES
                ):
                    print(f"📰 Excluded type found in {new_path}: {dc_types}")
                    return True

            # Recursively search in nested structures
            if find_excluded_dctype(value, new_path):
                return True

    elif isinstance(data, list):
        for index, item in enumerate(data):
            if find_excluded_dctype(item, f"{path}[{index}]"):
                return True

    return False


def fetch_item_ids(cursor=None):
    """Fetch item IDs using cursor-based pagination with retries."""
    if cursor is None:  # ✅ Always try to load the last saved cursor
        cursor = load_cursor()

    print(f"🔍 Querying API with cursor: {cursor}")

    # 🔥 Use the full API_PARAMS dictionary directly
    params = API_PARAMS.copy()  # Make a copy to avoid mutating the global dictionary
    params["cursor"] = cursor

    data = fetch_with_retries(SEARCH_URL, params)
    if not data:
        print("❌ API returned no valid response. Stopping download.")
        return [], None

    raw_items = data.get("items", [])
    filtered_items = [item for item in raw_items if not find_excluded_dctype(item)]
    next_cursor = data.get("nextCursor")

    print(f"📊 API Returned: {len(filtered_items)} items")  # 🔍 Debugging line

    if next_cursor:
        print(f"💾 Saving next cursor: {next_cursor}")  # ✅ Debugging
        save_cursor(next_cursor)  # ✅ Always save the next cursor
    else:
        print("✅ No more pages to fetch.")

    return filtered_items, next_cursor


def fetch_item_metadata(item_id):
    """Fetch full metadata for a specific item with retry logic."""
    url = f"{RECORD_URL}{item_id}.json"
    params = {"wskey": API_PARAMS["wskey"]}

    return fetch_with_retries(url, params)
