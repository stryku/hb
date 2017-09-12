from dicttoxml import dicttoxml
from enum import Enum


class ResponseErrorCode(Enum):
    UNDEF = 0
    OK = 1
    NOK = 2


class ResponseFormatter:
    @staticmethod
    def format(response):
        return dicttoxml([response], custom_root='resp', attr_type=False)
