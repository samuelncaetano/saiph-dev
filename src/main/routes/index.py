from src.main.config.config import configure_user_dependencies
from src.main.routes.user_routes import user_routes

routes = []


def register_route(pattern, method, handler, controller):  # type: ignore
    routes.append((pattern, method, handler, controller))


# Configurar dependências
user_controller = configure_user_dependencies()

# Registrar rotas de usuários
for route in user_routes:
    register_route(*route, user_controller)
