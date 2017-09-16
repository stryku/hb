from enum import Enum


class ResponseErrorCode(Enum):
    UNDEF = 0
    OK = 1
    NOK = 2
    PREPROCESSING_FAILED = 3
    TESSERACT_FAILED = 4
    RECEIPT_ID_NOT_FOUND = 5
    MULTIPLE_RECEIPTS_FOUND = 5
