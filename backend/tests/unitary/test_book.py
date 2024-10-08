from pathlib import Path
from typing import Any

import pytest  # type: ignore
from pydantic import ValidationError  # type: ignore

from backend.application.services.book_schema import book_to_pydantic
from backend.application.use_cases.book_use_cases import BookUseCases
from backend.domain.builders.book_builder import BookBuilder
from backend.domain.entities.book import Book
from backend.infrastructure.repositories.book_repository import BookRepository
from backend.main.controllers.book_controller import BookController


@pytest.fixture
def book_builder():
    return BookBuilder().with_title("1984").with_user_id(1).with_status(True).build()


@pytest.fixture
def temp_json_file(tmpdir):  # type: ignore
    file = tmpdir.join("database/books.json")
    file.ensure(file=True)
    file.write("[]")
    return Path(file)  # type: ignore


@pytest.fixture
def book_repository(temp_json_file: Any):
    return BookRepository(temp_json_file)


@pytest.fixture
def book_use_cases(book_repository: BookRepository):
    return BookUseCases(repository=book_repository)


@pytest.fixture
def book_controller(book_use_cases: BookUseCases):
    return BookController(book_use_case=book_use_cases)


@pytest.fixture
def book_list(book_controller: BookController):
    # Arrange
    books = [
        BookBuilder().with_title("1984").with_user_id(1).with_status(True).build(),
        BookBuilder().with_title("1984").with_user_id(1).with_status(False).build(),
        BookBuilder().with_title("1984").with_user_id(2).with_status(True).build(),
        BookBuilder().with_title("1984").with_user_id(2).with_status(False).build(),
    ]
    pydantic_books = list(map(book_to_pydantic, books))
    book_data_list = [book.model_dump() for book in pydantic_books]
    created_books = []

    # Act
    for book_data in book_data_list:
        book_data_without_id = book_data.copy()
        book_data_without_id.pop("id", None)
        status_code_create_book, created_book = book_controller.create_book(book_data_without_id)  # type: ignore
        created_books.append(created_book)

    return created_books


class TestBook:
    def test_instanciar_book(self, book_builder: Book):
        assert isinstance(book_builder, Book)

    def test_book_creation(self, book_builder: Book):
        assert book_builder.title == book_builder.get_title()
        assert book_builder.user_id == book_builder.get_user_id()
        assert book_builder.status == book_builder.get_status()

    def test_create_an_untitled_book(self):
        with pytest.raises(ValidationError):  # type: ignore
            BookBuilder().with_user_id(1).build()

    def test_create_a_book_without_user_id(self):
        with pytest.raises(ValidationError):  # type: ignore
            return BookBuilder().with_title("1984").build()


class TestRepository:
    def test_instanciar_user_repository(self, book_repository: BookRepository):
        assert isinstance(book_repository, BookRepository)


class TestController:
    def test_create_book(self, book_controller: BookController, book_builder: Book):
        # Arrange
        book_data_assert = book_to_pydantic(book_builder).model_dump()
        book_data = book_data_assert.copy()
        book_data_assert.update({"id": 1})
        book_data.pop("id", None)

        # Act
        status_code_create_book, created_book = book_controller.create_book(book_data)  # type: ignore

        # Assert
        assert created_book == book_data_assert

    def test_list_books(self, book_controller: BookController, book_list: list[Book]):
        # Act
        status_code_list_books, listed_books = book_controller.list_books()

        # Assert
        assert status_code_list_books == 200
        assert len(listed_books) == len(book_list)
        assert listed_books == book_list

    def test_get_book_by_id(self, book_controller: BookController, book_builder: Book):
        # Arrange
        book_data = book_to_pydantic(book_builder).model_dump()
        book_data.pop("id", None)

        # Act
        status_code_create_book, created_book = book_controller.create_book(book_data)  # type: ignore
        book_id: int = created_book["id"]
        status_code_get_by_id, fetched_book = book_controller.get_by_id(book_id)

        # Assert
        assert status_code_get_by_id == 200
        assert fetched_book == created_book

    def test_get_book_by_user_id(self, book_controller: BookController, book_list: list[Book], book_builder: Book):
        # Arrange
        user_id: int = book_builder.get_user_id()
        books = [
            {"id": 1, "title": "1984", "user_id": user_id, "status": True},
            {"id": 2, "title": "1984", "user_id": user_id, "status": False},
        ]

        # Act
        status_code_get_by_user_id, listed_books = book_controller.get_by_user_id(user_id)

        # Assert
        assert status_code_get_by_user_id == 200
        assert len(listed_books) == len(books)
        assert listed_books == books

    def test_update_book(self, book_controller: BookController, book_builder: Book):
        # Arrange
        update_data = {"title": "Admirável Mundo Novo"}
        book_data = book_to_pydantic(book_builder).model_dump()
        book_data.pop("id", None)

        # Act
        status_code_create_book, created_book = book_controller.create_book(book_data)  # type: ignore
        book_id = created_book["id"]
        status_code_update_book, updated_book = book_controller.update_book(book_id, update_data)

        # Assert
        assert status_code_update_book == 200
        assert updated_book.get("title") == update_data.get("title")

    def test_toggle_book_status(self, book_controller: BookController, book_builder: Book):
        # Arrange
        book_data = book_to_pydantic(book_builder).model_dump()
        book_data.pop("id", None)
        status_code_create_book, created_book = book_controller.create_book(book_data)  # type: ignore
        book_id = created_book["id"]

        # Act
        initial_status = created_book["status"]
        status_code_toggle_book_status, updated_book = book_controller.toggle_book_status(book_id)
        toggled_status = updated_book["status"]

        # Assert
        assert status_code_toggle_book_status == 200
        assert toggled_status == (not initial_status)

        # Act
        status_code_toggle_book_status, updated_book = book_controller.toggle_book_status(book_id)
        reverted_status = updated_book["status"]

        # Assert
        assert status_code_toggle_book_status == 200
        assert reverted_status == initial_status

    def test_delete_book(self, book_controller: BookController, book_builder: Book):
        # Arrange
        book_data = book_to_pydantic(book_builder).model_dump()
        book_data.pop("id", None)

        # Act
        status_code_create_book, created_book = book_controller.create_book(book_data)  # type: ignore
        book_id = created_book["id"]
        book_controller.delete_book(book_id)

        # Assert
        with pytest.raises(ValueError):
            book_controller.get_by_id(book_id)


if __name__ == "__main__":
    pytest.main([__file__, "-vv"])
