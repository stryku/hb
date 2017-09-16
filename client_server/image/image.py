import base64
import xml.etree.ElementTree as ET
import utils
from os import path


def extract_iamge_from_message(message):
    root = ET.fromstring(message.decode('ascii'))
    filename_el = root.find('filename')
    file_data_el = root.find('file_data')
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
