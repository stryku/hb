import socket
from request import request
import sys
import utils


def create_request():
    if len(sys.argv) == 1 or sys.argv[1] == 'ping':
        return request.RequestFactory.create(request.RequestType.PING)

    if sys.argv[1] == 'extract':
        b64_file = utils.read_file_as_b64(sys.argv[2])
        content = {
            'filename': sys.argv[2],
            'file_data': b64_file.decode()
        }
        return request.RequestFactory.create_full(request.RequestType.EXTRACT_FROM_RECEIPT.name,
                                                  content)


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
