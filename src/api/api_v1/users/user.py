from typing import Annotated, TYPE_CHECKING

from fastapi import APIRouter, Depends
from sqlalchemy import select

from api.api_v1.auth.fastapi_users_router import (
    fastapi_users,
    current_active_user,
    current_active_superuser,
)
from core.models import User, db_helper
from core.schemas.user import UserRead, UserUpdate

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
router = APIRouter()

# /me
router.include_router(
    router=fastapi_users.get_users_router(
        UserRead,
        UserUpdate,
        requires_verification=True,
    ),
)


@router.get("/all_users/")
async def get_all_users(
    current_user: Annotated[
        "User",
        Depends(current_active_superuser),
    ],
    users_db: Annotated[
        "AsyncSession",
        Depends(db_helper.session_getter),
    ],
):
    # Асинхронный запрос для получения всех пользователей
    result = await users_db.execute(select(User).order_by(User.id))
    users = result.scalars().all()  # Получаем все записи пользователей
    return [
        {
            "admin": UserRead.model_validate(current_user),
        },
        {"all_users": [UserRead.model_validate(user) for user in users]},
    ]


@router.get("/")
async def get_user(
    user: Annotated[
        User,
        Depends(current_active_user),
    ],
):
    return {
        "user": UserRead.model_validate(user),
    }


@router.get("/admin")
async def get_user(
    user: Annotated[
        User,
        Depends(current_active_superuser),
    ],
):
    return {
        "User": UserRead.model_validate(user),
    }
