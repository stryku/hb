import xml.etree.ElementTree as ET
from request.request_type import *
import utils


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
            'file_data': utils.b64decode(file_data_el.text)
        }


class ReceiptIdContentParser:
    @staticmethod
    def parse(data):
        receipt_id_el = data.find('receipt_id')
        return {
            'receipt_id': receipt_id_el.text,
        }


class CorrectTextContentParser:
    @staticmethod
    def parse(data):
        receipt_id_el = data.find('receipt_id')
        text_el = data.find('text')
        return {
            'receipt_id': receipt_id_el.text,
            'text': utils.b64decodestr(text_el.text)
        }


class AddExpansesList:
    @staticmethod
    def parse(data):
        return {
            'expanses_list': data.find('expanses_list').text
        }


class RequestContentParserFactory:
    @staticmethod
    def create(request_type):
        return {
            RequestType.EXTRACT_FROM_RECEIPT: ExtractFromReceiptContentParser(),
            RequestType.PING: NoContentParser(),
            RequestType.GET_RECEIPT_STATUS: ReceiptIdContentParser(),
            RequestType.GET_RECEIPT_TEXT: ReceiptIdContentParser(),
            RequestType.GET_FOR_CORRECTION: ReceiptIdContentParser(),
            RequestType.CORRECT_TEXT: CorrectTextContentParser(),
            RequestType.DB_GET_TABLES: NoContentParser(),
            RequestType.ADD_EXPENSES_LIST: AddExpansesList()
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
