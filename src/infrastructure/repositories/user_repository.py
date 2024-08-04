import logging
from dataclasses import asdict
from typing import Any, List

from pydantic import ValidationError  # pylint: disable = E0401  # type: ignore

from src.application.services.user_schema import pydantic_to_user, user_to_pydantic
from src.domain.entities.user import User, UserModel
from src.infrastructure.repositories.json_repository import JSONRepository

# Criar um logger
logger = logging.getLogger("user_repository")


class UserRepository(JSONRepository):
    def __init__(self, db_path: str):
        logger.debug(f"Initializing UserRepository with db_path: {db_path}")
        super().__init__(db_path=db_path, model=UserModel)

    def _get_next_id(self):
        data = self.load_data()
        if not data:
            return 1
        max_id = max(user.id for user in data)
        next_id = max_id + 1
        logger.debug(f"Next ID calculated: {next_id}")
        return next_id

    def add(self, item: User) -> dict[str, Any]:
        try:
            logger.debug(f"Adding user: {item}")
            if item.id == 0:
                item.id = self._get_next_id()
            data = self.load_data()
            data.append(item)
            data = list(map(user_to_pydantic, data))
            self.save_data(data)
            logger.info(f"User added: {asdict(item)}")
            return asdict(item)
        except ValidationError as error:
            logger.error(f"Validation error: {error}")
            raise ValueError(f"Invalid user data: {error}")  # pylint: disable = W0707

    def get_all(self) -> List[dict[str, Any]]:
        data = self.load_data()
        data = list(map(pydantic_to_user, data))
        data = [asdict(user) for user in data]
        return data

    def get_by_id(self, user_id: int) -> dict[str, Any]:
        logger.debug(f"Fetching user by ID: {user_id}")
        data = self.load_data()
        data = list(map(pydantic_to_user, data))
        for item in data:
            if item.id == user_id:
                logger.info(f"User found: {asdict(item)}")
                return asdict(item)
        logger.warning(f"User not found: {user_id}")
        raise ValueError("User not found")

    def update(self, updated_user_data: dict[str, Any]) -> dict[str, Any]:
        logger.debug(f"Updating user: {updated_user_data}")
        data = self.load_data()
        user_model = UserModel(**updated_user_data)
        for idx, item in enumerate(data):
            if item.id == user_model.id:
                data[idx] = user_model
                self.save_data(data)
                logger.info(f"User updated: {user_model.model_dump()}")
                return user_model.model_dump()
        logger.warning(f"User not found for update: {user_model.id}")
        raise ValueError("User not found")

    def delete(self, user_id: int) -> List[dict[str, Any]]:
        logger.debug(f"Deleting user by ID: {user_id}")
        data = self.load_data()
        for idx, item in enumerate(data):
            if item.id == user_id:
                del data[idx]
                self.save_data(data)
                return self.get_all()
        logger.warning(f"User not found for deletion: {user_id}")
        raise ValueError("User not found")
