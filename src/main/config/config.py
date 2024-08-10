from src.application.use_cases.book_use_cases import BookUseCases
from src.application.use_cases.user_use_cases import UserUseCases
from src.infrastructure.repositories.book_repository import BookRepository
from src.infrastructure.repositories.user_repository import UserRepository
from src.main.controllers.book_controller import BookController
from src.main.controllers.user_controller import UserController


def configure_user_dependencies(db_path: str) -> UserController:
    user_repository = UserRepository(db_path=db_path)
    user_use_cases = UserUseCases(repository=user_repository)
    user_controller = UserController(user_use_cases=user_use_cases)
    return user_controller


def configure_book_dependencies(db_path: str) -> BookController:
    book_repository = BookRepository(db_path=db_path)
    book_use_cases = BookUseCases(repository=book_repository)
    book_controller = BookController(book_use_case=book_use_cases)
    return book_controller
