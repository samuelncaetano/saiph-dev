import re
from typing import Any

from src.main.controllers.user_controller import UserController

routes = []


def route(path: str, method: str):
    def decorator(func):  # type: ignore
        pattern = re.compile(re.sub(r"<(\w+)>", r"(?P<\1>\\d+)", path))
        routes.append((pattern, method, func))
        return func

    return decorator


@route("/users", "GET")
def get_users(controller: UserController):
    def handler():
        users = controller.list_users()
        return 200, users

    return handler


@route("/users/<id>", "GET")
def get_users_by_id(controller: UserController, id: int):  # pylint: disable = C0103, W0622
    def handler():
        user = controller.get_by_id(int(id))
        return 200, user

    return handler


@route("/users", "POST")
def post_user(controller: UserController, user_data: dict[str, Any]):
    def handler():
        user = controller.create_user(user_data)
        return 201, user

    return handler


@route("/users/<id>", "PATCH")
def patch_user(controller: UserController, id: int):  # pylint: disable = C0103, W0622
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


def get_routes():
    return sorted(routes, key=lambda route: len(route[0].pattern), reverse=True)  # type: ignore
