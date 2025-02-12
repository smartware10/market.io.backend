from typing import Annotated

from fastapi import APIRouter, Depends

from api.api_v1.auth.fastapi_users_router import (
    current_active_user,
    current_active_superuser_user,
)
from core.models import User
from core.schemas.user import UserRead

router = APIRouter()


@router.get("/")
async def get_user(
    user: Annotated[
        User,
        Depends(current_active_user),
    ],
):
    return {
        "User": UserRead.model_validate(user),
    }


@router.get("/admin")
async def get_user(
    user: Annotated[
        User,
        Depends(current_active_superuser_user),
    ],
):
    return {
        "User": UserRead.model_validate(user),
    }
