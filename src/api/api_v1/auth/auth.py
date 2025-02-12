from fastapi import APIRouter

from api.api_v1.auth.fastapi_users_router import fastapi_users
from api.dependencies.authentication.backend import authentication_backend
from core.schemas.user import UserRead, UserCreate

router = APIRouter()

router.include_router(
    router=fastapi_users.get_auth_router(authentication_backend),
)
router.include_router(
    router=fastapi_users.get_register_router(UserRead, UserCreate),
)
router.include_router(
    router=fastapi_users.get_verify_router(UserRead),
)
