from enum import Enum
import xml.etree.ElementTree as ET
import base64


class RequestType(Enum):
    UNDEF = 0
    EXTRACT_FROM_RECEIPT = 1
    PING = 2


class NoContentParser:
    @staticmethod
    def parse(data):
        return {}


class ExtractFromReceiptContentParser:
    @staticmethod
    def parse(data):
        return {'image': base64.b64decode(data)}


class RequestContentParserFactory:
    @staticmethod
    def create(request_type):
        return {
            RequestType.EXTRACT_FROM_RECEIPT: ExtractFromReceiptContentParser(),
            RequestType.PING: NoContentParser()
        }[request_type]


class RequestMessageParser:
    @staticmethod
    def parse(data):
        tree = ET.parse(data)
        root = tree.getroot()
        request_type_el = root.find('request_type')
        request_content_el = root.find('request_content')

        request_type = RequestType[request_type_el.text]
        raw_content = request_content_el.text
        content_parser = RequestContentParserFactory.create(request_type)
        request_content = content_parser.parse(raw_content)

        return {
            'request_type': request_type,
            'request_content': request_content
        }
