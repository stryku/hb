from dicttoxml import dicttoxml


class ResponseFormatter:
    def __init__(self, requested):
        self.requested = requested

    def format(self, code, content):
        response = {
            'requested': self.requested.name,
            'code': code.name,
            'content': content
        }
        return dicttoxml(response, custom_root='resp', attr_type=False)
