import os
import shutil
import tempfile

import scripts
import utils
from crypto.file_encryptor import EncryptedFile
from database import lite, tables
from database.tables_metadata import TableType
from image import image
from request.request_type import *
from response import response
from response.response_err_code import *
from strbot import strykubot


class PingRequestHandler:
    @staticmethod
    def handle(request_content, formatter):
        return formatter.format(ResponseErrorCode.OK,
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

    def format_success_response(self, tesseract_return, receipt_id, formatter):
        response_content = {
            'extracted_text': utils.to_string(tesseract_return['stdout']),
            'receipt_id': utils.to_string(receipt_id)
        }
        return formatter.format(ResponseErrorCode.OK,
                                response_content)

    def post_success_actions(self, file, tesseract_return):
        name_to_save = self.get_name_to_save(file)
        shutil.copy(file.name, 'data/received_images/' + name_to_save)
        db = lite.Db()
        db.execute("insert into " +
                   tables.get_table_name(TableType.RECEIPTS) +
                   " (name, oryginal_name) values ('" + name_to_save + "', '" + os.path.basename(file.name) + "')")
        inserted_id = db.last_id()
        command = "insert into " + \
                  tables.get_table_name(TableType.EXTRACTED_RECEIPTS_TEXTS_TABLE) + \
                  " (receipt_id, txt) values ('" + str(inserted_id) + "', ?)"
        db.get_cur().execute(command, (tesseract_return['stdout'],))
        db.commit()
        db.close()
        return inserted_id

    def handle(self, request_content, formatter):
        extracted_oryg_file = self.extract_to_tmp_image(request_content['filename'],
                                                        request_content['file_data'])
        preprocess_return = self.preprocess_image(extracted_oryg_file)
        if preprocess_return['ret_code'] != 0:
            return formatter.format(ResponseErrorCode.PREPROCESSING_FAILED,
                                    preprocess_return)

        tesseract_return = scripts.tesseract(self.preprocessed_image_name)
        if tesseract_return['ret_code'] != 0:
            return formatter.format(ResponseErrorCode.TESSERACT_FAILED,
                                    tesseract_return)

        receipt_id = self.post_success_actions(extracted_oryg_file, tesseract_return)
        return self.format_success_response(tesseract_return, receipt_id, formatter)


class GetReceiptStatusHandler:
    @staticmethod
    def handle(request_content, formatter):
        receipt_id = request_content['receipt_id']
        try:
            receipt_status_ret = lite.DbDataGetter.get_field(tables.get_table_name(TableType.RECEIPTS),
                                                             'status',
                                                             receipt_id)
            receipt_status = lite.ReceiptStatus(int(receipt_status_ret))
            response_content = {'receipt_status': receipt_status.name}
            return formatter.format(ResponseErrorCode.OK, response_content)

        except lite.NotFoundInDbException:
            return formatter.format(ResponseErrorCode.RECEIPT_ID_NOT_FOUND,
                                    {'receipt_id': receipt_id})


class GetReceiptTextHandler:
    @staticmethod
    def handle(request_content, formatter):
        receipt_id = request_content['receipt_id']
        try:
            table_name = tables.get_table_name(TableType.EXTRACTED_RECEIPTS_TEXTS_TABLE)
            extracted_recepit_text = lite.DbDataGetter.get_field(table_name,
                                                                 'txt',
                                                                 receipt_id,
                                                                 'receipt_id')
            response_content = {'receipt_text': extracted_recepit_text}
            return formatter.format(ResponseErrorCode.OK, response_content)

        except lite.NotFoundInDbException:
            return formatter.format(ResponseErrorCode.RECEIPT_ID_NOT_FOUND,
                                    {'receipt_id': receipt_id})


class GetForCorrectionHandler:
    @staticmethod
    def handle(request_content, formatter):
        receipt_id = request_content['receipt_id']
        try:
            filename = lite.DbDataGetter.get_field(tables.get_table_name(TableType.RECEIPTS),
                                                   'name',
                                                   receipt_id)

            table_name = tables.get_table_name(TableType.EXTRACTED_RECEIPTS_TEXTS_TABLE)
            extracted_receipt_text = lite.DbDataGetter.get_field(table_name,
                                                                 'txt',
                                                                 receipt_id,
                                                                 'receipt_id')

            filename = 'data/received_images/' + filename
            file_message_content = image.prepare_image_for_message(filename)
            response_content = {
                'file': file_message_content,
                'text': utils.b64encode(extracted_receipt_text)
            }
            return formatter.format(ResponseErrorCode.OK, response_content)

        except lite.NotFoundInDbException:
            return formatter.format(ResponseErrorCode.RECEIPT_ID_NOT_FOUND,
                                    {'receipt_id': receipt_id})


class CorrectTextHandler:
    @staticmethod
    def update_db(request_content, formatter):
        receipt_id = request_content['receipt_id']
        text = request_content['text']
        CorrectTextHandler.update_text(receipt_id, text)
        CorrectTextHandler.update_receipt(receipt_id)
        return formatter.format(ResponseErrorCode.OK, {})

    @staticmethod
    def update_text(receipt_id, text):
        lite.DbDataUpdater.update_field(tables.get_table_name(TableType.EXTRACTED_RECEIPTS_TEXTS_TABLE),
                                        'txt',
                                        text,
                                        receipt_id,
                                        'receipt_id')

    @staticmethod
    def update_receipt(receipt_id):
        lite.DbDataUpdater.update_field(tables.get_table_name(TableType.RECEIPTS),
                                        'status',
                                        lite.ReceiptStatus.CORRECTED.value,
                                        receipt_id)

    @staticmethod
    def update_repo(text):
        bot = strykubot.StrykuBot()
        bot.clone_tmp_repo('hb')
        bot.checkout_branch('str-bot-training_text')
        repo_dir = bot.get_repo_dir()
        tess_dir = repo_dir + '/image_processing/tesseract'
        tess_dir = os.path.abspath(tess_dir)
        training_text_filename = tess_dir + '/training_text.txt'
        encrypted_file = EncryptedFile(training_text_filename)
        encrypted_file.decrypt_to_file()
        with open(training_text_filename, 'a') as file:
            file.write('\n\n' + text)

        utils.run_process_split(tess_dir + '/run_trainer.sh ' + tess_dir)

        encrypted_file.encrypt_file(training_text_filename)
        encrypted_file.close()

        tessdata_filename = tess_dir + '/tessdata/hb.traineddata'
        encrypted_file.encrypt_file(tessdata_filename)
        encrypted_file.close()

        bot.add_all()
        bot.commit('update tesseract training text')
        bot.push_last_branch()

    @staticmethod
    def handle(request_content, formatter):
        try:
            resp = CorrectTextHandler.update_db(request_content, formatter)
            CorrectTextHandler.update_repo(request_content['text'])
            return resp

        except lite.NotFoundInDbException:
            return formatter.format(ResponseErrorCode.RECEIPT_ID_NOT_FOUND,
                                    {'receipt_id': request_content['receipt_id']})


class DbGetTablesHandler:
    @staticmethod
    def _tables_dicts_to_list(dicts_list):
        result = []
        for table_dict in dicts_list:
            result.append(table_dict['name'])

        return result

    @staticmethod
    def handle(request_content, formatter):
        tables_dicts = lite.Db().get_tables()
        tables_names = DbGetTablesHandler._tables_dicts_to_list(tables_dicts)
        return formatter.format(ResponseErrorCode.OK,
                                {'tables': str(tables_names)})


class RequestHandlerFactory:
    @staticmethod
    def create(request_type):
        return {
            RequestType.PING: PingRequestHandler(),
            RequestType.EXTRACT_FROM_RECEIPT: ExtractFromReceiptRequestHandler(),
            RequestType.GET_RECEIPT_STATUS: GetReceiptStatusHandler(),
            RequestType.GET_RECEIPT_TEXT: GetReceiptTextHandler(),
            RequestType.GET_FOR_CORRECTION: GetForCorrectionHandler(),
            RequestType.CORRECT_TEXT: CorrectTextHandler(),
            RequestType.DB_GET_TABLES: DbGetTablesHandler()
        }[request_type]


class RequestHandler:
    @staticmethod
    def handle(request_data):
        request_type = request_data['request_type']
        handler = RequestHandlerFactory.create(request_type)
        return handler.handle(request_data['request_content'],
                              response.ResponseFormatter(request_type))
