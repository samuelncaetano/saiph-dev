import json
import shutil
from dataclasses import dataclass, field
from pathlib import Path
from tempfile import NamedTemporaryFile
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
        temp_file = NamedTemporaryFile("w", delete=False, dir=self._path.parent)  # pylint: disable = R1732
        try:
            data = list(map(user_to_pydantic, data))
            json.dump([item.model_dump() for item in data], temp_file)
            temp_file.flush()
            shutil.move(temp_file.name, self._path)
        finally:
            temp_file.close()

    def add(self, item: Any):
        data = self.load_data()
        data.append(item)
        self.save_data(data)

    def get_all(self):
        data = self.load_data()
        return list(map(pydantic_to_user, data))
