import socket
import request
import request_handler
import response


def main():
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("localhost", 9999))
    s.listen(10)

    print("starting server...")

    while True:
        sc, address = s.accept()
        print("accepted " + str(address))

        message = sc.recv(1024*1024*1024)
        print("received: " + str(message))
        parsed_message = request.RequestMessageParser.parse(message)
        handler_response = request_handler.RequestHandler.handle(parsed_message)
        formatted_response = response.ResponseFormatter.format(handler_response)
        print("sending response: " + str(formatted_response))
        sc.send(formatted_response)
        sc.close()

    s.close()


if __name__ == '__main__':
    main()