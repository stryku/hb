import tempfile
from os import path


def create_tmp_file(base_name):
    filename, extension = path.split(base_name)
    return tempfile.TemporaryFile(suffix=extension)