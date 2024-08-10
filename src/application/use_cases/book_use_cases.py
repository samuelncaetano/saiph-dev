from dataclasses import dataclass
from typing import Any, List

from src.domain.entities.book import Book
from src.infrastructure.repositories.book_repository import BookRepository


@dataclass(slots=True, kw_only=True)
class BookUseCases:
    repository: BookRepository

    def create_book(self, book: Book) -> dict[str, Any]:
        return self.repository.add(book)

    def list_books(self) -> List[dict[str, Any]]:
        return self.repository.get_all()

    def get_by_id(self, book_id: int) -> dict[str, Any]:
        return self.repository.get_by_id(book_id)

    def get_by_user_id(self, user_id: int) -> List[dict[str, Any]]:
        return self.repository.get_by_user_id(user_id)
