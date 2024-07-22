import json
from http.server import BaseHTTPRequestHandler, HTTPServer

from src.main.routes.config import configure_dependencies
from src.main.routes.routes import routes as app_routes

user_controller = configure_dependencies()


class RequestHandler(BaseHTTPRequestHandler):
    routes = app_routes

    def _send_response(self, status_code, content_type, data):  # type: ignore
        self.send_response(status_code)  # type: ignore
        self.send_header("Content-type", content_type)  # type: ignore
        self.end_headers()
        self.wfile.write(data.encode("utf-8"))  # type: ignore

    def do_GET(self):  # pylint: disable = C0103
        self._handle_request("GET")

    def do_POST(self):  # pylint: disable = C0103
        self._handle_request("POST")

    def do_PUT(self):  # pylint: disable = C0103
        self._handle_request("PUT")

    def do_DELETE(self):  # pylint: disable = C0103
        self._handle_request("DELETE")

    def _handle_request(self, method: str):
        path = self.path
        for pattern, route_method, handler in self.routes:
            match = pattern.match(path)
            if match and method == route_method:
                try:
                    if method in ["POST", "PUT"]:
                        content_length = int(self.headers["Content-Length"])
                        post_data = self.rfile.read(content_length).decode("utf-8")
                        user_data = json.loads(post_data)
                        if method == "POST":
                            status_code, response = handler(user_controller, user_data)
                        else:
                            status_code, response = handler(user_controller, **match.groupdict(), user_data=user_data)
                    elif method == "DELETE":
                        status_code, response = handler(user_controller, **match.groupdict())
                    else:
                        status_code, response = handler(user_controller, **match.groupdict())
                    self._send_response(status_code, "application/json", json.dumps(response))  # type: ignore
                except ValueError as error:
                    self._send_response(400, "application/json", json.dumps({"error": str(error)}))
                except Exception as error:
                    self._send_response(500, "application/json", json.dumps({"error": str(error)}))
                return
        self._send_response(404, "text/plain", "Not Found")


def run(server_class=HTTPServer, handler_class=RequestHandler, port=8080):  # type: ignore
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting httpd server on port {port}...")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
