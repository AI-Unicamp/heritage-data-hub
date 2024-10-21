import unittest

from europeana.parser import parse_image_url, parse_metadata


class TestParser(unittest.TestCase):

    def test_parse_metadata(self):
        """Test metadata parsing from an API response item."""
        mock_item = {
            "id": "12345",
            "title": ["Test Title"],
            "dcDescription": ["Test Description"],
            "dcCreator": ["Test Creator"],
        }
        metadata = parse_metadata(mock_item)
        self.assertEqual(metadata["id"], "12345")
        self.assertEqual(metadata["title"], "Test Title")
        self.assertEqual(metadata["description"], "Test Description")
        self.assertEqual(metadata["creator"], "Test Creator")

    def test_parse_image_url(self):
        """Test image URL parsing from an API response item."""
        mock_item = {"edmIsShownBy": ["http://test.com/image.jpg"]}
        image_url = parse_image_url(mock_item)
        self.assertEqual(image_url, "http://test.com/image.jpg")

    def test_parse_image_url_missing(self):
        """Test that None is returned when no image URL exists."""
        mock_item = {}
        image_url = parse_image_url(mock_item)
        self.assertIsNone(image_url)


if __name__ == "__main__":
    unittest.main()
