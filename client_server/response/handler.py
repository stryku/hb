from pprint import pprint

from image import image
from request.request_type import RequestType
from response import parser


class PrintResponseHandler:
    @staticmethod
    def handle(response):
        pprint(response)


class GetForCorrectionResponseHandler:
    @staticmethod
    def handle(response):
        img = response['content']['file']
        image.save_image_from_dict(img)
        txt_file = open(img['filename'] + '.txt', 'wb')
        txt_file.write(response['content']['text'])
        txt_file.close()


class ResponseHandlerFactory:
    @staticmethod
    def create(request_type):
        return {
            RequestType.PING: PrintResponseHandler(),
            RequestType.EXTRACT_FROM_RECEIPT: PrintResponseHandler(),
            RequestType.GET_RECEIPT_STATUS: PrintResponseHandler(),
            RequestType.GET_RECEIPT_TEXT: PrintResponseHandler(),
            RequestType.GET_FOR_CORRECTION: GetForCorrectionResponseHandler(),
            RequestType.CORRECT_TEXT: PrintResponseHandler(),
            RequestType.DB_GET_TABLES: PrintResponseHandler(),
            RequestType.ADD_EXPENSES_LIST: PrintResponseHandler()
        }[request_type]


class ResponseHandler:
    @staticmethod
    def handle(response_data):
        parsed_response = parser.ResponseMessageParser.parse(response_data)
        handler = ResponseHandlerFactory.create(parsed_response['requested'])
        handler.handle(parsed_response)
