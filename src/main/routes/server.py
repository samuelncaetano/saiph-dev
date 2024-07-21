import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any

from src.main.routes.config import configure_dependencies
from src.main.routes.routes import routes

user_controller = configure_dependencies()


class RequestHandler(BaseHTTPRequestHandler):
    routes = routes

    def _send_response(self, status_code: int, content_type: Any, data: Any):
        self.send_response(status_code)
        self.send_header("Content-type", content_type)
        self.end_headers()
        self.wfile.write(data.encode("utf-8"))

    def do_GET(self):  # pylint: disable = C0103
        self._handle_request("GET")

    def do_POST(self):  # pylint: disable = C0103
        self._handle_request("POST")

    def _handle_request(self, method: str):
        for path, route_method, handler in self.routes:
            if self.path == path and method == route_method:
                try:
                    if method == "POST":
                        content_length = int(self.headers["Content-Length"])
                        post_data = self.rfile.read(content_length).decode("utf-8")
                        user_data = json.loads(post_data)
                        status_code, response = handler(user_controller, user_data)
                    else:
                        status_code, response = handler(user_controller)
                    self._send_response(status_code, "application/json", json.dumps(response))  # type: ignore
                except ValueError as error:
                    self._send_response(400, "application/json", json.dumps({"error": str(error)}))
                except Exception as error:
                    self._send_response(500, "application/json", json.dumps({"error": str(error)}))
                return
        self._send_response(404, "text/plain", "Not Found")


def run(
    server_class: type[HTTPServer] = HTTPServer, handler_class: type[RequestHandler] = RequestHandler, port: int = 8080
):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting httpd server on port {port}...")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
