from dataclasses import dataclass
from typing import Any, List

from src.domain.entities.user import User
from src.infrastructure.repositories.user_repository import UserRepository


@dataclass(slots=True, kw_only=True)
class UserUseCases:
    repository: UserRepository

    def create_user(self, user: User) -> dict[str, Any]:
        return self.repository.add(user)

    def list_users(self) -> List[dict[str, Any]]:
        return self.repository.get_all()

    def get_by_id(self, user_id: int) -> dict[str, Any]:
        return self.repository.get_by_id(user_id)

    def update_user(self, user: dict[str, Any]) -> dict[str, Any]:
        return self.repository.update(user)

    def delete_user(self, user_id: int) -> List[dict[str, Any]]:
        return self.repository.delete(user_id)
