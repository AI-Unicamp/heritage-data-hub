import logging
from os import makedirs
from os.path import join

from helpers.constants import LOGS_DIR

makedirs(LOGS_DIR, exist_ok=True)

# Setup logging
logging.basicConfig(
    filename=join(LOGS_DIR, "crawler.log"),
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger()
