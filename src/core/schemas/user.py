import re
from datetime import date, datetime
from typing import Optional, List

from fastapi_users import schemas
from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    field_validator,
    RootModel,
)
from pydantic_core.core_schema import ValidationInfo

from core.types.user_id import UserIdType


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
        ..., description="Электронная почта пользователя (уникальная)"
    )
    password: str = Field(
        ...,
        min_length=8,
        exclude=True,
        description="Пароль пользователя (не менее 8 символов)",
    )
    is_active: Optional[bool] = Field(
        True, description="Признак того, что пользователь активен"
    )
    is_superuser: Optional[bool] = Field(
        False, description="Признак того, что пользователь является суперпользователем"
    )
    is_verified: Optional[bool] = Field(
        False, description="Признак того, что электронная почта подтверждена"
    )
    username: Optional[str] = Field(
        None, max_length=24, description="Имя пользователя (никнейм)"
    )
    first_name: Optional[str] = Field(None, max_length=24, description="Имя")
    last_name: Optional[str] = Field(None, max_length=24, description="Фамилия")
    middle_name: Optional[str] = Field(None, max_length=24, description="Отчество")
    birth_date: Optional[date] = Field(None, description="Дата рождения")


class UserProfileRead(UserProfile):
    """Схема для чтения данных пользователя."""

    id: int = Field(..., description="Уникальный идентификатор пользователя")
    registered_on: datetime = Field(
        ..., description="Дата и время регистрации пользователя"
    )


class UserReadList(RootModel[List["UserRead"]]):
    """Схема для чтения списка пользователей."""

    pass


class UserRead(UserProfileRead, schemas.BaseUser[UserIdType]):
    """Схема для чтения пользователя, включая базовые поля из FastAPI Users."""

    pass


class UserCreate(UserProfile, schemas.BaseUserCreate):
    """Схема для создания нового пользователя."""

    password: str = Field(
        ..., min_length=8, description="Пароль пользователя (не менее 8 символов)"
    )
    password_repeat: str = Field(..., min_length=8, description="Повтор пароля")

    @field_validator("password", mode="after")  # noqa
    @classmethod
    def validate_password(cls, value: str, info: ValidationInfo) -> str:
        if value.isnumeric():
            raise ValueError(
                f"{info.field_name}: пароль не может состоять только из цифр"
            )
        if not re.search(r"[A-Za-z]", value):
            raise ValueError(f"{info.field_name}: должен содержать хотя бы одну букву")
        return value

    @field_validator("password_repeat", mode="after")  # noqa
    @classmethod
    def check_passwords_match(cls, value: str, info: ValidationInfo) -> str:
        if value != info.data.get("password"):
            raise ValueError("Пароли не совпадают")
        return value


class UserUpdate(UserProfile, schemas.BaseUserUpdate):
    """Схема для обновления данных пользователя."""

    email: Optional[EmailStr] = Field(
        None, description="Обновлённая электронная почта пользователя"
    )
    password: Optional[str] = Field(
        None, min_length=8, description="Новый пароль пользователя"
    )
    is_active: Optional[bool] = Field(
        None, description="Изменить статус активности пользователя"
    )
    is_superuser: Optional[bool] = Field(
        None, description="Изменить статус суперпользователя"
    )
    is_verified: Optional[bool] = Field(
        None, description="Подтверждена ли почта пользователя"
    )
    username: Optional[str] = Field(
        None, max_length=24, description="Обновлённое имя пользователя"
    )
    first_name: Optional[str] = Field(
        None, max_length=24, description="Обновлённое имя"
    )
    last_name: Optional[str] = Field(
        None, max_length=24, description="Обновлённая фамилия"
    )
    middle_name: Optional[str] = Field(
        None, max_length=24, description="Обновлённое отчество"
    )
    birth_date: Optional[date] = Field(None, description="Обновлённая дата рождения")
