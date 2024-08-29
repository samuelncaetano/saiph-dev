from typing import Any, List

from backend.application.use_cases.user_use_cases import UserUseCases
from backend.domain.entities.user import User


class UserController:
    def __init__(self, user_use_cases: UserUseCases):
        self.user_use_cases = user_use_cases

    def create_user(self, user_data: dict[str, Any]) -> dict[str, Any]:
        user = User(id=0, **user_data)
        return self.user_use_cases.create_user(user)

    def login_user(self, login_data: dict[str, Any]) -> dict[str, Any]:
        email = login_data.get("email")
        password = login_data.get("password")
        if not email or not password:
            raise ValueError("Email and password are required")
        return self.user_use_cases.login_user(email, password)

    def list_users(self) -> List[dict[str, Any]]:
        return self.user_use_cases.list_users()

    def get_by_id(self, user_id: int) -> dict[str, Any]:
        return self.user_use_cases.get_by_id(user_id)

    def update_user(self, user_id: int, user_data: dict[str, Any]) -> dict[str, Any]:
        return self.user_use_cases.update_user(user_id, user_data)

    def delete_user(self, user_id: int) -> List[dict[str, Any]]:
        return self.user_use_cases.delete_user(user_id)
