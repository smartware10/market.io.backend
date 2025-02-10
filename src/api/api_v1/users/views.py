from fastapi import APIRouter

from api.api_v1.users.schemas import CreateUser
from api.api_v1.users import crud

router = APIRouter()


@router.post("/")
async def create_user(user: CreateUser):
    return await crud.create_user(user_in=user)
