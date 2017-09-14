import socket
import request


def main():
    s = socket.socket()
    s.connect(("localhost", 9999))
    req = request.RequestFactory.create(request.RequestType.PING)
    s.send(req)
    resp = s.recv(1024)
    print('received response: ' + str(resp))
    s.close()


if __name__ == '__main__':
    main()