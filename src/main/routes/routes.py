from functools import wraps
from typing import Any

from src.main.controllers.user_controller import UserController

routes = []


def route(path: str, method: str):
    def decorator(func):  # type: ignore
        routes.append((path, method, func))

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
