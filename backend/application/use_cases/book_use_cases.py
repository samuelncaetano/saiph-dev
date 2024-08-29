from dataclasses import asdict, dataclass
from typing import Any, List

from backend.domain.entities.book import Book
from backend.infrastructure.repositories.book_repository import BookRepository


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

    def update_book(self, book: dict[str, Any]) -> dict[str, Any]:
        return self.repository.update(book)

    def toggle_book_status(self, book_id: int) -> dict[str, Any]:
        book_dict = self.get_by_id(book_id)
        book = Book(**book_dict)
        book.status = not book.status
        updated_book = self.update_book(asdict(book))
        return updated_book

    def delete_book(self, book_id: int) -> List[dict[str, Any]]:
        return self.repository.delete(book_id)
