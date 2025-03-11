import requests
import json

# Mocking the EXCLUDED_DC_TYPES from the constants module
EXCLUDED_DC_TYPES = [
    "Newspaper",
    "Newspaper Issue",
    "Analytic serial",
    "PublicationIssue",
    "Article",
    "Manuscript",
    "Book",
    "Letter",
    "Painting",
    "Fine Art",
    "Watercolours",
    "Oil painting",
    "Drawing",
    "Prints & Drawings",
    "Story",
    "Sketchbooks",
    "Text",
]

EXCLUDED_DC_TYPES = [item.lower() for item in EXCLUDED_DC_TYPES]

# API URL for the test item with dcType Newspaper
test_item_url = "https://api.europeana.eu/record/317/2fb0b95e_d5ea_4dc7_ba72_a93ec523fc3d.json?wskey=iaceddupboa"


def fetch_and_filter_item(api_url: str) -> None:
    """Fetch an item from the Europeana API and check if it should be filtered out."""
    response = requests.get(api_url)

    if response.status_code != 200:
        print(f"❌ Failed to fetch item. Status code: {response.status_code}")
        return

    item_data = response.json()

    print("\n🔍 Full JSON Response:")
    print(json.dumps(item_data, indent=2))

    # Extract the 'about' field or item ID
    item_id = item_data.get("about") or item_data.get("object", {}).get(
        "about", "Unknown ID"
    )

    # Recursive function to find excluded `dcType`s with detailed debugging
    def find_excluded_dctype(data, path=""):
        """Recursively search for excluded dcType values in the JSON data."""
        if isinstance(data, dict):
            for key, value in data.items():
                new_path = f"{path}.{key}" if path else key

                if key == "dcType" and isinstance(value, dict):
                    dc_types = value.get("def", []) + value.get("en", [])
                    normalized_types = [dc_type.lower() for dc_type in dc_types]

                    print(f"🔍 Found dcType at {new_path}: {dc_types}")

                    for dc_type in normalized_types:
                        if any(
                            excluded_type in dc_type
                            for excluded_type in EXCLUDED_DC_TYPES
                        ):
                            print(f"📰 Excluded type '{dc_type}' found in {new_path}")
                            return True

                if find_excluded_dctype(value, new_path):
                    return True

        elif isinstance(data, list):
            for index, item in enumerate(data):
                if find_excluded_dctype(item, f"{path}[{index}]"):
                    return True

        return False

    should_exclude = find_excluded_dctype(item_data)

    if should_exclude:
        print(f"The item '{item_id}' contains an excluded dcType and will be excluded.")
    else:
        print(
            f"The item '{item_id}' does NOT contain an excluded dcType and will be included."
        )


fetch_and_filter_item(test_item_url)
