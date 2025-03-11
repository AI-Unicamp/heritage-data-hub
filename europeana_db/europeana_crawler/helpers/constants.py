from os import makedirs
from os.path import abspath, dirname, exists, join

from config.settings import EUROPEANA_API_KEY

# API Base URLs
SEARCH_URL = "https://api.europeana.eu/record/v2/search.json"
RECORD_URL = "https://api.europeana.eu/record"

# API Parameters
DEFAULT_ROWS = 100  # Number of items per API request. The default value in the browser request is 12, but the limit support is 100, more than this will set to the limit
DEFAULT_REUSABILITY = "open"  # Retrieve only open-license records
DEFAULT_MEDIA = "true"  # Ensure to contain media
DEFAULT_QUERY = "*"  # Required query parameter for starting point
BATCH_SIZE = 100
MAX_CONCURRENT_REQUESTS = 50

API_PARAMS = {
    "wskey": EUROPEANA_API_KEY,
    "query": DEFAULT_QUERY,
    "rows": DEFAULT_ROWS,
    "reusability": DEFAULT_REUSABILITY,
    "media": DEFAULT_MEDIA,
}

# Data Storage Paths
BASE_DIR = dirname(abspath(__file__))
DATA_DIR = join(BASE_DIR, "../data")
JSON_DIR = join(DATA_DIR, "json")
LOGS_DIR = join(DATA_DIR, "logs")
LOG_FILE = join(LOGS_DIR, "ids.log")
CACHE_FILE = join(LOGS_DIR, "cache.json")
CURSOR_FILE = join(LOGS_DIR, "cursor_state.json")
ANALYSIS_LOG = join(LOGS_DIR, "analysis.log")
FAILED_REQUESTS_FILE = join(LOGS_DIR, "failed_requests.json")


# Ensure directories exist
makedirs(JSON_DIR, exist_ok=True)
makedirs(LOGS_DIR, exist_ok=True)

# Ensure cache file exists
if not exists(CACHE_FILE):
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        f.write('{"downloaded_count": 0}')
