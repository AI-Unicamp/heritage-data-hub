import argparse
import time
from http.client import RemoteDisconnected

from requests.exceptions import ConnectionError

from europeana.api import EuropeanaAPI
from europeana.downloader import Downloader


def main():
    # Argparse configuration for command-line interaction
    parser = argparse.ArgumentParser(description="Download data from Europeana API")
    parser.add_argument("--query", type=str, required=True, help="Search query")
    parser.add_argument(
        "--rows", type=int, default=100, help="Number of rows to retrieve per request"
    )
    parser.add_argument(
        "--category",
        type=str,
        required=True,
        help="Category for filtering (e.g., furniture, painting)",
    )
    parser.add_argument(
        "--data-dir", type=str, default="data", help="Directory to save the results"
    )
    parser.add_argument(
        "--batch-size", type=int, default=10, help="Batch size for processing items"
    )
    parser.add_argument(
        "--max-items",
        type=int,
        default=100,  # Stop after retrieving 100 items
        help="Maximum number of items to retrieve for debugging",
    )

    # Parse the arguments
    args = parser.parse_args()

    # Initialize the API and the Downloader
    api = EuropeanaAPI()
    downloader = Downloader(data_dir=args.data_dir, category=args.category)

    # Retrieve all items using cursor-based pagination
    cursor = "*"
    all_items = []
    total_retrieved = 0
    total_processed = 0  # Add a counter to track processed items
    max_items = args.max_items  # Set the max items limit

    while (
        cursor and total_processed < max_items
    ):  # Control the loop with processed count
        try:
            for attempt in range(5):  # Retry loop
                try:
                    # Make the API call to retrieve a page of results
                    response = api.search(
                        query=args.query, rows=args.rows, cursor=cursor
                    )
                    break
                except Exception as e:
                    if attempt < 4:
                        print(f"API request failed (attempt {attempt + 1}/5): {e}")
                        time.sleep(5)
                    else:
                        raise Exception(f"API request failed after 5 attempts: {e}")

            # Get the items from the response
            items = response.get("items", [])
            num_items = len(items)

            # Adjust the number of items if we are close to the max limit
            if total_processed + num_items > max_items:
                items = items[
                    : max_items - total_processed
                ]  # Trim the list to hit exactly 100
                num_items = len(items)

            all_items.extend(items)
            total_retrieved += num_items
            total_processed += num_items

            print(f"Retrieved {num_items} items. Total so far: {total_retrieved}")

            # Process and save every batch of items
            while len(all_items) >= args.batch_size:
                downloader.filter_and_save(all_items[: args.batch_size])
                all_items = all_items[args.batch_size :]

                print(f"\nProcessed a batch of {args.batch_size} items.")
                print(f" - Skipped items: {downloader.cumulative_skipped_count}")
                print(f" - Valid items: {downloader.cumulative_valid_count}\n")

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
    main()
