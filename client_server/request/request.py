from enum import Enum
import xml.etree.ElementTree as ET
import base64
from dicttoxml import dicttoxml


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
        filename_el = data.find('filename')
        file_data_el = data.find('file_data')
        return {
            'filename': filename_el.text,
            'file_data': base64.b64decode(file_data_el.text)
        }


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
        req = ET.fromstring(data.decode('ascii'))
        request_type_el = req.find('request_type')
        request_content_el = req.find('request_content')

        request_type = RequestType[request_type_el.text]
        raw_content = request_content_el
        content_parser = RequestContentParserFactory.create(request_type)
        request_content = content_parser.parse(raw_content)

        return {
            'request_type': request_type,
            'request_content': request_content
        }


class RequestFactory:
    @staticmethod
    def create_full(req_type, content):
        req = {
            'request_type': req_type,
            'request_content': content
        }
        return dicttoxml(req, custom_root='req', attr_type=False)

    @staticmethod
    def create(req_type):
        return RequestFactory.create_full(req_type.name, '')
