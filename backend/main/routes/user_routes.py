import re
from typing import Any

from backend.main.controllers.user_controller import UserController
from backend.main.middlewares.session_middleware import session_middleware

routes = []


def apply_middlewares(handler, middlewares):  # type: ignore
    for middleware in middlewares:
        handler = middleware(handler)
    return handler


def route(path: str, method: str, middlewares=None):  # type: ignore
    if middlewares is None:
        middlewares = []

    def decorator(func):  # type: ignore
        pattern = re.compile(re.sub(r"<(\w+)>", r"(?P<\1>\\d+)", path))
        wrapped_func = apply_middlewares(func, middlewares)  # type: ignore
        routes.append((pattern, method, wrapped_func))
        return wrapped_func

    return decorator


@route("/users", "GET")
def get_users(request, controller: UserController):  # pylint: disable = W0613   # type: ignore
    def handler():
        users = controller.list_users()
        return 200, users

    return handler


@route("/users/<id>", "GET")
def get_users_by_id(
    request, controller: UserController, id: int  # pylint: disable = C0103, W0622, W0613   # type: ignore
):
    def handler():
        user = controller.get_by_id(int(id))
        return 200, user

    return handler


@route("/users", "POST", middlewares=[session_middleware])
def post_user(
    request, controller: UserController, user_data: dict[str, Any]  # pylint: disable = W0613  # type: ignore
):
    def handler():
        user = controller.create_user(user_data)
        return 201, user

    return handler


@route("/users/login", "POST", middlewares=[session_middleware])
def login_user(
    request, controller: UserController, login_data: dict[str, Any]  # pylint: disable = W0613   # type: ignore
):
    def handler():
        user = controller.login_user(login_data)
        return 200, user

    return handler


@route("/users/<id>", "PATCH")
def patch_user(request, controller: UserController, id: int):  # pylint: disable = C0103, W0622, W0613   # type: ignore
    def handler(user_data: dict[str, Any]):
        user = controller.update_user(int(id), user_data)
        return 200, user

    return handler


@route("/users/<id>", "DELETE")
def delete_user(request, controller: UserController, id: int):  # pylint: disable = C0103, W0622, W0613   # type: ignore
    def handler():
        users = controller.delete_user(int(id))
        return 200, users

    return handler


def get_routes():
    return sorted(routes, key=lambda route: len(route[0].pattern), reverse=True)  # type: ignore
