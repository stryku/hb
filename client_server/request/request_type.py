from enum import Enum


class RequestType(Enum):
    UNDEF = 0
    EXTRACT_FROM_RECEIPT = 1
    PING = 2
