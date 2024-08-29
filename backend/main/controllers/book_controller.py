from typing import Any, List

from backend.application.use_cases.book_use_cases import BookUseCases
from backend.domain.entities.book import Book


class BookController:
    def __init__(self, book_use_case: BookUseCases):
        self.book_use_case = book_use_case

    def create_book(self, book_data: dict[str, Any]) -> dict[str, Any]:
        book = Book(id=0, **book_data)
        return self.book_use_case.create_book(book)

    def list_books(self) -> List[dict[str, Any]]:
        return self.book_use_case.list_books()

    def get_by_id(self, book_id: int) -> dict[str, Any]:
        return self.book_use_case.get_by_id(book_id)

    def get_by_user_id(self, user_id: int) -> List[dict[str, Any]]:
        return self.book_use_case.get_by_user_id(user_id)

    def update_book(self, book_id: int, book_data: dict[str, Any]) -> dict[str, Any]:
        return self.book_use_case.update_book(book_id, book_data)

    def toggle_book_status(self, book_id: int) -> dict[str, Any]:
        return self.book_use_case.toggle_book_status(book_id)

    def delete_book(self, book_id: int) -> List[dict[str, Any]]:
        return self.book_use_case.delete_book(book_id)
