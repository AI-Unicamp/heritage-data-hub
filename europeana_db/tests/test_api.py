import json
import unittest

from europeana.api import EuropeanaAPI


class TestEuropeanaAPI(unittest.TestCase):
    def setUp(self):
        """Set up the API instance before each test."""
        self.api = EuropeanaAPI()

    def test_search_furniture(self):
        """Test searching for 'Furniture' objects."""
        query = "Furniture"
        rows = 5  # Fetch a small number of results for testing

        try:
            # Perform API search
            response = self.api.search(query=query, rows=rows)

            # Check if the response contains items
            self.assertIn("items", response)
            self.assertGreater(
                len(response["items"]), 0, "No items found in the response"
            )

            # Pretty print the JSON response for inspection
            formatted_response = json.dumps(response, indent=4, ensure_ascii=False)
            print(formatted_response)

        except Exception as e:
            self.fail(f"API request failed: {e}")


if __name__ == "__main__":
    unittest.main()
