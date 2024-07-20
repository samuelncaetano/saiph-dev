import json
from dataclasses import asdict
from http.server import BaseHTTPRequestHandler, HTTPServer

from src.application.use_cases.user_use_cases import UserUseCases
from src.infrastructure.database.json.user_repository import UserRepository
from src.main.controllers.user_controller import UserController

user_repository = UserRepository(db_path="database/users.json")
user_use_cases = UserUseCases(repository=user_repository)
user_controller = UserController(user_use_cases=user_use_cases)


class RequestHandler(BaseHTTPRequestHandler):
    def _send_response(self, status_code, content_type, data):  # type: ignore
        self.send_response(status_code)  # type: ignore
        self.send_header("Content-type", content_type)  # type: ignore
        self.end_headers()
        self.wfile.write(data.encode("utf-8"))  # type: ignore

    def do_GET(self):  # pylint: disable = C0103
        if self.path == "/users":
            users = user_controller.list_users()
            users_json = json.dumps([asdict(user) for user in users])
            self._send_response(200, "application/json", users_json)
        else:
            self._send_response(404, "text/plain", "Not Found")

    def do_POST(self):  # pylint: disable = C0103
        if self.path == "/users":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length).decode("utf-8")
            user_data = json.loads(post_data)
            user = user_controller.create_user(user_data)
            self._send_response(201, "application/json", json.dumps(asdict(user)))
        else:
            self._send_response(404, "text/plain", "Not Found")


def run(server_class=HTTPServer, handler_class=RequestHandler, port=8080):  # type: ignore
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting httpd server on port {port}...")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
