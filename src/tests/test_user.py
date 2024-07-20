from pathlib import Path
from typing import Any

import pytest  # type: ignore
from pydantic import ValidationError  # type: ignore

from src.domain.builders.user_builder import UserBuilder  # type: ignore
from src.domain.entities.user import User  # type: ignore
from src.infrastructure.database.json.user_repository import UserRepository


@pytest.fixture
def user_builder():
    return UserBuilder().with_name("John Doe").with_email("johndoe@example.com").with_age(0).build()


@pytest.fixture
def temp_json_file(tmpdir):  # type: ignore
    file = tmpdir.join("database/users.json")
    file.ensure(file=True)
    file.write("[]")
    return Path(file)  # type: ignore


@pytest.fixture
def user_repository(temp_json_file: Any):
    return UserRepository(temp_json_file)


def test_instanciar_user(user_builder: User):
    assert isinstance(user_builder, User)


def test_instanciar_user_repository(user_repository: UserRepository):
    assert isinstance(user_repository, UserRepository)


def test_user_creation(user_builder: User):
    assert user_builder.name == user_builder.get_name()
    assert user_builder.email == user_builder.get_email()
    assert user_builder.age == user_builder.get_age()


@pytest.mark.parametrize(
    "name, email, expected_error_field",
    [
        ("", "johndoe@example.com", "name"),
        ("John", "", "email"),
    ],
)
def test_user_model_validation_errors(name: str, email: str, expected_error_field: str):
    with pytest.raises(ValidationError) as exc_info:
        UserBuilder().with_name(name).with_email(email).with_age(0).build()
    assert f"O campo '{expected_error_field}' deve ter pelo menos 3 caracteres" in str(exc_info.value)  # type: ignore


def test_add_user(user_repository: UserRepository, user_builder: User):
    user_repository.add(user_builder)
    users = user_repository.get_all()
    assert len(users) == 1
    assert users[0].name == user_builder.get_name()
    assert users[0].email == user_builder.get_email()
    assert users[0].age == user_builder.get_age()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
