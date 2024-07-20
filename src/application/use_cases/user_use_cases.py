from dataclasses import dataclass
from typing import List

from src.domain.entities.user import User
from src.infrastructure.database.json.user_repository import UserRepository


@dataclass(slots=True, kw_only=True)
class UserUseCases:
    repository: UserRepository

    def create_user(self, user: User):
        self.repository.add(user)

    def list_users(self) -> List[User]:
        return self.repository.get_all()
