"""Creates the project database."""

from os.path import isdir
from os import listdir, makedirs
from posixpath import join
from difPy import dif
import click

from modules.classify_jsons import allocate, allocate_img, through_labels
from modules.jsons_fetcher import get_jsons
from modules.images_fetcher import get_images
from modules.classify_images import classify_images
from helpers.auxiliar import read_files
from helpers.constants import (DATA_INTERIM_IMAGES, DATA_PROCD_MODEL,
                               DATA_RAW_JSONS, DATA_RAW_IMAGES,
                               DATA_INTERIM_TEXT, DATA_PROCD_TEXT,
                               DATA_PROCD_IMAGES, TARGET_LABELS, TESAURO,
                               TL_JOINED)


class NaturalOrderGroup(click.Group):
    """Command group to list subcommands in the order they were added."""

    def list_commands(self, ctx):
        """List command names as they are in commands dict."""
        ctx.ensure_object(dict)
        return self.commands.keys()


@click.group(cls=NaturalOrderGroup)
def main():
    """Create database."""


@main.command('fetch_jsons')
def fetch_jsons():
    """Download JSON files from museum's web page."""
    print("Downloading JSON files...")
    get_jsons()
    print(f"JSON files download has been completed - # files: {len(read_files(DATA_RAW_JSONS))} .\n")


@main.command('fetch_images')
def fetch_images():
    """
    Download images from museum's web page.

    The images comes from each museum based on the URLs at the
    downloaded JSON files.
    """
    print("Downloading images...")
    get_images()
    print("Images download has been completed successifully.\n")


@main.command('classify_jsons_by_thesaurus')
@click.option('--thesauro', '-t', type=click.Choice(TESAURO), default='05')
@click.pass_context
def classify_jsons_by_thesaurus(ctx, thesauro):
    """
    Classify JSON files that matches the thesaurus type.

    In these case will match the files in data/raw/jsons folder and copy
    to data/interim/jsons.
    """
    if not isdir(DATA_RAW_JSONS):
        ctx.invoke(fetch_jsons)
    try:
        print(f"Classifying JSON files by thesaurus {thesauro}...")
        allocate(thesauro, 'classification', DATA_RAW_JSONS, DATA_INTERIM_TEXT)
        print(f"JSON files classification by thesaurus {thesauro} has been completed successifully.\n")
    except FileNotFoundError:
        print("There's no data to parse.\n")


@main.command('classify_imgs_by_thesaurus')
@click.pass_context
def classify_imgs_by_thesaurus(ctx):
    """Classifies the interim images by thesaurus."""
    if not isdir(DATA_RAW_IMAGES):
        ctx.invoke(fetch_images)
    if not isdir(DATA_INTERIM_TEXT):
        ctx.invoke(classify_jsons_by_thesaurus)
    try:
        print("Classifying images by thesaurus...")
        classify_images(DATA_RAW_IMAGES, DATA_INTERIM_TEXT, DATA_INTERIM_IMAGES)
        print("Images classification by thesaurus has been completed successifully.\n")
        
    except FileNotFoundError:
        print("There's no data to parse.\n")


@main.command('classify_jsons_by_labels')
@click.option('--label_list', '-l',
              help='List of labels to classify the JSON files.',
              default=TARGET_LABELS,
              multiple=True)
@click.option('--field', '-f',
              default='denomination',
              help='Field containing the target text to compare with target labels.')
@click.pass_context
def classify_jsons_by_labels(ctx, label_list, field):
    """
    Classifies the interim JSON files accordingly to the labels list.

    Will classify the JSON files from interim folder to processed one
    that matches the specified labels.
    """
    if not isdir(DATA_INTERIM_TEXT):
        ctx.invoke(classify_jsons_by_thesaurus)
    try:
        print("Classifying JSON files by labels...")
        through_labels(label_list, field)
        print("JSON files classification by labels has been completed successifully.\n")
    except FileNotFoundError:
        print("There's no data to parse.\n")


