import re
from typing import Any

from src.main.controllers.book_controller import BookController

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


@route("/books", "POST")
def post_book(
    request, controller: BookController, book_data: dict[str, Any]  # pylint: disable = W0613  # type: ignore
):
    def handler():
        book = controller.create_book(book_data)
        return 201, book

    return handler


def get_books_routes():
    return sorted(routes, key=lambda route: len(route[0].pattern), reverse=True)  # type: ignore
