from typing import Any, List

from src.application.services.book_schema import book_to_pydantic, pydantic_to_book
from src.application.use_cases.book_use_cases import BookUseCases
from src.domain.entities.book import Book, BookModel


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
        book_dict = self.get_by_id(book_id)
        book = pydantic_to_book(BookModel(**book_dict))
        for key, value in book_data.items():
            setattr(book, key, value)

        book_dict_pydantic = book_to_pydantic(book).model_dump()
        updated_book = self.book_use_case.update_book(book_dict_pydantic)  # type: ignore
        return updated_book

    def delete_book(self, book_id: int) -> List[dict[str, Any]]:
        return self.book_use_case.delete_book(book_id)
