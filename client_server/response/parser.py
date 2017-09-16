import base64
import xml.etree.ElementTree as ET
from response.response_err_code import *
from request.request_type import *
import lite
from image import image


def get_resp_code(resp):
    el = resp.find('code')
    return ResponseErrorCode[el.text]


class ProcessOutputParser:
    @staticmethod
    def parse(content):
        ret_val_el = content.find('ret_val')
        out_el = content.find('out')
        err_el = content.find('err')

        return {
            'out': out_el.text,
            'err': err_el.text,
            'ret_val': ret_val_el.text
        }


class NoContentResponseParser:
    @staticmethod
    def parse(resp):
        return '<<NO CONTENT>>'


class PingResponseParser:
    @staticmethod
    def parse(resp):
        return 'pong'


class ExtractFromReceiptResponseParser:
    @staticmethod
    def parse(resp):
        code = get_resp_code(resp)
        if code in [ResponseErrorCode.TESSERACT_FAILED, ResponseErrorCode.PREPROCESSING_FAILED]:
            return ProcessOutputParser.parse(resp.find('content'))

        content_el = resp.find('content')
        return {
            'extracted_text': content_el.find('extracted_text').text,
            'receipt_id': content_el.find('receipt_id').text
        }


class ReceiptNotFoundParserGuard:
    @staticmethod
    def parse(resp, content_parser):
        code = get_resp_code(resp)
        if code == ResponseErrorCode.RECEIPT_ID_NOT_FOUND:
            return 'Receipt with such ID %s not found' % resp.find('content').find('receipt_id').text

        content_el = resp.find('content')
        return content_parser(content_el)


class GetReceiptStatusResponseParser:
    @staticmethod
    def parse_content(content_el):
        return {
            'status': lite.ReceiptStatus[content_el.find('receipt_status').text]
        }

    @staticmethod
    def parse(resp):
        return ReceiptNotFoundParserGuard.parse(resp, GetReceiptStatusResponseParser.parse_content)


class GetReceiptTextResponseParser:
    @staticmethod
    def parse_content(content_el):
        return {
            'text': content_el.find('text').text
        }

    @staticmethod
    def parse(resp):
        return ReceiptNotFoundParserGuard.parse(resp, GetReceiptTextResponseParser.parse_content)


class GetForCorrectionResponseParser:
    @staticmethod
    def parse_content(content_el):
        return {
            'file': image.extract_image_from_element(content_el.find('file')),
            'text': base64.b64decode(content_el.find('text').text)
        }

    @staticmethod
    def parse(resp):
        return ReceiptNotFoundParserGuard.parse(resp, GetForCorrectionResponseParser.parse_content)


class ResponseContentParserFactory:
    @staticmethod
    def create(requested):
        return {
            RequestType.PING: PingResponseParser(),
            RequestType.EXTRACT_FROM_RECEIPT: ExtractFromReceiptResponseParser(),
            RequestType.GET_RECEIPT_STATUS: GetReceiptStatusResponseParser(),
            RequestType.GET_RECEIPT_TEXT: GetReceiptTextResponseParser(),
            RequestType.GET_FOR_CORRECTION: GetForCorrectionResponseParser(),
            RequestType.CORRECT_TEXT: NoContentResponseParser()
        }[requested]


class ResponseMessageParser:
    @staticmethod
    def parse(data):
        resp = ET.fromstring(data.decode('UTF-8'))
        code_el = resp.find('code')
        requested_el = resp.find('requested')

        code = ResponseErrorCode[code_el.text]
        requested = RequestType[requested_el.text]
        content_parser = ResponseContentParserFactory.create(requested)
        request_content = content_parser.parse(resp)

        return {
            'requested': requested,
            'code': code,
            'content': request_content
        }
