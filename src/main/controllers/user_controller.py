from typing import Any, List

from src.application.services.user_schema import pydantic_to_user, user_to_pydantic
from src.application.use_cases.user_use_cases import UserUseCases
from src.domain.entities.user import User, UserModel


class UserController:
    def __init__(self, user_use_cases: UserUseCases):
        self.user_use_cases = user_use_cases

    def create_user(self, user_data: dict[str, Any]) -> dict[str, Any]:
        user = User(**user_data)
        return self.user_use_cases.create_user(user)

    def list_users(self) -> List[dict[str, Any]]:
        return self.user_use_cases.list_users()

    def get_by_id(self, user_id: int) -> dict[str, Any]:
        return self.user_use_cases.get_by_id(user_id)

    def update_user(self, user_id: int, user_data: dict[str, Any]) -> dict[str, Any]:
        user_dict = self.get_by_id(user_id)
        user = pydantic_to_user(UserModel(**user_dict))
        for key, value in user_data.items():
            setattr(user, key, value)

        user_dict_pydantic = user_to_pydantic(user).model_dump()
        updated_user = self.user_use_cases.update_user(user_dict_pydantic)  # type: ignore
        return updated_user

    def delete_user(self, user_id: int) -> List[dict[str, Any]]:
        return self.user_use_cases.delete_user(user_id)
