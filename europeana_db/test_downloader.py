import time
from http.client import RemoteDisconnected

from requests.exceptions import ConnectionError

from europeana.api import EuropeanaAPI
from europeana.downloader import Downloader


def run_downloader_with_real_data():
    query = "Furniture"
    category = "furniture"
    rows = 10
    data_dir = "test_data"
    batch_size = 10
    max_items = 20

    api = EuropeanaAPI()
    downloader = Downloader(data_dir=data_dir, category=category)

    cursor = "*"
    all_items = []
    total_retrieved = 0

    while cursor and total_retrieved < max_items:
        try:
            for attempt in range(5):
                try:
                    response = api.search(query=query, rows=rows, cursor=cursor)
                    break
                except Exception as e:
                    if attempt < 4:
                        print(f"API request failed (attempt {attempt + 1}/5): {e}")
                        time.sleep(5)
                    else:
                        raise Exception(f"API request failed after 5 attempts: {e}")

            items = response.get("items", [])
            num_items = len(items)
            all_items.extend(items)
            total_retrieved += num_items

            # Process the current batch of items
            while len(all_items) >= batch_size:
                downloader.filter_and_save(all_items[:batch_size])
                all_items = all_items[batch_size:]

            # Move to the next cursor for the next batch
            cursor = response.get("nextCursor", None)

        except (RemoteDisconnected, ConnectionError) as e:
            print(f"Connection error: {e}. Retrying in 5 seconds...")
            time.sleep(5)

    # Save remaining items if they exist
    if all_items:
        downloader.filter_and_save(all_items)
        print(f"\nProcessed the remaining {len(all_items)} items.")

    # Final counts of valid and skipped items
    print(f"\nTotal valid items: {downloader.cumulative_valid_count}")
    print(f"Total skipped items: {downloader.cumulative_skipped_count}")
    print(f"Total items retrieved and saved: {total_retrieved}")


if __name__ == "__main__":
    run_downloader_with_real_data()
