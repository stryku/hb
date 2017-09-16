import socket
from request import request
from request.request_type import *
import sys
import utils


def create_request():
    if len(sys.argv) == 1 or sys.argv[1] == 'ping':
        return request.RequestFactory.create(RequestType.PING)

    if sys.argv[1] == 'extract':
        b64_file = utils.read_file_as_b64(sys.argv[2])
        content = {
            'filename': sys.argv[2],
            'file_data': b64_file.decode()
        }
        return request.RequestFactory.create_full(RequestType.EXTRACT_FROM_RECEIPT.name,
                                                  content)

    if sys.argv[1] == 'status':
        receipt_id = sys.argv[2]
        content = {
            'receipt_id': receipt_id
        }
        return request.RequestFactory.create_full(RequestType.GET_RECEIPT_STATUS.name,
                                                  content)

    if sys.argv[1] == 'text':
        receipt_id = sys.argv[2]
        content = {
            'receipt_id': receipt_id
        }
        return request.RequestFactory.create_full(RequestType.GET_RECEIPT_TEXT.name,
                                                  content)

    print("Unknown args: " + str(sys.argv))


def main():
    s = socket.socket()
    s.connect(("localhost", 9999))
    req = create_request()
    utils.send_msg(s, req)
    resp = utils.recv_msg(s)
    print('received response: ' + resp.decode())
    s.close()


if __name__ == '__main__':
    main()
