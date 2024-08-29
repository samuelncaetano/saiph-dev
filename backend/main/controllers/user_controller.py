from typing import Any, List, Literal

from backend.application.use_cases.user_use_cases import UserUseCases
from backend.domain.entities.user import User


class UserController:
    def __init__(self, user_use_cases: UserUseCases):
        self.user_use_cases = user_use_cases

    def create_user(self, user_data: dict[str, Any]) -> tuple[Literal[201], dict[str, Any]]:
        user = self.user_use_cases.create_user(User(id=0, **user_data))
        return 201, user

    def login_user(self, login_data: dict[str, Any]) -> tuple[Literal[200], dict[str, Any]]:
        email = login_data.get("email")
        password = login_data.get("password")
        if not email or not password:
            raise ValueError("Email and password are required")
        user = self.user_use_cases.login_user(email, password)
        return 200, user

    def list_users(self) -> tuple[Literal[200], List[dict[str, Any]]]:
        user = self.user_use_cases.list_users()
        return 200, user

    def get_by_id(self, user_id: int) -> tuple[Literal[200], dict[str, Any]]:
        user = self.user_use_cases.get_by_id(user_id)
        return 200, user

    def update_user(self, user_id: int, user_data: dict[str, Any]) -> tuple[Literal[200], dict[str, Any]]:
        user = self.user_use_cases.update_user(user_id, user_data)
        return 200, user

    def delete_user(self, user_id: int) -> tuple[Literal[200], List[dict[str, Any]]]:
        user = self.user_use_cases.delete_user(user_id)
        return 200, user
