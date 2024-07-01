from http.server import BaseHTTPRequestHandler, HTTPServer
from .request import Request
from urllib.parse import unquote
from http.cookies import SimpleCookie
from sqlalchemy.orm import sessionmaker
from my_framework.db import engine, Base
from my_framework.routing import get_handler
from my_framework.request import Request
from my_framework.response import Response
from my_framework.middleware import middleware_manager
from my_framework.session import session_manager
from my_framework.template_engine import render_template
from logging_config import logger
import os

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.handle_request()

    def do_POST(self):
        self.handle_request()

    def handle_request(self):
        try:
            logger.info(f"Handling request for path: {self.path}")
            self.path = unquote(self.path)

            if self.path.startswith('/static/'):
                self.serve_static_file()
            elif self.path.startswith('/'):
                self.serve_template_file(self.path[1:])   
            else:
                content_length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_length) if content_length > 0 else b''
                request = Request(self.command, self.path, self.headers, body)

                request = middleware_manager.process_request(request)
                if not request:
                    self.send_response(400)
                    self.end_headers()
                    self.wfile.write(b"Bad Request")
                    return

                self.handle_session(request)
                logger.info(f"Session ID: {request.session_id}")

                request.db = SessionLocal()

                handler = get_handler(request.path)
                if handler:
                    response = handler(request)
                    if not isinstance(response, Response):
                        response = Response(body=response)
                    response = middleware_manager.process_response(request, response)
                    logger.info(f"Sending response: {response.body[:100]}")
                    self.send_response(response.status)
                    self.send_header('Content-Type', 'text/html; charset=utf-8')
                    self.send_header('Content-Length', str(len(response.body.encode('utf-8'))))
                    for key, value in response.headers.items():
                        self.send_header(key, value)
                    self.send_header('Set-Cookie', f'session_id={request.session_id}; Path=/')
                    self.end_headers()
                    self.wfile.write(response.body.encode('utf-8'))
                else:
                    self.send_response(404)
                    self.end_headers()
                    self.wfile.write(b"Not Found")

                request.db.close()
        except Exception as e:
            logger.error(f"Error handling request: {e}", exc_info=True)
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b"Internal Server Error")

    def handle_session(self, request):
        try:
            cookie = SimpleCookie(self.headers.get('Cookie'))
            session_id = cookie.get('session_id')
            if session_id is None or session_id.value not in session_manager.sessions:
                session_id = session_manager.create_session()
                request.session_id = session_id
                logger.info(f"New session created: {session_id}")
            else:
                request.session_id = session_id.value
                logger.info(f"Existing session retrieved: {session_id.value}")

            request.session = session_manager.get_session(request.session_id)
        except Exception as e:
            logger.error(f"Error handling session: {e}")

    def serve_static_file(self):
        try:
            logger.info(f"Serving static file for path: {self.path}")
            static_file_path = os.path.join(os.path.dirname(__file__), '..', 'static', self.path[8:])
            if os.path.exists(static_file_path) and os.path.isfile(static_file_path):
                self.send_response(200)
                mime_type = self.guess_type(static_file_path)
                self.send_header('Content-Type', mime_type)
                with open(static_file_path, 'rb') as file:
                    static_content = file.read()
                    self.send_header('Content-Length', str(len(static_content)))
                    self.end_headers()
                    self.wfile.write(static_content)
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"Static file not found")
        except Exception as e:
            logger.error(f"Error serving static file: {e}", exc_info=True)
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b"Internal Server Error")

    def serve_template_file(self, template_name):
        try:
            logger.info(f"Serving template file for path: {self.path}")
            template_file_path = os.path.join(os.path.dirname(__file__), '..', 'templates', template_name)
            if os.path.exists(template_file_path) and os.path.isfile(template_file_path):
                self.send_response(200)
                mime_type = self.guess_type(template_file_path)
                self.send_header('Content-Type', mime_type)
                with open(template_file_path, 'rb') as file:
                    template_content = file.read()
                    self.send_header('Content-Length', str(len(template_content)))
                    self.end_headers()
                    self.wfile.write(template_content)
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"Template file not found")
        except Exception as e:
            logger.error(f"Error serving template file: {e}", exc_info=True)
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b"Internal Server Error")

    def guess_type(self, path):
        ext = os.path.splitext(path)[1]
        return {
            '.html': 'text/html',
            '.css': 'text/css',
            '.js': 'application/javascript',
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.gif': 'image/gif'
        }.get(ext, 'application/octet-stream')

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logger.info(f'Starting httpd server on port {port}')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
