from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.schemas.base import PasswordMixin


class UserCreate(PasswordMixin):
    """Validated input for registering a user."""

    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    first_name: str = Field(default="", max_length=50)
    last_name: str = Field(default="", max_length=50)


class UserRead(BaseModel):
    """Public user details; password hashes are never serialized."""

    id: UUID
    username: str
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class UserResponse(BaseModel):
    """Schema for user response data"""
    id: UUID
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)  # Enable mapping from ORM objects


class Token(BaseModel):
    """Schema for authentication token response"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                "token_type": "bearer",
                "user": {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "username": "johndoe",
                    "email": "john.doe@example.com",
                    "first_name": "John",
                    "last_name": "Doe",
                    "is_active": True,
                    "is_verified": False,
                    "created_at": "2025-01-01T00:00:00",
                    "updated_at": "2025-01-08T12:00:00",
                },
            }
        }
    )


class TokenData(BaseModel):
    """Schema for JWT token payload"""
    user_id: Optional[UUID] = None


class UserLogin(BaseModel):
    """Schema for user login"""
    username: str
    password: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "username": "johndoe123",
                "password": "SecurePass123",
            }
        }
    )
