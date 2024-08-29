import re
from typing import Any

from backend.main.controllers.book_controller import BookController

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


@route("/books", "GET")
def get_all_books(request, controller: BookController):  # pylint: disable = W0613   # type: ignore
    def handler():
        status, books = controller.list_books()
        return status, books

    return handler


@route("/books/<id>", "GET")
def get_books_by_id(
    request, controller: BookController, id: int  # pylint: disable = C0103, W0622, W0613   # type: ignore
):
    def handler():
        status, books = controller.get_by_id(int(id))
        return status, books

    return handler


@route("/books/user/<id>", "GET")
def get_books_by_user_id(
    request, controller: BookController, id: int  # pylint: disable = C0103, W0622, W0613   # type: ignore
):
    def handler():
        status, books = controller.get_by_user_id(int(id))
        return status, books

    return handler


@route("/books", "POST")
def post_book(
    request, controller: BookController, book_data: dict[str, Any]  # pylint: disable = W0613  # type: ignore
):
    def handler():
        status, book = controller.create_book(book_data)
        return status, book

    return handler


@route("/books/<id>", "PATCH")
def patch_book(request, controller: BookController, id: int):  # pylint: disable = C0103, W0622, W0613   # type: ignore
    def handler(book_data: dict[str, Any]):
        status, books = controller.update_book(int(id), book_data)
        return status, books

    return handler


@route("/books/toggle-status/<id>", "PATCH")
def toggle_book_status(
    request, controller: BookController, id: int  # pylint: disable = C0103, W0622, W0613   # type: ignore
):
    def handler(*args, **kwargs):  # pylint: disable = W0613   # type: ignore
        status, books = controller.toggle_book_status(int(id))
        return status, books

    return handler


@route("/books/<id>", "DELETE")
def delete_book(request, controller: BookController, id: int):  # pylint: disable = C0103, W0622, W0613   # type: ignore
    def handler():
        status, books = controller.delete_book(int(id))
        return status, books

    return handler


def get_books_routes():
    return sorted(routes, key=lambda route: len(route[0].pattern), reverse=True)  # type: ignore
