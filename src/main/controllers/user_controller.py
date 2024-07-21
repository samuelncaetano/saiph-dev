from pydantic import ValidationError  # pylint: disable = E0401  # type: ignore

from src.application.use_cases.user_use_cases import UserUseCases
from src.domain.entities.user import User


class UserController:
    def __init__(self, user_use_cases: UserUseCases):
        self.user_use_cases = user_use_cases

    def create_user(self, user_data: User) -> User:
        try:
            user = User(**user_data)
            self.user_use_cases.create_user(user)
            return user
        except ValidationError as error:
            raise ValueError(f"Invalid user data: {error}")  # pylint: disable = W0707

    def list_users(self) -> list[User]:
        return self.user_use_cases.list_users()
