"""Auxiliar functions."""
from json import load
from os.path import isdir, isfile, join
from os import listdir, makedirs
from shutil import copy
from requests import get
from difPy import dif

def pages(museum_dict) -> int:
    """
    Get the total number of pages for each museum.

    Args:
        museum_dict: a dictionary with the Museum acronym and base url.
    """
    total_pages = {}
    for acr, url in museum_dict.items():
        first_response = get(f'{url}1')
        num_pages = first_response.headers['x-wp-totalpages']
        total_pages[acr] = num_pages

    return total_pages


def read_files(path: str) -> list:
    """
    Read all files in a directory.

    Args:
        path: directory where the files are located.
    """
    files = [f for f in listdir(path) if isfile(join(path, f))]

    return files


def copy_files(file, dest):
    """
    Copy a file to a specified folder.

    Args:
        file: origin file.
        dest: destination folder that the file will be placed.
    """
    if not isdir(dest):
        makedirs(dest, exist_ok=True)

    copy(file, dest)


def load_json(jsons_path: str, file_name: str):
    """Load a JSON file.

    Args:
        jsons_path: the path os jsons.
        file_name: name of the file that will be loaded.
    """
    file_path = join(jsons_path, file_name)
    with open(file_path, encoding='utf-8') as f:
        data = load(f)

    return data


def get_nested(dictionary: dict, path: list):
    """
    Get the values of a specific item in a JSON by passing the path as a list.

    Args:
        path: list as the path until the specific value.
    """
    for nest in path:
        dictionary = dictionary[nest]
    return dictionary


def ask_user(question, function):
    """
    Ask the user if it would like to download tree data.

    Args:
        data: the data missing that will be downloaded.
    """
    answer = input(question)
    if answer == 'Yes':
        function()
    elif answer == 'No':
        print('The data will not be downloaded.')
        return
    else:
        print('Please enter Yes or No.')


def check_bad_words(bw_dict, label, target_string):
    """
    Check misunderstanding objects.

    Args:
        bw_dict: dict containing all the bad words by label.
        label: the label to be check.
    """
    return bool(bw_dict.key == label) and (target_string in bw_dict.value)


def remove_duplicated_img(images_path):
    """
    Remove duplicated images via mean square error.

    Args:
        images_path: path of the folder containing all images.
    """
    dif.compare_images(images_path, delete=True)
