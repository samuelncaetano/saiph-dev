from src.application.use_cases.user_use_cases import UserUseCases
from src.infrastructure.repositories.user_repository import UserRepository
from src.main.controllers.user_controller import UserController


def configure_dependencies():
    user_repository = UserRepository(db_path="database/users.json")
    user_use_cases = UserUseCases(repository=user_repository)
    user_controller = UserController(user_use_cases=user_use_cases)
    return user_controller
