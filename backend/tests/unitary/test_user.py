from pathlib import Path
from typing import Any

import pytest  # type: ignore
from pydantic import ValidationError  # type: ignore

from backend.application.services.user_schema import user_to_pydantic
from backend.application.use_cases.user_use_cases import UserUseCases
from backend.domain.builders.user_builder import UserBuilder  # type: ignore
from backend.domain.entities.user import User  # type: ignore
from backend.infrastructure.repositories.user_repository import UserRepository
from backend.main.controllers.user_controller import UserController


@pytest.fixture
def user_builder():
    return (
        UserBuilder()
        .with_name("John Doe")
        .with_email("johndoe@example.com")
        .with_password("default")
        .with_age(0)
        .build()
    )


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


class TestUser:
    def test_instanciar_user(self, user_builder: User):
        assert isinstance(user_builder, User)

    def test_user_creation(self, user_builder: User):
        assert user_builder.name == user_builder.get_name()
        assert user_builder.email == user_builder.get_email()
        assert user_builder.age == user_builder.get_age()

    @pytest.mark.parametrize(
        "name, email, password, expected_error_field",
        [
            ("", "johndoe@example.com", "default", "name"),
            ("John", "", "default", "email"),
            ("John", "johndoe@example.com", "", "password"),
        ],
    )
    def test_user_model_validation_errors(self, name: str, email: str, password: str, expected_error_field: str):
        with pytest.raises(ValidationError) as exc_info:  # type: ignore
            UserBuilder().with_name(name).with_email(email).with_password(password).with_age(0).build()
        assert f"O campo '{expected_error_field}' deve ter pelo menos 3 caracteres" in str(
            exc_info.value  # type: ignore
        )


class TestRepository:
    def test_instanciar_user_repository(self, user_repository: UserRepository):
        assert isinstance(user_repository, UserRepository)


class TestController:
    def test_create_user(self, user_controller: UserController, user_builder: User):
        # Arrange
        user_data_assert = user_to_pydantic(user_builder).model_dump()
        user_data = user_data_assert.copy()
        user_data_assert.update({"id": 1})
        user_data.pop("id", None)

        # Act
        status_code_create_user, created_user = user_controller.create_user(user_data)  # type: ignore

        # Assert
        assert created_user == user_data_assert

    def test_create_user_email(self, user_controller: UserController, user_builder: User):
        # Arrange
        user_data_assert = user_to_pydantic(user_builder).model_dump()
        user_data = user_data_assert.copy()
        user_data_assert.update({"id": 1})
        user_data.pop("id", None)

        # Act
        user_controller.create_user(user_data)  # type: ignore

        # Assert
        with pytest.raises(ValueError):
            user_controller.create_user(user_data)  # type: ignore

    def test_list_users(self, user_controller: UserController):
        # Arrange
        users = [
            UserBuilder()
            .with_id(1)
            .with_name("John Doe")
            .with_email("johndoe@example.com")
            .with_password("default")
            .with_age(30)
            .build(),
            UserBuilder()
            .with_id(2)
            .with_name("Jane Doe")
            .with_email("janedoe@example.com")
            .with_password("default")
            .with_age(25)
            .build(),
        ]
        pydantic_users = list(map(user_to_pydantic, users))
        user_data_list = [user.model_dump() for user in pydantic_users]

        # Act
        created_users = []
        for user_data in user_data_list:
            user_data_without_id = user_data.copy()
            user_data_without_id.pop("id", None)
            status_code_create_user, created_user = user_controller.create_user(user_data_without_id)  # type: ignore
            created_users.append(created_user)
        status_code_list_users, listed_users = user_controller.list_users()

        # Assert
        assert status_code_list_users == 200
        assert len(listed_users) == len(users)
        assert listed_users == created_users

    def test_login_user(self, user_controller: UserController, user_builder: User):
        # Arrange
        user_data = user_to_pydantic(user_builder).model_dump()
        user_data.pop("id", None)
        login_data = {"email": user_data["email"], "password": user_data["password"]}

        # Act
        user_controller.create_user(user_data)  # type: ignore
        status_code_login_user, logged_user = user_controller.login_user(login_data)  # type: ignore

        # Assert
        assert logged_user["email"] == login_data["email"]

    def test_login_user_without_email_and_password(self, user_controller: UserController, user_builder: User):
        # Arrange
        user_data = user_to_pydantic(user_builder).model_dump()
        user_data.pop("id", None)
        login_data = {"email": "", "password": ""}

        # Act
        user_controller.create_user(user_data)  # type: ignore

        # Assert
        with pytest.raises(ValueError):
            user_controller.login_user(login_data)

    def test_get_user_by_id(self, user_controller: UserController, user_builder: User):
        # Arrange
        user_data = user_to_pydantic(user_builder).model_dump()
        user_data.pop("id", None)

        # Act
        status_code_create_user, created_user = user_controller.create_user(user_data)  # type: ignore
        user_id: int = created_user["id"]
        status_code_get_by_id, fetched_user = user_controller.get_by_id(user_id)

        # Assert
        assert status_code_get_by_id == 200
        assert fetched_user == created_user

    def test_update_user(self, user_controller: UserController, user_builder: User):
        # Arrange
        update_data = {"name": "Updated Name", "email": "updatedemail@example.com", "age": 35}
        user_data = user_to_pydantic(user_builder).model_dump()
        user_data.pop("id", None)

        # Act
        status_code_create_user, created_user = user_controller.create_user(user_data)  # type: ignore
        user_id = created_user["id"]
        status_code_update_user, updated_user = user_controller.update_user(user_id, update_data)

        # Assert
        assert status_code_update_user == 200
        assert updated_user["name"] == "Updated Name"
        assert updated_user["email"] == "updatedemail@example.com"
        assert updated_user["age"] == 35

    def test_delete_user(self, user_controller: UserController, user_builder: User):
        # Arrange
        user_data = user_to_pydantic(user_builder).model_dump()
        user_data.pop("id", None)

        # Act
        status_code_create_user, created_user = user_controller.create_user(user_data)  # type: ignore
        user_id = created_user["id"]
        user_controller.delete_user(user_id)

        # Assert
        with pytest.raises(ValueError):
            user_controller.get_by_id(user_id)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
