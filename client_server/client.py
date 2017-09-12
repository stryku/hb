import socket


def main():
    s = socket.socket()
    s.connect(("localhost", 9999))
    ping_message = b'<?xml version="1.0"?><req><request_type>PING</request_type>\n<request_content>content</request_content></req>'
    s.send(ping_message)
    resp = s.recv(1024)
    print('received response: ' + str(resp))
    s.close()


if __name__ == '__main__':
    main()