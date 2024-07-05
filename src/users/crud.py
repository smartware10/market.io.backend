"""  Create Read Update Delete """
from src.users.schemas import CreateUser

async def create_user(user_in: CreateUser) -> dict:
    user = user_in.model_dump()
    return {
        "success": True,
        "user": user,
    }