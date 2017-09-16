import scripts
import tempfile
import os
import utils
import shutil
import lite
from request.request_type import *
from response.response_err_code import *
from response import response


class PingRequestHandler:
    @staticmethod
    def handle(request_content):
        return response.ResponseFormatter.format(ResponseErrorCode.OK,
                                                 'pong')


class ExtractFromReceiptRequestHandler:
    def __init__(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.preprocessed_image_name = ''

    def get_name_to_save(self, file):
        return str(utils.current_milli_time()) + '_' + os.path.basename(file.name)

    def extract_to_tmp_image(self, oryginal_name, data):
        file = open(self.temp_dir.name + '/' + oryginal_name, 'wb')
        file.write(data)
        file.close()
        return file

    def preprocess_image(self, oryginal_file):
        name = os.path.basename(oryginal_file.name)
        path = os.path.dirname(oryginal_file.name)
        self.preprocessed_image_name = path + '/preprocessed_' + name + '.png'
        return scripts.textcleaner(oryginal_file.name, self.preprocessed_image_name)

    def format_success_response(self, tesseract_return, receipt_id):
        response_content = {
            'extracted_text': utils.to_string(tesseract_return['stdout']),
            'receipt_id': utils.to_string(receipt_id)
        }
        return response.ResponseFormatter.format(ResponseErrorCode.OK,
                                                 response_content)

    def post_success_actions(self, file, tesseract_return):
        name_to_save = self.get_name_to_save(file)
        shutil.copy(file.name, 'data/received_images/' + name_to_save)
        db = lite.Db()
        db.execute("insert into " +
                   lite.RECEIPTS_TABLE +
                   " (name, oryginal_name) values ('" + os.path.basename(file.name) + "', '" + name_to_save + "')")
        inserted_id = db.last_id()
        command = "insert into " + \
                  lite.EXTRACTED_RECEIPTS_TEXTS_TABLE + \
                  " (receipt_id, txt) values ('" + str(inserted_id) + "', ?)"
        db.get_cur().execute(command, (tesseract_return['stdout'],))
        db.commit()
        db.close()
        return inserted_id

    def handle(self, request_content):
        extracted_oryg_file = self.extract_to_tmp_image(request_content['filename'],
                                                        request_content['file_data'])
        preprocess_return = self.preprocess_image(extracted_oryg_file)
        if preprocess_return['ret_code'] != 0:
            return response.ResponseFormatter.format(ResponseErrorCode.PREPROCESSING_FAILED,
                                                     preprocess_return)

        tesseract_return = scripts.tesseract(self.preprocessed_image_name)
        if tesseract_return['ret_code'] != 0:
            return response.ResponseFormatter.format(ResponseErrorCode.TESSERACT_FAILED,
                                                     tesseract_return)

        receipt_id = self.post_success_actions(extracted_oryg_file, tesseract_return)
        return self.format_success_response(tesseract_return, receipt_id)


class RequestHandlerFactory:
    @staticmethod
    def create(request_type):
        return {
            RequestType.PING: PingRequestHandler(),
            RequestType.EXTRACT_FROM_RECEIPT: ExtractFromReceiptRequestHandler(),
        }[request_type]


class RequestHandler:
    @staticmethod
    def handle(request_data):
        handler = RequestHandlerFactory.create(request_data['request_type'])
        return handler.handle(request_data['request_content'])
