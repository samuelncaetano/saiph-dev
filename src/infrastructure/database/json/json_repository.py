import json
from pathlib import Path
from typing import Any

from src.application.services.user_schema import pydantic_to_user, user_to_pydantic


class JSONRepository:
    def __init__(self, db_path: str, model: type):
        self.db_path = Path(db_path)
        self.model = model

        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.db_path.exists():
            self._initialize_db()

    def _initialize_db(self):
        with open(self.db_path, "w") as f:  # pylint: disable = W1514, C0103
            json.dump([], f)

    def load_data(self):
        with open(self.db_path, "r") as f:  # pylint: disable = W1514, C0103
            data = json.load(f)
            return [self.model(**item) for item in data]

    def save_data(self, data: Any):
        with open(self.db_path, "w") as f:  # pylint: disable = W1514, C0103
            data = map(user_to_pydantic, data)
            json.dump([item.model_dump() for item in data], f)

    def add(self, item: Any):
        data = self.load_data()
        item = user_to_pydantic(item)
        data.append(item)
        self.save_data(data)

    def get_all(self):
        data = self.load_data()
        return list(map(pydantic_to_user, data))
