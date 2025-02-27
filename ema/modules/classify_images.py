"""Classify images according to thesaurus or label."""
from os.path import join
from helpers.auxiliar import read_files, copy_files
from typing import List, NoReturn


def target_jsons_id(jsons_path: str) -> List[str]:
    """
    Get JSON files acronyn and id part. 

    Example: MINC_9999.
    Args:
        jsons_path: the target JSON path, for example data/interim/jsons.
    """
    files = read_files(jsons_path)
    item_json = []
    for file in files:
        item_id = file.split('_')[1].split('.')[0]
        item_acr = file.split('_')[0]
        item_json.append(f'{item_acr}_{item_id}')

    return item_json


def classify_images(raw_img_path: str, json_path: str, dest: str) -> NoReturn:
    """
    Get images based in a classification.

    The classification can be thesaurus or labels.
    Correspondent ones will be checked with the target one, from target_jsons_id.
    Args:
        raw_img_path: path of all the images (data_raw_images).
        json_path: path to interim JSON files.
        dest: path to the processed images.
    """
    files = read_files(raw_img_path)
    tg_files = target_jsons_id(json_path)
    matches = [i for i in files for j in tg_files if j in i]
    for item in matches:
        copy_files(join(raw_img_path, item), dest)
