import threading
import time
from http.server import HTTPServer
from pathlib import Path

import pytest  # type: ignore
import requests  # type: ignore

from src.domain.entities.user import User
from src.main.config.config import configure_user_dependencies
from src.main.routes.index import register_routes
from src.main.server.server import RequestHandler


# Função para iniciar o servidor em uma thread separada
def start_server(port: int, db_path: str):
    server_address = ("", port)
    user_controller = configure_user_dependencies(db_path)
    register_routes(user_controller)
    httpd = HTTPServer(server_address, RequestHandler)
    httpd.serve_forever()


@pytest.fixture(scope="module")
def test_server(tmpdir_factory):  # type: ignore
    temp_dir = tmpdir_factory.mktemp("data")
    db_path = Path(temp_dir) / "users.json"  # type: ignore
    port = 8081

    # Inicializar servidor em thread separada
    server_thread = threading.Thread(target=start_server, args=(port, db_path))
    server_thread.daemon = True
    server_thread.start()

    # Esperar servidor iniciar
    time.sleep(1)

    yield f"http://localhost:{port}"

    # Teardown
    requests.get(f"http://localhost:{port}/shutdown")
    server_thread.join(1)


def test_integration_create_user(test_server):  # type: ignore
    url = f"{test_server}/users"
    user_data = {"name": "John Doe", "email": "johndoe@example.com", "password": "default", "age": 30}

    response = requests.post(url, json=user_data)
    created_user = response.json()

    assert response.status_code == 201
    assert created_user["name"] == "John Doe"
    assert created_user["email"] == "johndoe@example.com"
    assert created_user["password"] == "default"
    assert created_user["age"] == 30


def test_integration_list_users(test_server):  # type: ignore
    url = f"{test_server}/users"
    response = requests.get(url)
    users: list[User] = response.json()

    assert response.status_code == 200
    assert isinstance(users, list)
    assert len(users) > 0


def test_integration_get_user_by_id(test_server):  # type: ignore
    url = f"{test_server}/users"
    user_data = {"name": "Jane Doe", "email": "janedoe@example.com", "password": "default", "age": 25}

    response_post = requests.post(url, json=user_data)
    created_user = response_post.json()
    user_id = created_user["id"]

    response_get = requests.get(f"{url}/{user_id}")
    fetched_user = response_get.json()

    assert response_get.status_code == 200
    assert fetched_user["id"] == user_id
    assert fetched_user["name"] == "Jane Doe"
    assert fetched_user["email"] == "janedoe@example.com"
    assert fetched_user["password"] == "default"
    assert fetched_user["age"] == 25


def test_integration_update_user(test_server):  # type: ignore
    url = f"{test_server}/users"
    user_data = {"name": "Jane Smith", "email": "janesmith@example.com", "password": "default", "age": 28}
    update_data = {"name": "Jane Doe", "email": "janedoe@example.com", "password": "default", "age": 29}

    response_post = requests.post(url, json=user_data)
    created_user = response_post.json()
    user_id = created_user["id"]

    response_patch = requests.patch(f"{url}/{user_id}", json=update_data)
    updated_user = response_patch.json()

    assert response_patch.status_code == 200
    assert updated_user["id"] == user_id
    assert updated_user["name"] == "Jane Doe"
    assert updated_user["email"] == "janedoe@example.com"
    assert updated_user["password"] == "default"
    assert updated_user["age"] == 29


def test_integration_delete_user(test_server):  # type: ignore
    url = f"{test_server}/users"
    user_data = {"name": "Jim Doe", "email": "jimdoe@example.com", "password": "default", "age": 35}

    response_post = requests.post(url, json=user_data)
    created_user = response_post.json()
    user_id = created_user["id"]

    response_delete = requests.delete(f"{url}/{user_id}")
    assert response_delete.status_code == 200

    response_invalided = requests.get(f"{url}/{user_id}")
    assert response_invalided.status_code == 404
