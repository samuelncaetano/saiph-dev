import json
from dataclasses import asdict
from http.server import BaseHTTPRequestHandler, HTTPServer

from src.main.routes.config import configure_dependencies

user_controller = configure_dependencies()


class RequestHandler(BaseHTTPRequestHandler):
    def _send_response(self, status_code, content_type, data):  # type: ignore
        self.send_response(status_code)  # type: ignore
        self.send_header("Content-type", content_type)  # type: ignore
        self.end_headers()
        self.wfile.write(data.encode("utf-8"))  # type: ignore

    def do_GET(self):  # pylint: disable = C0103
        if self.path == "/users":
            try:
                users = user_controller.list_users()
                users_json = json.dumps([asdict(user) for user in users])
                self._send_response(200, "application/json", users_json)
            except Exception as error:
                self._send_response(500, "application/json", json.dumps({"error": str(error)}))
        else:
            self._send_response(404, "text/plain", "Not Found")

    def do_POST(self):  # pylint: disable = C0103
        if self.path == "/users":
            try:
                content_length = int(self.headers["Content-Length"])
                post_data = self.rfile.read(content_length).decode("utf-8")
                user_data = json.loads(post_data)
                user = user_controller.create_user(user_data)
                self._send_response(201, "application/json", json.dumps(asdict(user)))
            except ValueError as error:
                self._send_response(400, "application/json", json.dumps({"error": str(error)}))
            except Exception as error:
                self._send_response(500, "application/json", json.dumps({"error": str(error)}))
        else:
            self._send_response(404, "text/plain", "Not Found")


def run(server_class=HTTPServer, handler_class=RequestHandler, port=8080):  # type: ignore
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting httpd server on port {port}...")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
