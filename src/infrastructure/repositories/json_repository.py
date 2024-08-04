import json
import logging
import shutil
from dataclasses import dataclass, field
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any

# Criar um logger
logger = logging.getLogger(__name__)


@dataclass
class JSONRepository:
    db_path: str
    model: type
    _path: Path = field(init=False)

    def __post_init__(self):
        self._path = Path(self.db_path)
        logging.debug(f"Initializing JSONRepository with path: {self._path}")
        self._path.parent.mkdir(parents=True, exist_ok=True)
        if not self._path.exists():
            self._initialize_db()

    def _initialize_db(self):
        logging.debug(f"Creating new database file at: {self._path}")
        with open(self._path, "w") as f:  # pylint: disable = W1514, C0103
            json.dump([], f)
        logging.info(f"Database initialized at: {self._path}")

    def load_data(self):
        logging.debug(f"Loading data from: {self._path}")
        with open(self._path, "r") as f:  # pylint: disable = W1514, C0103
            data = json.load(f)
            # logging.info(f'Data loaded: {data}')
            return [self.model(**item) for item in data]

    def save_data(self, data: Any):
        logging.debug(f"Saving data to: {self._path}")
        temp_file = NamedTemporaryFile("w", delete=False, dir=self._path.parent)  # pylint: disable = R1732
        try:
            json.dump([item.model_dump() for item in data], temp_file)
            temp_file.flush()
            shutil.move(temp_file.name, self._path)
            logging.info(f"Data successfully saved to: {self._path}")
        finally:
            temp_file.close()
            logging.debug(f"Temporary file closed: {temp_file.name}")
