from dataclasses import dataclass

from typing_extensions import Self  # pylint: disable = E0401

from src.application.services.user_schema import user_schema
from src.domain.entities.user import User


@dataclass
class UserBuilder:
    id: int = 0  # pylint: disable = C0103
    name: str = ""
    email: str = ""
    age: int = 0

    def with_name(self, name: str) -> Self:
        self.name = name
        return self

    def with_email(self, email: str) -> Self:
        self.email = email
        return self

    def with_age(self, age: int) -> Self:
        self.age = age
        return self

    def build(self) -> User:
        user = User(id=self.id, name=self.name, email=self.email, age=self.age)
        return user_schema(user)
