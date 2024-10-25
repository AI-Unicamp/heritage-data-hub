import csv
import json
import os
from os.path import join


def save_metadata(items, valid_items_count, csv_filename, metadata_dir):
    """Append valid metadata to a CSV file."""
    csv_path = join(metadata_dir, csv_filename)
    file_exists = os.path.isfile(csv_path)

    with open(csv_path, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "id",
                "title",  # Translated title
                "original_title",  # Original title
                "original_title_language_alpha_2",  # Language code for the original title
                "image_url",
                "english_description",  # Translated description
                "original_description",  # Original description
                "original_description_language_alpha_2",  # Language code for the original description
            ],
        )

        # Write the header only if the file does not exist
        if not file_exists:
            writer.writeheader()

        # Filter only the expected fields to avoid extra fields error
        for item in items[:valid_items_count]:
            filtered_item = {
                "id": item.get("id", "N/A"),
                "title": item.get("title", "No title available"),
                "original_title": item.get(
                    "original_title", "No original title available"
                ),
                "original_title_language_alpha_2": item.get(
                    "original_title_language_alpha_2", "N/A"
                ),
                "image_url": item.get("image_url", "N/A"),
                "english_description": item.get(
                    "english_description", "No description available"
                ),
                "original_description": item.get(
                    "original_description", "No original description available"
                ),
                "original_description_language_alpha_2": item.get(
                    "original_description_language_alpha_2", "N/A"
                ),
            }
            writer.writerow(filtered_item)


def save_skipped_metadata(items, skipped_items_count, csv_filename, metadata_dir):
    """Append skipped metadata to the skipped CSV file."""
    csv_path = join(metadata_dir, csv_filename)
    file_exists = os.path.isfile(csv_path)

    with open(csv_path, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file, fieldnames=["id", "title", "image_url", "description"]
        )

        # Write the header only if the file does not exist
        if not file_exists:
            writer.writeheader()

        # Write only the skipped items
        for item in items[:skipped_items_count]:
            writer.writerow(item)


def save_json(item, item_id, json_dir):
    """Save the full JSON of each item in the json_dir folder."""
    safe_item_id = item_id.replace("/", "_")
    json_filename = join(json_dir, f"{safe_item_id}.json")

    try:
        with open(json_filename, "w", encoding="utf-8") as json_file:
            json.dump(item, json_file, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Failed to save JSON for item ID {safe_item_id}: {e}")
