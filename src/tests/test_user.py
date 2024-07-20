from pathlib import Path
from typing import Any

import pytest  # type: ignore
from pydantic import ValidationError  # type: ignore

from src.application.services.user_schema import user_to_pydantic
from src.application.use_cases.user_use_cases import UserUseCases
from src.domain.builders.user_builder import UserBuilder  # type: ignore
from src.domain.entities.user import User  # type: ignore
from src.infrastructure.database.json.user_repository import UserRepository
from src.main.controllers.user_controller import UserController


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


@pytest.fixture
def user_use_cases(user_repository: UserRepository):
    return UserUseCases(repository=user_repository)


@pytest.fixture
def user_controller(user_use_cases: UserUseCases):
    return UserController(user_use_cases=user_use_cases)


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


def test_create_user(user_controller: UserController, user_builder: User):
    user_data = user_to_pydantic(user_builder).model_dump()

    created_user = user_controller.create_user(user_data)  # type: ignore

    assert created_user.name == user_builder.get_name()
    assert created_user.email == user_builder.get_email()
    assert created_user.age == user_builder.get_age()


def test_list_users(user_controller: UserController, user_repository: UserRepository):
    users = [
        UserBuilder().with_name("John Doe").with_email("johndoe@example.com").with_age(30).build(),
        UserBuilder().with_name("Jane Doe").with_email("janedoe@example.com").with_age(25).build(),
    ]

    pydantic_users = list(map(user_to_pydantic, users))

    user_data_list = [user.model_dump() for user in pydantic_users]

    for user_data in user_data_list:
        user_controller.create_user(user_data)  # type: ignore

    # Converta a string JSON para uma lista de dicionários
    listed_users = user_controller.list_users()

    assert len(listed_users) == len(users)
    assert listed_users == users


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
