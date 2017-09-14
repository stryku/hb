import socket
import request
import sys
import utils


def create_request():
    if len(sys.argv) == 1 or sys.argv[1] == 'ping':
        return request.RequestFactory.create(request.RequestType.PING)

    if sys.argv[1] == 'extract':
        b64_file = utils.read_file_as_b64(sys.argv[2])
        return request.RequestFactory.create_full(request.RequestType.EXTRACT_FROM_RECEIPT,
                                                  b64_file)


def main():
    s = socket.socket()
    s.connect(("localhost", 9999))
    req = create_request()
    s.send(req)
    resp = s.recv(1024)
    print('received response: ' + str(resp))
    s.close()


if __name__ == '__main__':
    main()