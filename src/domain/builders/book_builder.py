from dataclasses import dataclass

from typing_extensions import Self  # pylint: disable = E0401  # type: ignore

from src.application.services.book_schema import book_schema
from src.domain.entities.book import Book


@dataclass(slots=True, kw_only=True)
class BookBuilder:
    id: int = 0  # pylint: disable = C0103
    title: str = ""
    user_id: int = 0

    def with_title(self, title: str) -> Self:
        self.title = title
        return self

    def with_user_id(self, user_id: int) -> Self:
        self.user_id = user_id
        return self

    def build(self) -> Book:
        book = Book(id=self.id, title=self.title, user_id=self.user_id)
        return book_schema(book)
