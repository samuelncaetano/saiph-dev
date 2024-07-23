import json
from http.server import BaseHTTPRequestHandler, HTTPServer

from src.main.config.config import configure_user_dependencies
from src.main.routes.index import register_routes, routes


class RequestHandler(BaseHTTPRequestHandler):
    routes = routes

    def _send_response(self, status_code: int, content_type: str, data: str):
        self.send_response(status_code)
        self.send_header("Content-type", content_type)
        self.end_headers()
        self.wfile.write(data.encode("utf-8"))

    def do_GET(self):  # pylint: disable = C0103
        self._handle_request("GET")

    def do_POST(self):  # pylint: disable = C0103
        self._handle_request("POST")

    def do_PATCH(self):  # pylint: disable = C0103
        self._handle_request("PATCH")

    def do_DELETE(self):  # pylint: disable = C0103
        self._handle_request("DELETE")

    def _handle_request(self, method: str):
        path = self.path
        for pattern, route_method, handler, controller in self.routes:
            match = pattern.match(path)
            if match and method == route_method:
                try:
                    if method in ["POST", "PATCH"]:
                        content_length = int(self.headers["Content-Length"])
                        post_data = self.rfile.read(content_length).decode("utf-8")
                        request_data = json.loads(post_data)
                        if method == "POST":
                            status_code, response = handler(controller, request_data)()
                        else:
                            status_code, response = handler(controller, **match.groupdict())(request_data)
                    elif method == "DELETE":
                        status_code, response = handler(controller, **match.groupdict())()
                    else:
                        status_code, response = handler(controller, **match.groupdict())()
                    self._send_response(status_code, "application/json", json.dumps(response))  # type: ignore
                except ValueError as error:
                    self._send_response(404, "application/json", json.dumps({"error": str(error)}))
                except Exception as error:
                    self._send_response(500, "application/json", json.dumps({"error": str(error)}))
                return
        self._send_response(404, "text/plain", "Not Found")


def run(
    server_class: type[HTTPServer] = HTTPServer,
    handler_class: type[RequestHandler] = RequestHandler,
    port: int = 8080,
    db_path_user: str = "database/users.json",
):
    user_controller = configure_user_dependencies(db_path_user)
    register_routes(user_controller)
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting HTTP server on port {port}...")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
