import os
from os.path import join

from lingua import LanguageDetectorBuilder

from helpers.metadata_handler import (save_json, save_metadata,
                                      save_skipped_metadata)
from helpers.translator import translate_to_english


class Downloader:
    def __init__(self, data_dir="data", category=None):
        """
        Initializes the Downloader class.
        :param data_dir: Directory for saving metadata and JSON files.
        :param category: The category to use for filtering (must be provided).
        """
        if not category:
            raise ValueError("A category must be provided.")

        # Define the directories for metadata (CSV files), JSON files, and logs
        self.metadata_dir = join(data_dir, "metadata")
        self.json_dir = join(data_dir, "json")
        self.logs_dir = join(data_dir, "logs")
        self.skipped_logs_dir = join(self.logs_dir, "skipped")
        self.category = category

        # Ensure that the directories are created
        os.makedirs(self.metadata_dir, exist_ok=True)
        os.makedirs(self.json_dir, exist_ok=True)
        os.makedirs(self.logs_dir, exist_ok=True)
        os.makedirs(self.skipped_logs_dir, exist_ok=True)

        # Initialize cumulative counts
        self.cumulative_valid_count = 0
        self.cumulative_skipped_count = 0

        # Create a language detector for use in title and description detection
        self.detector = (
            LanguageDetectorBuilder.from_all_languages()
            .with_preloaded_language_models()
            .build()
        )

    def get_title(self, item):
        """Get the title, translating if necessary."""
        # Fallback to 'title' field if 'dcTitleLangAware' is not available
        if "title" in item:
            original_title = item["title"][0] if isinstance(item["title"], list) else item["title"]

            # Detect language using `lingua`
            try:
                detected_language = self.detector.detect_language_of(original_title)
                detected_lang_code = detected_language.iso_code_639_1.name.lower()  # Convert to lowercase
            except Exception as e:
                detected_lang_code = "unknown"
                print(f"Failed to detect language for title: {e}")

            # Translate the title if not in English
            if detected_lang_code != "en":
                translated_title = translate_to_english(original_title, detected_lang_code)
            else:
                translated_title = original_title  # No translation needed

            return {
                "original": original_title,
                "translated": translated_title,
                "lang": detected_lang_code
            }

        # If no title is available
        return {
            "original": "No title available",
            "translated": "No title available",
            "lang": "N/A"
        }

    def get_description(self, item):
        """Get the description, translating if necessary."""
        description_aware = item.get("dcDescriptionLangAware", {})
        description_list = description_aware.get("en", [])

        if isinstance(description_list, list) and description_list:
            return {
                "original": description_list[0],
                "translated": description_list[0],  # Already in English
                "lang": "en"
            }

        # Fallback to 'dcDescription' field if 'dcDescriptionLangAware' is not available
        if "dcDescription" in item:
            original_description = item["dcDescription"][0] if isinstance(item["dcDescription"], list) else item["dcDescription"]

            # Detect language using `lingua`
            try:
                detected_language = self.detector.detect_language_of(original_description)
                detected_lang_code = detected_language.iso_code_639_1.name.lower()  # Convert to lowercase
            except Exception as e:
                detected_lang_code = "unknown"
                print(f"Failed to detect language for description: {e}")

            # Translate the description if not in English
            if detected_lang_code != "en":
                translated_description = translate_to_english(original_description, detected_lang_code)
            else:
                translated_description = original_description  # No translation needed

            return {
                "original": original_description,
                "translated": translated_description,
                "lang": detected_lang_code
            }

        # If no description is available
        return {
            "original": "No description available",
            "translated": "No description available",
            "lang": "N/A"
        }

    def is_valid_image_format(self, image_url):
        """Check if the image URL has a valid image format by extension or by making a request."""
        if any(image_url.endswith(ext) for ext in [".jpg", ".jpeg", ".png", ".tiff"]):
            return True
        try:
            import requests
            response = requests.head(image_url, allow_redirects=True)
            content_type = response.headers.get("Content-Type", "")
            return "image" in content_type
        except requests.RequestException:
            return False

    def filter_and_save(self, items):
        """Filter items based on category and save valid/invalid items separately."""
        valid_items = []
        skipped_items = []

        for item in items:
            item_id = item.get("id", "unknown")

            # Handle title with translation
            title = self.get_title(item)

            # Handle description with translation
            description = self.get_description(item)

            image_urls = item.get("edmIsShownBy", [])
            image_url = image_urls[0] if isinstance(image_urls, list) and image_urls else None

            # If no description is found, skip the item
            if not description:
                skipped_items.append({
                    "id": item_id,
                    "title": title["original"],
                    "image_url": image_url or "N/A",
                    "description": description["original"]
                })
                save_json(item, item_id, self.skipped_logs_dir)  # Save skipped item JSON
                self.cumulative_skipped_count += 1
                continue

            # If the item has a valid image URL, save it
            if image_url and self.is_valid_image_format(image_url):
                valid_items.append(
                    {
                        "id": item_id.replace("/", "_"),
                        "title": title["translated"],
                        "original_title": title["original"],
                        "original_title_language_alpha_2": title["lang"],
                        "image_url": image_url,
                        "english_description": description["translated"],
                        "original_description": description["original"],
                        "original_description_language_alpha_2": description["lang"],
                    }
                )
                self.cumulative_valid_count += 1
                save_json(item, item_id, self.json_dir)
            else:
                skipped_items.append({
                    "id": item_id,
                    "title": title["original"],
                    "image_url": image_url or "N/A",
                    "description": description["original"]
                })
                save_json(item, item_id, self.skipped_logs_dir)
                self.cumulative_skipped_count += 1

        # Save valid items
        if valid_items:
            save_metadata(
                valid_items, len(valid_items), "valid_items.csv", self.metadata_dir
            )
        print(f"\nSaving {len(valid_items)} valid items to the valid metadata csv.")

        # Save skipped items
        if skipped_items:
            save_skipped_metadata(
                skipped_items, len(skipped_items), "skipped_items.csv", self.metadata_dir
            )
        print(f"Saving {len(skipped_items)} skipped items to the skipped metadata csv.")