@main.command('classify_imgs_by_labels')
@click.pass_context
def classify_imgs_by_labels(ctx):
    """
    Classify images by target labels.

    The classification is made by matching the JSON files with the target
    labels. If the denomination description contains the target label the
    image related to the item is then allocated to processed images folder.
    """
    if not isdir(DATA_RAW_IMAGES):
        ctx.invoke(fetch_images)
    if not isdir(DATA_INTERIM_IMAGES):
        ctx.invoke(classify_imgs_by_thesaurus)
    if not isdir(DATA_PROCD_TEXT):
        ctx.invoke(classify_jsons_by_labels)
    try:
        print("Classifying images by labels...")
        if not isdir(DATA_PROCD_IMAGES):
            makedirs(DATA_PROCD_IMAGES, exist_ok=True)
        classify_images(DATA_RAW_IMAGES, DATA_PROCD_TEXT, DATA_PROCD_IMAGES)
        print("Images classification by labels has been completed successifully.\n")
    except FileNotFoundError:
        print("There's no data to parse.\n")


@main.command('duplicate_remover')
@click.option('--rm_path', '-d', 
              help='Path of the directory containing folders with the duplicated images',
              default=DATA_PROCD_MODEL)
def duplicate_remover(rm_path):
    """
    Remove duplicated images on a specified folder.

    Args:
        rm_path: directory containing all labeled folders with the processed 
        images with possible duplicated ones, in data/processed/modeldb.
    """
    if isdir(rm_path):
        for folder in listdir(rm_path):
            if click.confirm(
                    'Will remove all duplicated images. Would you like to continue?',
                    default=True):
                print('Removing duplicated images...')
                dif(folder, delete=True)  # pylint: disable=no-member
                print('Duplicated images have been removed successifully.\n')
    else:
        print(
            'Target folder does not exist.'
            'Make the database download and preprocessing first.\n')


@main.command('create_model_db')
@click.option('--labels', '-j',
              help='List of labels that will be the classified folders.',
              default=TL_JOINED,
              multiple=True)
@click.option('--field', '-f',
              help='Text field to compare with the target labels.',
              default='denomination')
@click.pass_context
def create_model_db(ctx, labels, field):
    """
    Model database creation by each folder label.

    Aims to create the database input version for the model.
    """
    print("-----------------------------------------------------------------------")
    print("-                    Building the whole database                      -")
    print("-----------------------------------------------------------------------\n")
    if not isdir(DATA_RAW_JSONS):
        makedirs(DATA_RAW_JSONS, exist_ok=True)
        ctx.invoke(fetch_jsons)
    if not isdir(DATA_INTERIM_TEXT):
        makedirs(DATA_INTERIM_TEXT, exist_ok=True)
        ctx.invoke(classify_jsons_by_labels)
    if not isdir(DATA_INTERIM_IMAGES):
        makedirs(DATA_INTERIM_IMAGES, exist_ok=True)
        ctx.invoke(classify_imgs_by_labels)
    if not isdir(DATA_PROCD_TEXT):
        makedirs(DATA_PROCD_TEXT, exist_ok=True)
        ctx.invoke(classify_jsons_by_labels)
    if not isdir(DATA_PROCD_IMAGES):
        makedirs(DATA_PROCD_IMAGES, exist_ok=True)
        print("Classifying images by labels...")
        classify_images(DATA_RAW_IMAGES, DATA_PROCD_TEXT, DATA_PROCD_IMAGES)
        print("Images classification by labels has been completed successifully.\n")
    if not isdir(DATA_PROCD_MODEL):
        makedirs(DATA_PROCD_MODEL, exist_ok=True)
        print("Creating the images database by folders...")
        for item in labels:
            dest_folder = join(DATA_PROCD_MODEL, item[1])
            if not isdir(dest_folder):
                makedirs(dest_folder, exist_ok=True)
            allocate_img(item[0], field, DATA_PROCD_TEXT, DATA_PROCD_IMAGES, dest_folder)
        print("Images database by folders has been created successifully.\n")
    else:
        print('Processed model database already exists.')

    print('Removing duplicated images...')
    ctx.invoke(classify_jsons_by_labels)
    print('Duplicated images has been removed successifully.')

    print("DONE: Database has been completed successifully.\n")

if __name__ == '__main__':
    main()  # pylint: disable=no-value-for-parameter
