import re
from functools import wraps
from typing import Any

from src.main.controllers.user_controller import UserController

routes = []


def route(path: str, method: str):
    def decorator(func):  # type: ignore
        pattern = re.compile(re.sub(r"<(\w+)>", r"(?P<\1>\\d+)", path))
        routes.append((pattern, method, func))

        @wraps(func)  # type: ignore
        def wrapper(*args, **kwargs):  # type: ignore
            return func(*args, **kwargs)

        return wrapper

    return decorator


@route("/users", "GET")
def get_users(controller: UserController):
    users = controller.list_users()
    return 200, users


@route("/users", "POST")
def post_user(controller: UserController, user_data: dict[str, Any]):
    user = controller.create_user(user_data)
    return 201, user


@route("/users/<id>", "PUT")
def put_user(controller: UserController, id: int, user_data: dict[str, Any]):  # pylint: disable = W0622, C0103
    user = controller.update_user(int(id), user_data)
    return 200, user


@route("/users/<id>", "DELETE")
def delete_user(controller: UserController, id: int):  # pylint: disable = W0622, C0103
    users = controller.delete_user(int(id))
    return 200, users
