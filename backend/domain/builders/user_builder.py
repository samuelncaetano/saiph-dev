from dataclasses import dataclass

from typing_extensions import Self  # pylint: disable = E0401  # type: ignore

from backend.application.services.user_schema import user_schema
from backend.domain.entities.user import User


@dataclass
class UserBuilder:
    id: int = 0  # pylint: disable = C0103
    name: str = ""
    email: str = ""
    age: int = 0
    password: str = ""

    def with_id(self, id: int) -> Self:  # pylint: disable = C0103, W0622
        self.id = id
        return self

    def with_name(self, name: str) -> Self:
        self.name = name
        return self

    def with_email(self, email: str) -> Self:
        self.email = email
        return self

    def with_age(self, age: int) -> Self:
        self.age = age
        return self

    def with_password(self, password: str) -> Self:
        self.password = password
        return self

    def build(self) -> User:
        user = User(id=self.id, name=self.name, email=self.email, password=self.password, age=self.age)
        return user_schema(user)
