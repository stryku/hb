import response
import request
import base64
import scripts
import tempfile


class PingRequestHandler:
    @staticmethod
    def handle(request_content):
        return response.ResponseFormatter.format(response.ResponseErrorCode.OK,
                                                 'pong')


class ExtractFromReceiptRequestHandler:
    def __init__(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.preprocessed_image_name = ''

    def extract_to_tmp_image(self, oryginal_name, b64_data):
        file = open(self.temp_dir.name + '/' + oryginal_name)
        file.write(base64.b64decode(b64_data))
        return file

    def preprocess_image(self, oryginal_file):
        self.preprocessed_image_name = 'preprocessed_' + oryginal_file.name
        return scripts.textcleaner(oryginal_file, self.preprocessed_image_name)

    def format_success_response(self, tesseract_return):
        response_content = {
            'extracted_text': tesseract_return['stdout']
        }
        return response.ResponseFormatter.format(response.ResponseErrorCode.OK,
                                                 response_content)

    def handle(self, request_content):
        extracted_oryg_file = self.extract_to_tmp_image(request_content['filename'],
                                                        request_content['file_data'])
        preprocess_return = self.preprocess_image(extracted_oryg_file)
        if preprocess_return['ret_code'] != 0:
            return response.ResponseFormatter.format(response.ResponseErrorCode.PREPROCESSING_FAILED,
                                                     preprocess_return)

        tesseract_return = scripts.tesseract(self.preprocessed_image_name)
        if tesseract_return['ret_code'] != 0:
            return response.ResponseFormatter.format(response.ResponseErrorCode.TESSERACT_FAILED,
                                                     tesseract_return)

        return self.format_success_response(tesseract_return)


class RequestHandlerFactory:
    @staticmethod
    def create(request_type):
        return {
            request.RequestType.PING: PingRequestHandler()
        }[request_type]


class RequestHandler:
    @staticmethod
    def handle(request_data):
        handler = RequestHandlerFactory.create(request_data['request_type'])
        return handler.handle(request_data['request_content'])
