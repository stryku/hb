from response import ResponseErrorCode
import request

class PingRequestHandler:
    def handle(self, request_content):
        return {
            'code': ResponseErrorCode.OK.name,
            'content': 'pong'
        }


class RequestHandlerFactory:
    @staticmethod
    def create(request_type):
        return {
            request.RequestType.PING: PingRequestHandler()
        }[request_type]


class RequestHandler:
    @staticmethod
    def handle(request_data):
        handler = RequestHandlerFactory.create(request_data['request_type'])
        return handler.handle(request_data['request_content'])
