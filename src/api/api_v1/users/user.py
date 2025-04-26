from typing import Annotated, TYPE_CHECKING, List

from fastapi import APIRouter, Depends
from starlette import status

from api.common import get_current_user
from api.dependencies import crud as common_crud
from core.helpers import db_helper, reset_database_helper
from core.models import User as UserModel
from core.schemas.user import UserRead

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
router = APIRouter()


@router.get(
    "/all_users/",
    name="users:get all users",
    status_code=status.HTTP_200_OK,
    response_model=List[UserRead],
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
    return await common_crud.get_all(session=session, model=UserModel)
