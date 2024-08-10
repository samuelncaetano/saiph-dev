import logging
from dataclasses import asdict
from typing import Any, List

from pydantic import ValidationError  # pylint: disable = E0401  # type: ignore

from src.application.services.book_schema import book_to_pydantic, pydantic_to_book
from src.domain.entities.book import Book, BookModel
from src.infrastructure.repositories.json_repository import JSONRepository

# Criar um logger
logger = logging.getLogger("book_repository")


class BookRepository(JSONRepository):
    def __init__(self, db_path: str):
        logger.debug(f"Initializing BookRepository with db_path: {db_path}")
        super().__init__(db_path=db_path, model=BookModel)

    def _get_next_id(self):
        data = self.load_data()
        if not data:
            return 1
        max_id = max(user.id for user in data)
        next_id = max_id + 1
        logger.debug(f"Next ID calculated: {next_id}")
        return next_id

    def add(self, item: Book) -> dict[str, Any]:
        try:
            logger.debug(f"Adding book: {item}")
            if item.id == 0:
                item.id = self._get_next_id()
            data = self.load_data()
            data.append(item)
            data = list(map(book_to_pydantic, data))
            self.save_data(data)
            logger.info(f"book added: {asdict(item)}")
            return asdict(item)
        except ValidationError as error:
            logger.error(f"Validation error: {error}")
            raise ValueError(f"Invalid book data: {error}")  # pylint: disable = W0707

    def get_all(self) -> List[dict[str, Any]]:
        data = self.load_data()
        data = list(map(pydantic_to_book, data))
        data = [asdict(book) for book in data]
        return data

    def get_by_id(self, book_id: int) -> dict[str, Any]:
        logger.debug(f"Fetching book by ID: {book_id}")
        data = self.load_data()
        data = list(map(pydantic_to_book, data))
        for item in data:
            if item.id == book_id:
                logger.info(f"Book found: {asdict(item)}")
                return asdict(item)
        logger.warning(f"Book not found: {book_id}")
        raise ValueError("Book not found")

    def get_by_user_id(self, user_id: int) -> list[dict[str, Any]]:
        logger.debug(f"Fetching books by user ID: {user_id}")
        data = self.load_data()
        data = list(map(pydantic_to_book, data))
        books = []
        for item in data:
            if item.user_id == user_id:
                logger.info(f"Book found: {asdict(item)}")
                books.append(asdict(item))
        if books:  # pylint: disable = R1705
            return books
        else:
            logger.warning(f"No books found for user ID: {user_id}")
            raise ValueError("No books found for the given user ID")

    def update(self, updated_book_data: dict[str, Any]) -> dict[str, Any]:
        logger.debug(f"Updating book: {updated_book_data}")
        data = self.load_data()
        book_model = BookModel(**updated_book_data)
        for idx, item in enumerate(data):
            if item.id == book_model.id:
                data[idx] = book_model
                self.save_data(data)
                logger.info(f"book updated: {book_model.model_dump()}")
                return book_model.model_dump()
        logger.warning(f"Book not found for update: {book_model.id}")
        raise ValueError("Book not found")

    def delete(self, book_id: int) -> List[dict[str, Any]]:
        logger.debug(f"Deleting book by ID: {book_id}")
        data = self.load_data()
        for idx, item in enumerate(data):
            if item.id == book_id:
                del data[idx]
                self.save_data(data)
                return self.get_all()
        logger.warning(f"Book not found for deletion: {book_id}")
        raise ValueError("Book not found")
