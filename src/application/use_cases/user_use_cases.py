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
