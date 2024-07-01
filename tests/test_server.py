import pytest
from http.server import HTTPServer
from my_framework.server import RequestHandler

@pytest.fixture
def http_server():
    server_address = ('', 8001)
    httpd = HTTPServer(server_address, RequestHandler)
    yield httpd
    httpd.server_close()

def test_server_starts(http_server):
    assert http_server.server_address[1] == 8001
