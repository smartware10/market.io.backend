"""  Create Read Update Delete """

from api.api_v1.users.schemas import CreateUser


async def create_user(user_in: CreateUser) -> dict:
    user = user_in.model_dump()
    return {
        "success": True,
        "user": user,
    }
