import os
from config.settings import EUROPEANA_API_KEY

# ✅ API Base URLs
SEARCH_URL = "https://api.europeana.eu/record/v2/search.json"
RECORD_URL = "https://api.europeana.eu/record"

# ✅ API Parameters
DEFAULT_ROWS = 100  # Number of items per API request
DEFAULT_REUSABILITY = "open"  # Retrieve only open-license records
DEFAULT_MEDIA = "true"  # Ensure media items are retrieved
DEFAULT_QUERY = "*"  # Required query parameter
BATCH_SIZE = 1000

API_PARAMS = {
    "wskey": EUROPEANA_API_KEY,
    "query": DEFAULT_QUERY,
    "rows": DEFAULT_ROWS,
    "reusability": DEFAULT_REUSABILITY,
    "media": DEFAULT_MEDIA,
}

# List of `dcType`s to be excluded
EXCLUDED_DC_TYPES = [
    "Newspaper",
    "Newspaper Issue",
    "Analytic serial",
    "PublicationIssue",
    "Publication cover",
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


# ✅ Data Storage Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "../data")
JSON_DIR = os.path.join(DATA_DIR, "json")  # JSON metadata storage
LOGS_DIR = os.path.join(DATA_DIR, "logs")  # Logs directory
LOG_FILE = os.path.join(LOGS_DIR, "ids.log")  # Log file path
CACHE_FILE = os.path.join(
    LOGS_DIR, "cache.json"
)  # Cache file for tracking total downloads
CURSOR_FILE = os.path.join(LOGS_DIR, "cursor_state.json")  # File to store cursor

# Ensure directories exist
os.makedirs(JSON_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

# Ensure cache file exists
if not os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        f.write('{"downloaded_count": 0}')
