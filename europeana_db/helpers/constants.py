# helpers/constants.py
API_BASE_URL = "https://api.europeana.eu/record/v2/search.json"
DEFAULT_ROWS = 100
LOG_FILE_PATH = "data/logs/europeana.log"

# Constants for different category filters

CATEGORIES = {
    "furniture": {
        "edmConceptLabel": "Furniture",  # Filter by "Furniture" in edmConceptLabel
        "dcDescriptionLangAware": "en",  # Prefer English descriptions
        "dcTitleLangAware": "en",  # Title in English
    },
    # You can add more categories here in the future, e.g., painting, cloths
    "painting": {
        "edmConceptLabel": "painting",
        "dcDescriptionLangAware": "en",
        "dcTitleLangAware": "en",
    },
    "cloths": {
        "edmConceptLabel": "cloth",
        "dcDescriptionLangAware": "en",
        "dcTitleLangAware": "en",
    },
}
