import os


def create_directories(directories):
    """Ensure that a list of directories exists."""
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
