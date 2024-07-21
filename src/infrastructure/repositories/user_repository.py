from dataclasses import asdict
from typing import Any

from pydantic import ValidationError  # pylint: disable = E0401  # type: ignore

from src.application.services.user_schema import pydantic_to_user, user_to_pydantic
from src.domain.entities.user import User, UserModel
from src.infrastructure.repositories.json_repository import JSONRepository


class UserRepository(JSONRepository):
    def __init__(self, db_path: str):
        super().__init__(db_path=db_path, model=UserModel)

    def add(self, item: User) -> dict[str, Any]:
        try:
            data = self.load_data()
            data.append(item)
            data = list(map(user_to_pydantic, data))
            self.save_data(data)
            return asdict(item)
        except ValidationError as error:
            raise ValueError(f"Invalid user data: {error}")  # pylint: disable = W0707

    def get_all(self):
        data = self.load_data()
        return list(map(pydantic_to_user, data))
