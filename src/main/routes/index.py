from src.main.controllers.user_controller import UserController
from src.main.routes.user_routes import get_routes

all_routes = []


def register_route(pattern, method, handler, controller):  # type: ignore
    all_routes.append((pattern, method, handler, controller))


def register_user_routes(controller: UserController):
    sorted_user_routes = get_routes()
    for route in sorted_user_routes:
        register_route(*route, controller)


def register_routes(user_controller: UserController):
    register_user_routes(user_controller)
