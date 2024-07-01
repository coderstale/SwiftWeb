class Response:
    def __init__(self, body='', status=200, headers=None):
        self.body = body
        self.status = status
        self.headers = headers or {}

    @staticmethod
    def render_template(template_name, context):
        from my_framework.template_engine import template_engine
        body = template_engine.render(template_name, context)
        return Response(body=body)
