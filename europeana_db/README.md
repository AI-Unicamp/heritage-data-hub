# Europeana-DB

Europeana-DB is a dataset designed for AI research and development, focusing on image captioning and analysis of cultural heritage object (CHO). The dataset includes a curated collection of images sourced from the Europeana API, along with their associated metadata and descriptions. The modular design of Europeana-DB allows for expansion of cultural heritage object categories, while specifically excluding certain types like books, paintings, and texts, as outlined in the project configuration (see constants.py).

## Key Features

- **CHO Coverage**: The dataset is composed of cultural heritage objects, including but not limited to furniture, textiles, artifacts, and other media available in the Europeana official database.
- **Image Captioning**: Specifically designed to generate data to train AI models.
- **Modular and Scalable**: Structured to integrate additional cultural heritage object categories in future iterations.
- **Automated Data Pipeline**: Includes tools for automated data retrieval, processing, and preparation.
- **Customizable Filters**: Easily adjust which categories to include or exclude using the `constants.py` configuration.

## Project Structure

```
heritage-data-hub
└── europeana_db
    ├── .env               # Environment variables (set here your Europeana API Key)
    ├── .gitignore
    ├── dataset            # Folder for storing processed datasets
    ├── europeana_crawler  # Module for data retrieval from the Europeana API
    │   ├── config         # Configuration files
    │   ├── data           # Raw data storage
    │   ├── europeana      # API interaction scripts
    │   ├── helpers        # Helper utilities and functions
    │   ├── main.py        # Main script for data downloading
    │   ├── notebooks      # Jupyter notebooks for exploration
    │   └── tests          # Unit and integration tests
    ├── europeana_preprocessor # Data preprocessing and cleaning module
    ├── poetry.lock
    ├── pyproject.toml
    └── README.md
```

## How to Install and Set Up

### Install Poetry

Ensure you have Poetry installed:

```sh
pip install poetry
```

### Install Dependencies

Navigate to the project directory and install dependencies using Poetry:

```sh
cd europeana_db
poetry install
```

### Activate the Virtual Environment

```sh
poetry shell
```

## How to Execute

To execute the Europeana Dataset Downloader, run the following command from the `europeana_crawler` directory:

```sh
python main.py --limit 50
```

### Options

- `--limit [LIMIT]` : Limits the number of items to download (default: 10).
- `--all` : Downloads all available files, ignoring the `--limit` parameter.

## Example

```sh
python main.py --limit 100
```

This command will download 100 items using the Europeana API and store the JSON metadata files in the `data` directory.

## Future Plans

- Expand to more categories, while maintaining the exclusion of specified `dcType`s (e.g., books, paintings, texts).
- Implement advanced preprocessing and data augmentation techniques.
- Enhance metadata enrichment using external linked data sources.

## License

Europeana-DB is released under the MIT License.
