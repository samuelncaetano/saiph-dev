import json
from http.server import BaseHTTPRequestHandler, HTTPServer

from src.main.config.config import configure_user_dependencies
from src.main.routes.index import all_routes, register_routes


class RequestHandler(BaseHTTPRequestHandler):
    routes = all_routes

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

    def get_command(self, handler, match, controller):  # type: ignore
        status_code, response = handler(controller, **match.groupdict())()
        return status_code, response

    def post_command(self, handler, controller):  # type: ignore
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length).decode("utf-8")
        request_data = json.loads(post_data)
        status_code, response = handler(controller, request_data)()
        return status_code, response

    def put_command(self, handler, match, controller):  # type: ignore
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length).decode("utf-8")
        request_data = json.loads(post_data)
        status_code, response = handler(controller, **match.groupdict())(request_data)
        return status_code, response

    def patch_command(self, handler, match, controller):  # type: ignore
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length).decode("utf-8")
        request_data = json.loads(post_data)
        status_code, response = handler(controller, **match.groupdict())(request_data)
        return status_code, response

    def delete_command(self, handler, match, controller):  # type: ignore
        status_code, response = handler(controller, **match.groupdict())()
        return status_code, response

    def _handle_request(self, method: str):
        path = self.path
        for pattern, route_method, handler, controller in self.routes:
            match = pattern.match(path)
            if match and method == route_method:
                try:
                    if method == "POST":
                        status_code, response = self.post_command(handler, controller)  # type: ignore
                    elif method == "PUT":
                        status_code, response = self.put_command(handler, match, controller)  # type: ignore
                    elif method == "PATCH":
                        status_code, response = self.patch_command(handler, match, controller)  # type: ignore
                    elif method == "DELETE":
                        status_code, response = self.delete_command(handler, match, controller)  # type: ignore
                    elif method == "GET":
                        status_code, response = self.get_command(handler, match, controller)  # type: ignore
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
