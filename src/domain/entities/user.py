from dataclasses import dataclass
from typing import Any

from pydantic import BaseModel, field_validator  # pylint: disable = E0401 # type: ignore


@dataclass(slots=True, kw_only=True)
class User:
    id: int  # pylint: disable = C0103
    name: str
    email: str
    age: int

    def get_name(self):
        return self.name

    def get_email(self):
        return self.email

    def get_age(self):
        return self.age


class UserModel(BaseModel):  # type: ignore
    id: int
    name: str
    email: str
    age: int

    @field_validator("name", "email", mode="before")
    def not_empty(cls, value: str, field: Any) -> str:
        if len(value) < 3:
            raise ValueError(f"O campo '{field.field_name}' deve ter pelo menos 3 caracteres")
        return value
