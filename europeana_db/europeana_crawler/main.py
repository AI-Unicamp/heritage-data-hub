import argparse
from europeana.downloader import collect_data


def main():
    parser = argparse.ArgumentParser(description="Europeana Dataset Downloader")

    # Argument for setting a limit on downloads
    parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Limit the number of items to download (default: 10)",
    )

    # Argument to download all available files
    parser.add_argument(
        "--all",
        action="store_true",
        help="Download all available files (ignores --limit)",
    )

    args = parser.parse_args()

    # If --all is used, set limit to None (i.e., download everything)
    download_limit = None if args.all else args.limit

    collect_data(limit=download_limit)


if __name__ == "__main__":
    main()
