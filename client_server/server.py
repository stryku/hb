import socket
import request
import request_handler
import response


def main():
    s = socket.socket()
    s.bind(("localhost", 9999))
    s.listen(10)

    print("starting server...")

    while True:
        sc, address = s.accept()
        print("accepted " + str(address))

        message = sc.recv()
        print("received: " + message)
        parsed_message = request.RequestMessageParser.parse(message)
        handler_response = request_handler.RequestHandler.handle(parsed_message)
        formatted_response = response.ResponseFormatter.format(handler_response)
        print("sending response: " + formatted_response)
        sc.send(formatted_response)
        sc.close()

    s.close()


if __name__ == '__main__':
    main()