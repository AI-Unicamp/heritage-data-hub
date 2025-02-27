"""Refine the raw json files by it's categories."""
from os.path import join
from helpers.auxiliar import (copy_files, get_nested, load_json,
                              read_files, check_bad_words)
from helpers.constants import (DATA_INTERIM_TEXT, DATA_PROCD_TEXT,
                               TARGET_LABELS, TL_BW)
from helpers import constants


def allocate(str_compare, field, origin_path, dest_path):
    """
    Allocate files from a specific path to another.

    The allocation is intended to separate the required data
    in specific folders.
    Args:
        str_compare: the string that will be compared with the existent in the
        json data.
        field: the specific field inside the json that will be the target,
        for example "classification", "denomination".
        origin_path: the root path of all files.
        dest_path: destination path where the classified files will be saved.
    """
    files = read_files(origin_path)
    for file in files:
        acr = file.split('.')[0].split('_')[0]
        acr_fields = getattr(constants, f'{acr}_FIELDS')
        data = load_json(origin_path, file)
        file_origin = join(origin_path, file)
        str_target = get_nested(data, acr_fields[field])
        if str_compare in str(str_target).lower() and \
                (file_origin not in dest_path):
            copy_files(file_origin, dest_path)


def allocate_img(str_compare, field, procd_txt, procd_img, model_db):
    """
    Allocate images related to JSON files that contains the specific label.

    The destination folder will be the spefified label compared.
    Args:
        str_compare: target specified label tha will be the folder's name.
        field: the specific field inside the json that will be the target,
        for example "classification", "denomination".
        procd_txt: the processed jsons path.
        procd_img: the processed images path.
        model_db: path that the images will be copied.
    """
    txt_files = read_files(procd_txt)
    img_files = read_files(procd_img)
    for file in txt_files:
        acr = file.split('.')[0].split('_')[0]
        acr_fields = getattr(constants, f'{acr}_FIELDS')
        data = load_json(procd_txt, file)
        str_target = get_nested(data, acr_fields[field])
        txt_name = file.split('.')[0]
        imgs = [i for i in img_files if txt_name in i]
        for item in imgs:
            img_path = join(procd_img, item)
            tgt = str(str_target).lower()
            if (str_compare in tgt) and (not any(tgt in i for i in TL_BW[str_compare])) and (not any(i in tgt for i in  TL_BW[str_compare])):
                copy_files(img_path, model_db)


def through_labels(target_list: list, field: str):
    """
    Go through all labels to get the related file.

    Args:
        target_list: list of the target labels.
        field: specific JSON field that will be used, for example denomination.

    """
    for label in target_list:
        allocate(label, field, DATA_INTERIM_TEXT, DATA_PROCD_TEXT)
