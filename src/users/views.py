from fastapi import APIRouter

from src.users.schemas import CreateUser
from src.users import crud

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/")
async def create_user(user: CreateUser):
    return await crud.create_user(user_in=user)