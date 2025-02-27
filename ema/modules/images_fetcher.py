"""Download all images from museum's website."""
from json import dumps, load
from os.path import exists, isdir, join
from os import listdir, makedirs
import re
import time
from tqdm import tqdm
import requests
from helpers.constants import (HEADERS, DATA_RAW_IMAGES, DATA_RAW_JSONS,
                               WORKSPACE)
from helpers.auxiliar import read_files
from modules.jsons_fetcher import get_jsons


def url_regex(file: str) -> list:
    """
    Find all image urls in a JSON file.

    Args:
        file: JSON file to find image urls.
    """
    urls = re.findall(
            r'(?:http\:|https\:)?\/\/.[^\s"]+\.(?:jpg|jpeg|png|bmp)',
            dumps(file)
            )

    return urls


def __request(url, try_count=10):
    s = requests.Session()
    for error_count in range(0, try_count):
        try:
            return s.get(url, headers=HEADERS)
        except requests.exceptions.ConnectionError as e:
            print(f'Cannot connect to url {url} trying again \
                    ({error_count}/{try_count} - {e}')
            time.sleep(60)
            continue


def save_bad_requests(broken_link):
    """
    Save all broken links into a text file.

    Args:
        broken_link: link that could not get the image.
    """
    with open(join(WORKSPACE, 'bad_requests.txt'), 'a', encoding='utf8') as f:
        f.write(broken_link)


def fetcher(url: str, filename: str):
    """
    Download images.

    Args:
        url: url to download the image.
        filename: path of the file containing the images URL.
    """
    r = __request(url)
    if r is not None and r.status_code == 200:
        with open(filename, "wb") as file:
            file.write(r.content)
    elif r is not None:
        bad_r = f"Image could not be saved - {r.status_code} - {url}"
        print(bad_r)
        save_bad_requests(bad_r + '\n')
    else:
        bad_r = f"Image could not be saved - None - {url}"
        print(bad_r)
        save_bad_requests(bad_r + '\n')


def iterate_all(jsons_path: str, images_path: str):
    """
    Go throught all JSON files and download the images.

    Args:
        json_path: file path containing all JSON files.
        images_path: path where the images will be saved.
    """
    if not isdir(DATA_RAW_IMAGES):
        makedirs(DATA_RAW_IMAGES, exist_ok=True)

    allfiles = read_files(jsons_path)
    for file in tqdm(allfiles):
        with open(join(jsons_path, file), encoding='utf-8') as filename:
            data = load(filename)
            name_id = re.split(r'[/.]', filename.name)[-2]
            i = 0
            if url_regex(data):
                for item in list(set(url_regex(data))):
                    ext = item.split('.')[-1].rstrip('\n')
                    img = f'{join(images_path, name_id)}_{i}.{ext}'
                    if not exists(img):
                        fetcher(item, img)
                    i += 1


def get_images():
    """
    Download images from all JSON files.

    Args:
        jsons_path: directory with all JSON files.
        images_path: directory where all images will be stored.
    """
    if not isdir(DATA_RAW_JSONS):
        makedirs(DATA_RAW_JSONS, exist_ok=True)
        print("===> NOTE: It was necessary to download the JSON files first.")
        get_jsons()
        print('===> JSON files download has been completed.')
        iterate_all(DATA_RAW_JSONS, DATA_RAW_IMAGES)
    elif listdir(DATA_RAW_JSONS) == []:
        print("===> NOTE: It was necessary to download the JSON files first.")
        get_jsons()
        print('===> JSON files download has been completed.')
        iterate_all(DATA_RAW_JSONS, DATA_RAW_IMAGES)
    else:
        iterate_all(DATA_RAW_JSONS, DATA_RAW_IMAGES)
