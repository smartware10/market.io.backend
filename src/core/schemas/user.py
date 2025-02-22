from datetime import date, datetime
from typing import Optional

from fastapi_users import schemas
from pydantic import BaseModel, ConfigDict

from core.types.user_id import UserIdType


class UserProfile(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={datetime: lambda v: v.strftime("%d/%m/%Y, %H:%M")},
    )

    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    middle_name: Optional[str] = None
    birth_date: Optional[date] = None


class UserProfileRead(UserProfile):
    registered_on: datetime


class UserRead(UserProfileRead, schemas.BaseUser[UserIdType]):
    pass


class UserCreate(UserProfile, schemas.BaseUserCreate):
    pass


class UserUpdate(UserProfile, schemas.BaseUserUpdate):
    pass
