from typing import Any, List

from src.application.use_cases.user_use_cases import UserUseCases
from src.domain.entities.user import User


class UserController:
    def __init__(self, user_use_cases: UserUseCases):
        self.user_use_cases = user_use_cases

    def create_user(self, user_data: User) -> dict[str, Any]:
        user = User(**user_data)
        return self.user_use_cases.create_user(user)

    def list_users(self) -> List[dict[str, Any]]:
        return self.user_use_cases.list_users()
