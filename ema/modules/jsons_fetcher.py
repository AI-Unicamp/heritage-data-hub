"""Download text data from museum's website."""

import json
from os import makedirs
from os.path import exists, isdir, join
import time
from tqdm import tqdm
import requests
from helpers.constants import MUSEUM_DICT, DATA_RAW_JSONS
from helpers import auxiliar


def savefile(filename: str, data: dict):
    """
    Save the JSON file into a folder if not exists.

    Args:
        filename: name of the file that will be saved.
        data: JSON reponse.
    """
    if not exists(filename):
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(
                    data,
                    file,
                    sort_keys=True,
                    ensure_ascii=False,
                    indent=4
                    )


def __request(url, try_count=10):
    s = requests.Session()
    for error_count in range(0, try_count):
        try:
            return s.get(url)
        except requests.exceptions.ConnectionError as e:
            print(f'Cannot connect to url {url} trying again \
                    ({error_count}/{try_count} - {e})...')
            time.sleep(60)
            continue


def fetcher_perpage(base_url: str, acr: str, page_num: int):
    """
    Go throught every page and download the JSON file.

    Args:
        url: url of the museum.
        page_num: number of the page containing the JSON content that will be downloaded.
    """
    if not isdir(DATA_RAW_JSONS):
        makedirs(DATA_RAW_JSONS, exist_ok=True)

    r = __request(f'{base_url}{page_num}')
    assert r.status_code == 200, (f"Não foi possível acessar o acervo \
            {r.content} - {f'{base_url}{page_num}'}/{r.content}")
    for item in range(0, len(r.json()['items'])):
        data = r.json()['items'][item]
        object_id = r.json()['items'][item]['id']
        filename = join(DATA_RAW_JSONS, f'{acr}_{object_id}.json')
        savefile(filename, data)

    return True


def get_jsons():
    """Download JSON files from IBRAM Museums."""
    npages = auxiliar.pages(MUSEUM_DICT)
    for acr, url in MUSEUM_DICT.items():
        print('Museum ACR:', acr)
        for page in tqdm(range(1, int(npages[acr]) + 1)):
            fetcher_perpage(url, acr, page)

    return True
