import socket
import sys
import traceback
import utils
from request import parser
from request import handler


def main():
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((sys.argv[1], 9999))
    s.listen(10)

    print("starting server...")

    while True:
        try:
            while True:
                sc, address = s.accept()
                print("accepted " + str(address))

                message = utils.recv_msg(sc)
                parsed_message = parser.RequestMessageParser.parse(message)
                handler_response = handler.RequestHandler.handle(parsed_message)
                utils.send_msg(sc, handler_response)
                sc.close()

            s.close()
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
            print(''.join('!! ' + line for line in lines))


if __name__ == '__main__':
    main()