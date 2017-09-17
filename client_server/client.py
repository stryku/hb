import socket
from request import request
from request.request_type import *
import sys
import utils
from image import image
from response import handler


def create_request():
    if len(sys.argv) == 2 or sys.argv[2] == 'ping':
        return request.RequestFactory.create(RequestType.PING)

    if sys.argv[2] == 'extract':
        filename = sys.argv[3]
        content = image.prepare_image_for_message(filename)
        return request.RequestFactory.create_full(RequestType.EXTRACT_FROM_RECEIPT.name,
                                                  content)

    if sys.argv[2] == 'status':
        receipt_id = sys.argv[3]
        content = {
            'receipt_id': receipt_id
        }
        return request.RequestFactory.create_full(RequestType.GET_RECEIPT_STATUS.name,
                                                  content)

    if sys.argv[2] == 'text':
        receipt_id = sys.argv[3]
        content = {
            'receipt_id': receipt_id
        }
        return request.RequestFactory.create_full(RequestType.GET_RECEIPT_TEXT.name,
                                                  content)

    if sys.argv[2] == 'get_for_correction' or sys.argv[2] == 'gfc':
        receipt_id = sys.argv[3]
        content = {
            'receipt_id': receipt_id
        }
        return request.RequestFactory.create_full(RequestType.GET_FOR_CORRECTION.name,
                                                  content)

    if sys.argv[2] == 'correct':
        receipt_id = sys.argv[3]
        txt_filename = sys.argv[4]
        content = {
            'receipt_id': receipt_id,
            'text': utils.read_file_as_b64(txt_filename)
        }
        return request.RequestFactory.create_full(RequestType.CORRECT_TEXT.name,
                                                  content)

    print("Unknown args: " + str(sys.argv))


def main():
    s = socket.socket()
    s.connect((sys.argv[1], 9999))
    req = create_request()
    utils.send_msg(s, req)
    resp = utils.recv_msg(s)
    handler.ResponseHandler.handle(resp)
    #print('received response: ' + resp.decode())
    s.close()


if __name__ == '__main__':
    main()
