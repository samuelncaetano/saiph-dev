from dataclasses import asdict
from typing import Any, List

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

    def get_all(self) -> List[dict[str, Any]]:
        data = self.load_data()
        data = list(map(pydantic_to_user, data))
        data = [asdict(user) for user in data]
        return data

    def get_by_id(self, user_id: int) -> dict[str, Any]:
        data = self.load_data()
        data = list(map(pydantic_to_user, data))
        for item in data:
            if item.id == user_id:
                return asdict(item)
        raise ValueError("User not found")

    def update(self, updated_user_data: dict[str, Any]) -> dict[str, Any]:
        data = self.load_data()
        user_model = UserModel(**updated_user_data)
        for idx, item in enumerate(data):
            if item.id == user_model.id:
                data[idx] = user_model
                self.save_data(data)
                return user_model.model_dump()
        raise ValueError("User not found")

    def delete(self, user_id: int) -> List[dict[str, Any]]:
        data = self.load_data()
        data = list(map(pydantic_to_user, data))
        for idx, item in enumerate(data):
            if item.id == user_id:
                del data[idx]
                self.save_data(data)
                return self.get_all()
        raise ValueError("User not found")
