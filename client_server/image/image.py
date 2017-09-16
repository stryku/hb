import base64
import utils
from os import path


def extract_image_from_element(el):
    filename_el = el.find('filename')
    file_data_el = el.find('file_data')
    return {
        'filename': filename_el.text,
        'file_data': base64.b64decode(file_data_el.text)
    }


def prepare_image_for_message(filename):
    b64_file = utils.read_file_as_b64(filename)
    return {
        'filename': path.basename(filename),
        'file_data': b64_file.decode()
    }


def save_image_from_dict(img_dict):
    file = open(img_dict['filename'], 'wb')
    file.write(img_dict['file_data'])
    file.close()
