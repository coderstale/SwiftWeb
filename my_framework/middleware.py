class MiddlewareManager:
    def __init__(self):
        self.middlewares = []

    def add_middleware(self, middleware):
        self.middlewares.append(middleware)

    def process_request(self, request):
        for middleware in self.middlewares:
            request = middleware.process_request(request)
            if not request:
                break
        return request

    def process_response(self, request, response):
        for middleware in self.middlewares:
            response = middleware.process_response(request, response)
        return response


middleware_manager = MiddlewareManager()
