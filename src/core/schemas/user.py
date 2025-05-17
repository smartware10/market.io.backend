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
    """Базовая схема пользователя с основной информацией."""

    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={
            datetime: lambda v: v.strftime("%d/%m/%Y, %H:%M:%S"),
            date: lambda v: v.strftime("%d/%m/%Y"),
        },
    )

    email: EmailStr = Field(
        ...,
        description="Электронная почта пользователя (уникальная)",
        json_schema_extra={
            "format": "email, unique",
            "example": "example@market.io",
        },
    )
    is_active: Optional[bool] = Field(
        True,
        description="Признак того, что пользователь активен",
        json_schema_extra={
            "format": "boolean",
            "readOnly": True,
            "example": True,
        },
    )
    is_superuser: Optional[bool] = Field(
        False,
        description="Признак того, что пользователь является суперпользователем",
        json_schema_extra={
            "format": "boolean",
            "readOnly": True,
            "example": False,
        },
    )
    is_verified: Optional[bool] = Field(
        False,
        description="Признак того, что электронная почта подтверждена",
        json_schema_extra={
            "format": "boolean",
            "readOnly": True,
            "example": True,
        },
    )
    username: Optional[str] = Field(
        None,
        max_length=32,
        description="Имя пользователя (никнейм), (до 32 символов)",
        json_schema_extra={
            "format": "string",
            "maxLength": 32,
        },
    )
    first_name: Optional[str] = Field(
        None,
        max_length=32,
        description="Имя (до 32 символов)",
        json_schema_extra={
            "format": "string",
            "maxLength": 32,
        },
    )
    last_name: Optional[str] = Field(
        None,
        max_length=32,
        description="Фамилия (до 32 символов)",
        json_schema_extra={
            "format": "string",
            "maxLength": 32,
        },
    )
    middle_name: Optional[str] = Field(
        None,
        max_length=32,
        description="Отчество (до 32 символов)",
        json_schema_extra={
            "format": "string",
            "maxLength": 32,
        },
    )
    birth_date: Optional[date] = Field(
        None,
        description="Дата рождения (в формате 'ГГГГ-ММ-ДД')",
        json_schema_extra={
            "format": "date, YYYY-MM-DD",
            "example": "2020-01-20",
        },
    )


class UserProfileRead(UserProfile):
    """Схема для чтения данных пользователя."""

    id: int = Field(
        ...,
        description="Уникальный идентификатор пользователя",
        json_schema_extra={
            "format": "integer, unique",
            "readOnly": True,
        },
    )
    registered_on: datetime = Field(
        ...,
        description="Дата и время регистрации пользователя",
        json_schema_extra={
            "format": "datetime",
            "readOnly": True,
            "example": "22/11/2001, 19:14:01",
        },
    )


class UserReadList(RootModel[List["UserRead"]]):
    """Схема для чтения списка пользователей."""

    pass


class UserRead(UserProfileRead, schemas.BaseUser):
    """Схема для чтения пользователя, включая базовые поля из FastAPI Users."""

    pass


class UserCreate(UserProfile, schemas.BaseUserCreate):
    """Схема для создания нового пользователя."""

    password: str = Field(
        ...,
        description="Пароль пользователя (не менее 8 символов)",
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
        description="Повтор пароля",
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
                    "reason": "Пароли не совпадают",
                },
            )
        return value


class UserUpdate(UserProfile, schemas.BaseUserUpdate):
    """Схема для обновления данных пользователя."""

    email: Optional[EmailStr] = Field(
        None,
        description="Обновлённая электронная почта пользователя",
        json_schema_extra={
            "format": "email, unique",
            "example": "example@market.io",
        },
    )
    password: Optional[str] = Field(
        None,
        description="Новый пароль пользователя",
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
        description="Повтор пароля",
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
        description="Изменить статус активности пользователя",
        json_schema_extra={
            "format": "boolean",
            "example": False,
        },
    )
    is_superuser: Optional[bool] = Field(
        None,
        description="Изменить статус суперпользователя",
        json_schema_extra={
            "format": "boolean",
            "example": True,
        },
    )
    is_verified: Optional[bool] = Field(
        None,
        description="Подтверждена ли почта пользователя",
        json_schema_extra={
            "format": "boolean",
            "example": True,
        },
    )
    username: Optional[str] = Field(
        None,
        max_length=32,
        description="Обновлённое имя пользователя",
        json_schema_extra={
            "format": "string",
            "maxLength": 32,
        },
    )
    first_name: Optional[str] = Field(
        None,
        max_length=32,
        description="Обновлённое имя",
        json_schema_extra={
            "format": "string",
            "maxLength": 32,
        },
    )
    last_name: Optional[str] = Field(
        None,
        max_length=32,
        description="Обновлённая фамилия",
        json_schema_extra={
            "format": "string",
            "maxLength": 32,
        },
    )
    middle_name: Optional[str] = Field(
        None,
        max_length=32,
        description="Обновлённое отчество",
        json_schema_extra={
            "format": "string",
            "maxLength": 32,
        },
    )
    birth_date: Optional[date] = Field(
        None,
        description="Обновлённая дата рождения",
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
                    "reason": "Повтор пароля обязателен при смене пароля",
                },
            )

        if self.password != self.password_repeat:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "code": ErrorCode.UPDATE_USER_INVALID_PASSWORD,
                    "reason": "Пароли не совпадают",
                },
            )

        return self
