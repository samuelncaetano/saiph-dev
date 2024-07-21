from pydantic import ValidationError  # pylint: disable = E0401  # type: ignore

from src.application.services.user_schema import user_to_pydantic
from src.domain.entities.user import User, UserModel
from src.infrastructure.repositories.json.json_repository import JSONRepository


class UserRepository(JSONRepository):
    def __init__(self, db_path: str):
        super().__init__(db_path=db_path, model=UserModel)

    def add(self, item: User):
        try:
            user_to_pydantic(item)
            super().add(item)
        except ValidationError as error:
            raise ValueError(f"Invalid user data: {error}")  # pylint: disable = W0707
