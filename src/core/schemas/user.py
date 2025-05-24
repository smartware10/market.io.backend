from datetime import date, datetime
from typing import Optional, List, Self

from fastapi import HTTPException, status
from fastapi_users import schemas
from fastapi_users.router import ErrorCode
from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    RootModel,
    field_validator,
    model_validator,
)
from pydantic_core.core_schema import ValidationInfo


class UserProfile(BaseModel):
    """Base user schema with main profile information."""

    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={
            datetime: lambda v: v.strftime("%d/%m/%Y, %H:%M:%S"),
            date: lambda v: v.strftime("%d/%m/%Y"),
        },
    )

    email: EmailStr = Field(
        ...,
        description="User's email (must be unique)",
        json_schema_extra={
            "format": "email, unique",
            "example": "example@market.io",
        },
    )
    is_active: Optional[bool] = Field(
        True,
        description="Indicates whether the user is active",
        json_schema_extra={
            "format": "boolean",
            "readOnly": True,
            "example": True,
        },
    )
    is_superuser: Optional[bool] = Field(
        False,
        description="Indicates whether the user is a superuser",
        json_schema_extra={
            "format": "boolean",
            "readOnly": True,
            "example": False,
        },
    )
    is_verified: Optional[bool] = Field(
        False,
        description="Indicates whether the email is verified",
        json_schema_extra={
            "format": "boolean",
            "readOnly": True,
            "example": True,
        },
    )
    username: Optional[str] = Field(
        None,
        max_length=32,
        description="Username (up to 32 characters)",
        json_schema_extra={
            "format": "string",
            "maxLength": 32,
        },
    )
    first_name: Optional[str] = Field(
        None,
        max_length=32,
        description="First name (up to 32 characters)",
        json_schema_extra={
            "format": "string",
            "maxLength": 32,
        },
    )
    last_name: Optional[str] = Field(
        None,
        max_length=32,
        description="Last name (up to 32 characters)",
        json_schema_extra={
            "format": "string",
            "maxLength": 32,
        },
    )
    middle_name: Optional[str] = Field(
        None,
        max_length=32,
        description="Middle name (up to 32 characters)",
        json_schema_extra={
            "format": "string",
            "maxLength": 32,
        },
    )
    birth_date: Optional[date] = Field(
        None,
        description="Birth date (in format 'YYYY-MM-DD')",
        json_schema_extra={
            "format": "date, YYYY-MM-DD",
            "example": "2020-01-20",
        },
    )


class UserProfileRead(UserProfile):
    """Schema for reading user data."""

    id: int = Field(
        ...,
        description="Unique user identifier",
        json_schema_extra={
            "format": "integer, unique",
            "readOnly": True,
        },
    )
    registered_on: datetime = Field(
        ...,
        description="User registration date and time",
        json_schema_extra={
            "format": "datetime",
            "readOnly": True,
            "example": "22/11/2001, 19:14:01",
        },
    )


class UserReadList(RootModel[List["UserRead"]]):
    """Schema for reading a list of users."""

    pass


class UserRead(UserProfileRead, schemas.BaseUser):
    """Schema for reading a user, including base fields from FastAPI Users."""

    pass


class UserCreate(UserProfile, schemas.BaseUserCreate):
    """Schema for creating a new user."""

    password: str = Field(
        ...,
        description="User password (minimum 8 characters)",
        json_schema_extra={
            "minLength": 8,
            "maxLength": 128,
            "pattern": r"^(?!\d+$).*$",
            "example": "MyStrongPassword123",
            "writeOnly": True,
        },
    )
    password_repeat: str = Field(
        ...,
        exclude=True,
        description="Password confirmation",
        json_schema_extra={
            "minLength": 8,
            "maxLength": 128,
            "pattern": r"^(?!\d+$).*$",
            "example": "MyStrongPassword123",
            "writeOnly": True,
        },
    )

    @field_validator("password_repeat", mode="after")  # noqa
    @classmethod
    def check_passwords_match(cls, value: str, info: ValidationInfo) -> str:
        if value != info.data.get("password"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "code": ErrorCode.REGISTER_INVALID_PASSWORD,
                    "reason": "Passwords do not match",
                },
            )
        return value


class UserUpdate(UserProfile, schemas.BaseUserUpdate):
    """Schema for updating user data."""

    email: Optional[EmailStr] = Field(
        None,
        description="Updated user email",
        json_schema_extra={
            "format": "email, unique",
            "example": "example@market.io",
        },
    )
    password: Optional[str] = Field(
        None,
        description="New user password",
        json_schema_extra={
            "minLength": 8,
            "maxLength": 128,
            "pattern": r"^(?!\d+$).*$",
            "example": "MyStrongPassword123",
            "writeOnly": True,
        },
    )
    password_repeat: Optional[str] = Field(
        None,
        exclude=True,
        description="Password confirmation",
        json_schema_extra={
            "minLength": 8,
            "maxLength": 128,
            "pattern": r"^(?!\d+$).*$",
            "example": "MyStrongPassword123",
            "writeOnly": True,
        },
    )
    is_active: Optional[bool] = Field(
        None,
        description="Change user active status",
        json_schema_extra={
            "format": "boolean",
            "example": False,
        },
    )
    is_superuser: Optional[bool] = Field(
        None,
        description="Change user superuser status",
        json_schema_extra={
            "format": "boolean",
            "example": True,
        },
    )
    is_verified: Optional[bool] = Field(
        None,
        description="Indicates if the user's email is verified",
        json_schema_extra={
            "format": "boolean",
            "example": True,
        },
    )
    username: Optional[str] = Field(
        None,
        max_length=32,
        description="Updated username",
        json_schema_extra={
            "format": "string",
            "maxLength": 32,
        },
    )
    first_name: Optional[str] = Field(
        None,
        max_length=32,
        description="Updated first name",
        json_schema_extra={
            "format": "string",
            "maxLength": 32,
        },
    )
    last_name: Optional[str] = Field(
        None,
        max_length=32,
        description="Updated last name",
        json_schema_extra={
            "format": "string",
            "maxLength": 32,
        },
    )
    middle_name: Optional[str] = Field(
        None,
        max_length=32,
        description="Updated middle name",
        json_schema_extra={
            "format": "string",
            "maxLength": 32,
        },
    )
    birth_date: Optional[date] = Field(
        None,
        description="Updated birth date",
        json_schema_extra={
            "format": "date, YYYY-MM-DD",
            "example": "2020-01-20",
        },
    )

    @model_validator(mode="after")
    def check_passwords_match(self) -> Self:
        if self.password is None:
            return self

        if not self.password_repeat:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "code": ErrorCode.UPDATE_USER_INVALID_PASSWORD,
                    "reason": "Password confirmation is required when changing the password",
                },
            )

        if self.password != self.password_repeat:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "code": ErrorCode.UPDATE_USER_INVALID_PASSWORD,
                    "reason": "Passwords do not match",
                },
            )

        return self
