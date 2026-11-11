from datetime import datetime
from uuid import uuid4

import pytest
from pydantic import ValidationError

from app.models.user import User
from app.schemas.user import UserCreate, UserRead


def test_password_hashing_uses_a_salted_hash():
    password = "StrongPass123"

    first_hash = User.hash_password(password)
    second_hash = User.hash_password(password)

    assert first_hash != password
    assert first_hash != second_hash
    assert User.verify_password(User(password_hash=first_hash), password)
    assert not User.verify_password(User(password_hash=first_hash), "WrongPass123")


def test_password_property_returns_the_stored_hash():
    password_hash = User.hash_password("StrongPass123")
    user = User(password_hash=password_hash)

    assert user.password == password_hash


def test_user_create_validates_email_and_password():
    user = UserCreate(
        username="johndoe",
        email="john.doe@example.com",
        password="StrongPass123",
    )

    assert user.username == "johndoe"
    assert user.email == "john.doe@example.com"

    with pytest.raises(ValidationError):
        UserCreate(
            username="johndoe",
            email="not-an-email",
            password="StrongPass123",
        )


def test_user_create_requires_a_password():
    with pytest.raises(ValidationError):
        UserCreate(username="johndoe", email="john.doe@example.com")


def test_user_read_excludes_password_hash():
    user = User(
        id=uuid4(),
        username="johndoe",
        email="john.doe@example.com",
        password_hash=User.hash_password("StrongPass123"),
        created_at=datetime(2025, 1, 1),
    )

    result = UserRead.model_validate(user).model_dump()

    assert result["username"] == "johndoe"
    assert result["email"] == "john.doe@example.com"
    assert "password_hash" not in result
