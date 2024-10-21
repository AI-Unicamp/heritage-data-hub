import argparse

from europeana.api import EuropeanaAPI
from europeana.downloader import Downloader


def main():
    # Argparse configuration for command-line interaction
    parser = argparse.ArgumentParser(description="Download data from Europeana API")
    parser.add_argument("-q", "--query", type=str, required=True, help="Search query")
    parser.add_argument(
        "-r", "--rows", type=int, default=100, help="Number of rows to retrieve"
    )
    parser.add_argument(
        "-c",
        "--category",
        type=str,
        required=True,
        help="Category for filtering (e.g., furniture, painting)",
    )
    parser.add_argument(
        "-d",
        "--data-dir",
        type=str,
        default="data",
        help="Directory to save the results",
    )
    args = parser.parse_args()

    # API Interaction
    api = EuropeanaAPI()
    response = api.search(query=args.query, rows=args.rows)

    # Initialize the Downloader with the specified category and data directory
    downloader = Downloader(data_dir=args.data_dir, category=args.category)

    # Filter and download data (metadata and images)
    items = response.get("items", [])
    downloader.filter_and_save(items)


if __name__ == "__main__":
    main()
