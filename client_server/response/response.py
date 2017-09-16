from dicttoxml import dicttoxml


class ResponseFormatter:
    @staticmethod
    def format_ready(response):
        return dicttoxml(response, custom_root='resp', attr_type=False)

    @staticmethod
    def format(code, content):
        response = {
            'code': code.name,
            'content': content
        }
        return ResponseFormatter.format_ready(response)
