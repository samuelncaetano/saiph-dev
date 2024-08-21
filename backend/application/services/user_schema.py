from backend.domain.entities.user import User, UserModel


def user_to_pydantic(user: User) -> UserModel:
    return UserModel(id=user.id, name=user.name, email=user.email, password=user.password, age=user.age)


def pydantic_to_user(user_model: UserModel) -> User:
    return User(
        id=user_model.id, name=user_model.name, email=user_model.email, password=user_model.password, age=user_model.age
    )


def user_schema(user: User) -> User:
    validate = user_to_pydantic(user)
    return pydantic_to_user(validate)
