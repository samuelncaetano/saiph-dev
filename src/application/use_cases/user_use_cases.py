from typing import List

from src.domain.entities.user import User
from src.infrastructure.database.json.user_repository import UserRepository


class UserUseCases:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def create_user(self, user: User):
        self.repository.add(user)

    def list_users(self) -> List[User]:
        return self.repository.get_all()
