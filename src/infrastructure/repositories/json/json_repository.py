import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from src.application.services.user_schema import pydantic_to_user, user_to_pydantic


@dataclass
class JSONRepository:
    db_path: str
    model: type
    _path: Path = field(init=False)

    def __post_init__(self):
        self._path = Path(self.db_path)
        self._path.parent.mkdir(parents=True, exist_ok=True)
        if not self._path.exists():
            self._initialize_db()

    def _initialize_db(self):
        with open(self._path, "w") as f:  # pylint: disable = W1514, C0103
            json.dump([], f)

    def load_data(self):
        with open(self._path, "r") as f:  # pylint: disable = W1514, C0103
            data = json.load(f)
            return [self.model(**item) for item in data]

    def save_data(self, data: Any):
        with open(self._path, "w") as f:  # pylint: disable = W1514, C0103
            data = map(user_to_pydantic, data)
            json.dump([item.model_dump() for item in data], f)

    def add(self, item: Any):
        data = self.load_data()
        data.append(item)
        self.save_data(data)

    def get_all(self):
        data = self.load_data()
        return list(map(pydantic_to_user, data))
