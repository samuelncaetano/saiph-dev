from backend.domain.entities.book import Book, BookModel


def book_to_pydantic(book: Book) -> BookModel:
    return BookModel(id=book.id, title=book.title, user_id=book.user_id)


def pydantic_to_book(book_model: BookModel) -> Book:
    return Book(id=book_model.id, title=book_model.title, user_id=book_model.user_id)


def book_schema(book: Book) -> Book:
    validate = book_to_pydantic(book)
    return pydantic_to_book(validate)
