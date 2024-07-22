import re
from functools import wraps
from typing import Any

from src.main.controllers.user_controller import UserController

user_routes = []


def route(path: str, method: str):
    def decorator(func):  # type: ignore
        pattern = re.compile(re.sub(r"<(\w+)>", r"(?P<\1>\\d+)", path))
        user_routes.append((pattern, method, func))

        @wraps(func)  # type: ignore
        def wrapper(*args, **kwargs):  # type: ignore
            return func(*args, **kwargs)

        return wrapper

    return decorator


@route("/users", "GET")
def get_users(controller: UserController):
    def handler():
        users = controller.list_users()
        return 200, users

    return handler


@route("/users", "POST")
def post_user(controller: UserController, user_data: dict[str, Any]):
    def handler():
        user = controller.create_user(user_data)
        return 201, user

    return handler


@route("/users/<id>", "PUT")
def put_user(controller: UserController, id: int):  # pylint: disable = C0103, W0622
    def handler(user_data: dict[str, Any]):
        user = controller.update_user(int(id), user_data)
        return 200, user

    return handler


@route("/users/<id>", "DELETE")
def delete_user(controller: UserController, id: int):  # pylint: disable = C0103, W0622
    def handler():
        users = controller.delete_user(int(id))
        return 200, users

    return handler
