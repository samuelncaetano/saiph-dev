import json
from http.server import HTTPServer
from pathlib import Path
from threading import Thread

import pytest  # type: ignore
import requests  # type: ignore

from src.main.routes.server import RequestHandler

# Configurações do servidor
PORT = 8081
DB_PATH = "database/users.json"


@pytest.fixture(scope="module")
def http_server():
    server_address = ("", PORT)
    httpd = HTTPServer(server_address, RequestHandler)
    thread = Thread(target=httpd.serve_forever)
    thread.daemon = True
    thread.start()
    yield httpd
    httpd.shutdown()
    thread.join()


@pytest.fixture(scope="function", autouse=True)
def clear_json_db():
    path = Path(DB_PATH)
    if path.exists():
        path.unlink()
    with open(DB_PATH, "w") as f:
        json.dump([], f)


def test_list_users_empty(http_server):  # type: ignore
    response = requests.get(f"http://localhost:{PORT}/users")
    assert response.status_code == 200
    assert response.json() == []


def test_create_user(http_server):  # type: ignore
    user_data = {"id": 1, "name": "John Doe", "email": "john.doe@example.com", "age": 30}
    response = requests.post(f"http://localhost:{PORT}/users", json=user_data)
    assert response.status_code == 201
    assert response.json()["name"] == "John Doe"


def test_create_user_invalid_data(http_server):  # type: ignore
    invalid_user_data = {"id": 2, "name": "JD", "email": "invalid_email", "age": 25}
    response = requests.post(f"http://localhost:{PORT}/users", json=invalid_user_data)
    assert response.status_code == 400
    assert "error" in response.json()


def test_update_user(http_server):  # type: ignore
    user_data = {"id": 1, "name": "John Doe", "email": "john.doe@example.com", "age": 30}
    user_data_update = {"id": 1, "name": "Mary Doe", "email": "mary.doe@example.com", "age": 30}
    response = requests.post(f"http://localhost:{PORT}/users", json=user_data)
    response = requests.put(f"http://localhost:{PORT}/users/1", json=user_data_update)
    assert response.status_code == 200
    assert response.json()["name"] == "Mary Doe"


def test_delete_user(http_server):  # type: ignore
    user_data = {"id": 1, "name": "John Doe", "email": "john.doe@example.com", "age": 30}
    response = requests.post(f"http://localhost:{PORT}/users", json=user_data)
    response = requests.delete(f"http://localhost:{PORT}/users/1")
    remaining_users = response.json()

    assert response.status_code == 200
    assert remaining_users == []


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
