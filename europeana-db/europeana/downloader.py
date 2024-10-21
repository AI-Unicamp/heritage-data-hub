import csv
import json
import os
from os.path import join

from helpers.constants import CATEGORIES  # Import the category filters
from helpers.utils import create_directories


class Downloader:
    def __init__(self, data_dir="data", category=None):
        """
        Initializes the Downloader class.

        :param data_dir: Directory for saving metadata and JSON files.
        :param category: The category to use for filtering (must be provided).
        """
        if not category:
            raise ValueError("A category must be provided.")

        # Define the directories for metadata (CSV files) and JSON files
        self.metadata_dir = join(data_dir, "metadata")
        self.json_dir = join(data_dir, "json")
        self.category = category

        # Ensure that the directories are created
        create_directories([self.metadata_dir, self.json_dir])

        # Get the filter configuration for the selected category
        self.filter_config = CATEGORIES.get(category, {})
        if not self.filter_config:
            raise ValueError(f"Category '{category}' not found in CATEGORIES.")

    def save_metadata(self, items, csv_filename="metadata.csv"):
        """Save metadata (id, image URL, and description) in a CSV file."""
        if not items:
            # Skip saving if there are no items
            print("No metadata to save.")
            return

        csv_path = join(self.metadata_dir, csv_filename)
        with open(csv_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["id", "image_url", "description"])
            writer.writeheader()
            for item in items:
                writer.writerow(item)
        print(f"Metadata saved at {csv_path}")

    def save_json(self, item, item_id):
        """Save the full JSON of each item in the json_dir folder."""
        # Sanitize the ID by replacing slashes and other unsafe characters
        safe_item_id = item_id.replace("/", "_")
        json_filename = join(self.json_dir, f"{safe_item_id}.json")

        try:
            # Save the full item JSON to a file named after the sanitized item ID
            with open(json_filename, "w", encoding="utf-8") as json_file:
                json.dump(item, json_file, indent=4, ensure_ascii=False)
            print(f"Saved full JSON for item ID {safe_item_id} at {json_filename}")
        except Exception as e:
            print(f"Failed to save JSON for item ID {safe_item_id}: {e}")

    def filter_and_save(self, items):
        """
        Filter items based on the selected category, extract metadata (id, image URL,
        and description), and save the data.
        """
        metadata_list = []

        # Extract the filter configurations for the category
        concept_label_filter = self.filter_config.get("edmConceptLabel", "").lower()
        description_lang = self.filter_config.get("dcDescriptionLangAware", "en")

        for item in items:
            # Extract the ID of the item
            item_id = item.get("id", "unknown")

            # Check if the category concept label exists in edmConceptLabel
            concept_labels = item.get("edmConceptLabel", [])
            has_concept_label = any(
                label.get("def", "").lower() == concept_label_filter
                for label in concept_labels
            )

            # If the concept label is not found, skip this item
            if not has_concept_label:
                print(
                    f"Skipping item ID {item_id}: No '{concept_label_filter}' in edmConceptLabel"
                )
                continue

            # Extract image URL from the first element of the list (edmIsShownBy)
            image_urls = item.get("edmIsShownBy", [])
            image_url = (
                image_urls[0] if isinstance(image_urls, list) and image_urls else None
            )

            # Extract description from dcDescriptionLangAware > specified language
            description_aware = item.get("dcDescriptionLangAware", {}).get(
                description_lang, []
            )
            description = (
                description_aware[0]
                if description_aware
                else f"No {description_lang} description available"
            )

            # Prepare metadata for the CSV
            item_metadata = {
                "id": item_id.replace("/", "_"),  # Use sanitized ID
                "image_url": image_url,
                "description": description,  # Now using the specified language description
            }

            # Save the full JSON of the item
            self.save_json(item, item_id)

            # Add metadata to the list
            metadata_list.append(item_metadata)

        # Only save metadata if there are matching items
        if metadata_list:
            self.save_metadata(metadata_list)
