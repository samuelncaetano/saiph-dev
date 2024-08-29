from typing import Any, List, Literal

from backend.application.use_cases.book_use_cases import BookUseCases
from backend.domain.entities.book import Book


class BookController:
    def __init__(self, book_use_case: BookUseCases):
        self.book_use_case = book_use_case

    def create_book(self, book_data: dict[str, Any]) -> tuple[Literal[201], dict[str, Any]]:
        book = self.book_use_case.create_book(Book(id=0, **book_data))
        return 201, book

    def list_books(self) -> tuple[Literal[200], List[dict[str, Any]]]:
        book = self.book_use_case.list_books()
        return 200, book

    def get_by_id(self, book_id: int) -> tuple[Literal[200], dict[str, Any]]:
        book = self.book_use_case.get_by_id(book_id)
        return 200, book

    def get_by_user_id(self, user_id: int) -> tuple[Literal[200], List[dict[str, Any]]]:
        book = self.book_use_case.get_by_user_id(user_id)
        return 200, book

    def update_book(self, book_id: int, book_data: dict[str, Any]) -> tuple[Literal[200], dict[str, Any]]:
        book = self.book_use_case.update_book(book_id, book_data)
        return 200, book

    def toggle_book_status(self, book_id: int) -> tuple[Literal[200], dict[str, Any]]:
        book = self.book_use_case.toggle_book_status(book_id)
        return 200, book

    def delete_book(self, book_id: int) -> tuple[Literal[200], List[dict[str, Any]]]:
        book = self.book_use_case.delete_book(book_id)
        return 200, book
