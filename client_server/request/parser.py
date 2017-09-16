import xml.etree.ElementTree as ET
import base64
from request.request_type import *


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


class ReceiptIdContentParser:
    @staticmethod
    def parse(data):
        receipt_id__el = data.find('receipt_id')
        return {
            'receipt_id': receipt_id__el.text,
        }


class RequestContentParserFactory:
    @staticmethod
    def create(request_type):
        return {
            RequestType.EXTRACT_FROM_RECEIPT: ExtractFromReceiptContentParser(),
            RequestType.PING: NoContentParser(),
            RequestType.GET_RECEIPT_STATUS: ReceiptIdContentParser(),
            RequestType.GET_RECEIPT_TEXT: ReceiptIdContentParser()
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
