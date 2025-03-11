import argparse
import asyncio
from europeana.downloader import collect_data


async def main():
    parser = argparse.ArgumentParser(description="Europeana Dataset Downloader")

    parser.add_argument(
        "--limit",
        type=int,
        default=100,
        help="Limit the number of items to download (default: 100)",
    )

    parser.add_argument(
        "--all",
        action="store_true",
        help="Download all available files (ignores --limit)",
    )

    args = parser.parse_args()

    # If --all is used, set limit to None (i.e., download everything)
    download_limit = None if args.all else args.limit

    # Run the async function
    await collect_data(limit=download_limit)


if __name__ == "__main__":
    asyncio.run(main())
