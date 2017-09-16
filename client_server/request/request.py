from dicttoxml import dicttoxml


class RequestFactory:
    @staticmethod
    def create_full(req_type, content):
        req = {
            'request_type': req_type,
            'request_content': content
        }
        return dicttoxml(req, custom_root='req', attr_type=False)

    @staticmethod
    def create(req_type):
        return RequestFactory.create_full(req_type.name, '')
