from src.domain.entities.user import UserModel
from src.infrastructure.repositories.json.json_repository import JSONRepository


class UserRepository(JSONRepository):
    def __init__(self, db_path: str):
        super().__init__(db_path=db_path, model=UserModel)
