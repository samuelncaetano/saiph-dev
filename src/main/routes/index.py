from src.main.controllers.book_controller import BookController
from src.main.controllers.user_controller import UserController
from src.main.routes.book_routes import get_books_routes
from src.main.routes.user_routes import get_routes

all_routes = []


def register_route(pattern, method, handler, controller):  # type: ignore
    all_routes.append((pattern, method, handler, controller))


def register_user_routes(controller: UserController):
    sorted_user_routes = get_routes()
    for route in sorted_user_routes:
        register_route(*route, controller)


def register_book_routes(controller: BookController):
    sorted_book_routes = get_books_routes()
    for route in sorted_book_routes:
        register_route(*route, controller)


def register_routes(user_controller: UserController, book_controller: BookController):
    register_user_routes(user_controller)
    register_book_routes(book_controller)
