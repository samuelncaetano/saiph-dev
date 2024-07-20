from src.application.use_cases.user_use_cases import UserUseCases
from src.domain.entities.user import User


class UserController:
    def __init__(self, user_use_cases: UserUseCases):
        self.user_use_cases = user_use_cases

    def create_user(self, user_data: User) -> User:
        user = User(**user_data)
        self.user_use_cases.create_user(user)
        return user

    def list_users(self) -> list[User]:
        return self.user_use_cases.list_users()
