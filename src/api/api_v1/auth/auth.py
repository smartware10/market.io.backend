from fastapi import APIRouter

from api.dependencies.authentication import authentication_backend
from core.schemas.user import UserRead, UserCreate
from .fastapi_users_router import fastapi_users

router = APIRouter()

# /login
# /logout
router.include_router(
    router=fastapi_users.get_auth_router(
        authentication_backend,
        requires_verification=True,
    ),
)

# /register
router.include_router(
    router=fastapi_users.get_register_router(UserRead, UserCreate),
)

# /request-verify-token
# /verify
router.include_router(
    router=fastapi_users.get_verify_router(UserRead),
)

# /forgot-password
# /reset-password
router.include_router(
    router=fastapi_users.get_reset_password_router(),
)
