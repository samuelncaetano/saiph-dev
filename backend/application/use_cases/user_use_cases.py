from dataclasses import dataclass
from typing import Any, List

from backend.domain.entities.user import User
from backend.infrastructure.repositories.user_repository import UserRepository


@dataclass(slots=True, kw_only=True)
class UserUseCases:
    repository: UserRepository

    def create_user(self, user: User) -> dict[str, Any]:
        if self.repository.get_by_email(user.email):
            raise ValueError("Email already registered")
        return self.repository.add(user)

    def login_user(self, email: str, password: str) -> dict[str, Any]:
        user = self.repository.validate_user(email, password)
        if not user:
            raise ValueError("Invalid email or password")
        return user

    def list_users(self) -> List[dict[str, Any]]:
        return self.repository.get_all()

    def get_by_id(self, user_id: int) -> dict[str, Any]:
        return self.repository.get_by_id(user_id)

    def update_user(self, user: dict[str, Any]) -> dict[str, Any]:
        return self.repository.update(user)

    def delete_user(self, user_id: int) -> List[dict[str, Any]]:
        return self.repository.delete(user_id)
