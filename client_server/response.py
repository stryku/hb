from dicttoxml import dicttoxml
from enum import Enum


class ResponseErrorCode(Enum):
    UNDEF = 0
    OK = 1
    NOK = 2
    PREPROCESSING_FAILED = 3
    TESSERACT_FAILES = 4


class ResponseFormatter:
    @staticmethod
    def format_ready(response):
        return dicttoxml(response, custom_root='resp', attr_type=False)

    @staticmethod
    def format(code, content):
        response = {
            'code': code.name,
            'content': content
        }
        return ResponseFormatter.format_ready(response)
