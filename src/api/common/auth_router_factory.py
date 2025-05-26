from fastapi import APIRouter
from fastapi_users import FastAPIUsers

from core.models import User
from core.types.user_id import UserIdType
from core.schemas.user import UserCreate, UserUpdate, UserRead

from api.dependencies.authentication import get_authentication_backend, get_user_manager


def get_auth_router(version_api: str) -> APIRouter:
    from core.config import settings, get_token_url

    router = APIRouter()

    # Choosing a strategy for version and URL
    try:
        strategy = getattr(settings.api, version_api).authentication_backend_strategy
        token_url = get_token_url(version_api)
    except AttributeError:
        raise AttributeError(f"Invalid version API selected!. Got: {version_api}")

    # Create authentication_backend
    authentication_backend = get_authentication_backend(strategy, token_url)

    # Create FastAPIUsers
    fastapi_users = FastAPIUsers[User, UserIdType](
        get_user_manager,
        auth_backends=[authentication_backend],
    )

    # /login
    # /logout
    router.include_router(
        fastapi_users.get_auth_router(
            authentication_backend,
            requires_verification=True,
        ),
    )

    # /me
    router.include_router(
        router=fastapi_users.get_users_router(
            UserRead,
            UserUpdate,
            requires_verification=True,
        ),
    )

    # /register
    router.include_router(
        fastapi_users.get_register_router(UserRead, UserCreate),
    )

    # /request-verify-token
    # /verify
    router.include_router(
        fastapi_users.get_verify_router(UserRead),
    )

    # /forgot-password
    # /reset-password
    router.include_router(
        fastapi_users.get_reset_password_router(),
    )

    return router
