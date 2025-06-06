from typing import Annotated, TYPE_CHECKING

from fastapi import APIRouter, Depends
from starlette import status

from api.common import get_current_user
from api.dependencies import crud as common_crud
from core.helpers import db_helper
from core.models import User as UserModel
from core.schemas.user import UserReadList

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
router = APIRouter()


@router.get(
    "/",
    name="users:get all users",
    status_code=status.HTTP_200_OK,
    response_model=UserReadList,
    description="<h1>Get a list of all users</h1>",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Missing token or inactive user",
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "Not a superuser",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Internal Server Error",
        },
    },
)
async def get_all_users(
    current_user: Annotated[
        "UserModel",
        get_current_user("v1", superuser=True),
    ],
    session: Annotated[
        "AsyncSession",
        Depends(db_helper.session_getter),
    ],
):
    return await common_crud.get_all_object(session=session, model=UserModel)
