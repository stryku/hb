from enum import Enum


class RequestType(Enum):
    UNDEF = 0
    EXTRACT_FROM_RECEIPT = 1
    PING = 2
    GET_RECEIPT_STATUS = 3
    GET_RECEIPT_TEXT = 4
    GET_FOR_CORRECTION = 5
    CORRECT_TEXT = 6
    STATUS = 7
    DB_GET_TABLE = 8
    DB_GET_TABLES = 9
    ADD_EXPENSES_LIST = 10
