from dataclasses import dataclass, field
from typing import Any

from pydantic import BaseModel, field_validator  # pylint: disable = E0401 # type: ignore


@dataclass(slots=True, kw_only=True)
class Book:
    id: int  # pylint: disable = C0103
    title: str
    user_id: int
    status: bool = field(default=False)

    def get_title(self):
        return self.title

    def get_user_id(self):
        return self.user_id

    def get_status(self):
        return self.status


class BookModel(BaseModel):  # type: ignore
    id: int  # pylint: disable = C0103
    title: str
    user_id: int
    status: bool = False

    @field_validator("title", mode="before")
    def title_not_empty(cls, value: str, field: Any) -> str:  # pylint: disable = W0621
        if len(value) < 3:
            raise ValueError(
                f"O campo '{field.field_name}' deve ter pelo menos 3 caracteres"  # pylint: disable = W0621
            )
        return value

    @field_validator("user_id", mode="before")
    def user_id_not_empty(cls, value: int, field: Any) -> int:  # pylint: disable = W0621
        if value <= 0:
            raise ValueError(f"O campo '{field.field_name}' deve ser vazio")  # pylint: disable = W0621
        return value
