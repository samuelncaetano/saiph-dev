import json
import logging
from http.server import BaseHTTPRequestHandler, HTTPServer

from backend.main.config.config import configure_book_dependencies, configure_user_dependencies
from backend.main.routes.index import all_routes, register_routes

# Configuração básica do logging
logging.basicConfig(
    level=logging.INFO,  # Nível de log
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # Formato da mensagem
    datefmt="%Y-%m-%d %H:%M:%S",  # Formato da data
    handlers=[logging.FileHandler("logs.txt"), logging.StreamHandler()],  # Log para um arquivo  # Log para o console
)

# Criar um logger
logger = logging.getLogger("server")


class RequestHandler(BaseHTTPRequestHandler):
    routes = all_routes

    def _send_response(self, status_code: int, content_type: str, data: str):
        logger.debug(f"Sending response: status_code={status_code}, content_type={content_type}")
        self.send_response(status_code)
        self.send_header("Content-type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PATCH, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization, Session-ID")
        self.end_headers()
        self.wfile.write(data.encode("utf-8"))

    def do_OPTIONS(self):  # pylint: disable = C0103
        logger.debug(f"Handling OPTIONS request: path={self.path}")
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PATCH, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization, Session-ID")
        self.end_headers()

    def do_GET(self):  # pylint: disable = C0103
        logger.debug(f"Handling GET request: path={self.path}")
        self._handle_request("GET")

    def do_POST(self):  # pylint: disable = C0103
        logger.debug(f"Handling POST request: path={self.path}")
        self._handle_request("POST")

    def do_PATCH(self):  # pylint: disable = C0103
        logger.debug(f"Handling PATCH request: path={self.path}")
        self._handle_request("PATCH")

    def do_DELETE(self):  # pylint: disable = C0103
        logger.debug(f"Handling DELETE request: path={self.path}")
        self._handle_request("DELETE")

    def get_command(self, handler, match, controller):  # type: ignore
        logger.debug(f"Executing GET command: handler={handler}, match={match.groupdict()}, controller={controller}")
        status_code, response = handler(self, controller, **match.groupdict())()
        return status_code, response

    def post_command(self, handler, controller):  # type: ignore
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length).decode("utf-8")
        request_data = json.loads(post_data)
        logger.debug(f"Executing POST command: handler={handler}, request_data={request_data}, controller={controller}")
        status_code, response = handler(self, controller, request_data)()
        return status_code, response

    def put_command(self, handler, match, controller):  # type: ignore
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length).decode("utf-8")
        request_data = json.loads(post_data)
        logger.debug(
            f"Executing PUT command: handler={handler}, match={match.groupdict()}, request_data={request_data}, controller={controller}"  # pylint: disable = C0301   # noqa: E501
        )
        status_code, response = handler(self, controller, **match.groupdict())(request_data)
        return status_code, response

    def patch_command(self, handler, match, controller):  # type: ignore
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length).decode("utf-8")
        request_data = json.loads(post_data)
        logger.debug(
            f"Executing PATCH command: handler={handler}, match={match.groupdict()}, request_data={request_data}, controller={controller}"  # pylint: disable = C0301   # noqa: E501
        )
        status_code, response = handler(self, controller, **match.groupdict())(request_data)
        return status_code, response

    def delete_command(self, handler, match, controller):  # type: ignore
        logger.debug(f"Executing DELETE command: handler={handler}, match={match.groupdict()}, controller={controller}")
        status_code, response = handler(self, controller, **match.groupdict())()
        return status_code, response

    def _handle_request(self, method: str):
        path = self.path
        logger.debug(f"Handling request: method={method}, path={path}")
        for pattern, route_method, handler, controller in self.routes:
            match = pattern.match(path)
            if match and method == route_method:
                try:
                    if method == "POST":
                        status_code, response = self.post_command(handler, controller)  # type: ignore
                        logger.info(f"Request handled: method={method}, path={path}, status_code={status_code}")
                    elif method == "PUT":
                        status_code, response = self.put_command(handler, match, controller)  # type: ignore
                        logger.info(f"Request handled: method={method}, path={path}, status_code={status_code}")
                    elif method == "PATCH":
                        status_code, response = self.patch_command(handler, match, controller)  # type: ignore
                        logger.info(f"Request handled: method={method}, path={path}, status_code={status_code}")
                    elif method == "DELETE":
                        status_code, response = self.delete_command(handler, match, controller)  # type: ignore
                        logger.info(f"Request handled: method={method}, path={path}, status_code={status_code}")
                    elif method == "GET":
                        status_code, response = self.get_command(handler, match, controller)  # type: ignore
                        logger.info(f"Request handled: method={method}, path={path}, status_code={status_code}")
                    self._send_response(status_code, "application/json", json.dumps(response))  # type: ignore
                except ValueError as error:
                    logger.error(f"ValueError: {error}")
                    self._send_response(400, "application/json", json.dumps({"error": str(error)}))
                except Exception as error:
                    logger.error(f"Unhandled exception: {error}")
                    self._send_response(500, "application/json", json.dumps({"error": str(error)}))
                return
        logger.warning(f"Route not found: path={path}, method={method}")
        self._send_response(404, "text/plain", "Not Found")


def run(
    server_class: type[HTTPServer] = HTTPServer,
    handler_class: type[RequestHandler] = RequestHandler,
    port: int = 8080,
    db_path_user: str = "database/users.json",
    db_path_book: str = "database/books.json",
):
    logger.debug("Configuring user dependencies")
    user_controller = configure_user_dependencies(db_path_user)
    book_controller = configure_book_dependencies(db_path_book)
    register_routes(user_controller, book_controller)
    logger.debug("Registering routes")
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting HTTP server on port {port}...")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
