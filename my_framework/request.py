from urllib.parse import parse_qs

class Request:
    def __init__(self, method, path, headers, body):
        self.method = method
        self.path = path
        self.headers = headers
        self.body = body
        self.session_id = None
        self.session = {}
        self.db = None
        self.query_params = self.parse_query_params()
        self.form_data = self.parse_form_data()

    def parse_query_params(self):
        query_string = self.path.split('?', 1)[-1] if '?' in self.path else ''
        return parse_qs(query_string)

    def parse_form_data(self):
        content_type = self.headers.get('Content-Type', '')
        if content_type == 'application/x-www-form-urlencoded':
            return parse_qs(self.body.decode('utf-8'))
        return {}
