from src.main.controllers.user_controller import UserController
from src.main.routes.user_routes import user_routes

routes = []


def register_route(pattern, method, handler, controller):  # type: ignore
    routes.append((pattern, method, handler, controller))


def register_user_routes(controller: UserController):
    for route in user_routes:
        register_route(*route, controller)


def register_routes(user_controller: UserController):
    register_user_routes(user_controller)
