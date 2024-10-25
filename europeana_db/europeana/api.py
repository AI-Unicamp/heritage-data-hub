import requests

from config import EUROPEANA_API_KEY
from helpers.constants import API_BASE_URL


class EuropeanaAPI:
    def __init__(self, api_key=EUROPEANA_API_KEY):
        self.api_key = api_key

    def search(self, query, rows=100, cursor=None, media=True, reusability="open"):
        """Search the Europeana API and return a list of cultural heritage objects (CHOs)."""
        params = {
            "wskey": self.api_key,
            "query": query,
            "rows": rows,
            "cursor": cursor,
            "media": media,
            "reusability": reusability,
        }
        response = requests.get(API_BASE_URL, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(
                f"API request failed with status code {response.status_code}"
            )
