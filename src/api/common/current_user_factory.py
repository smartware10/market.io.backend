from fastapi import Depends
from fastapi_users import FastAPIUsers

from core.models import User
from core.types.user_id import UserIdType
from api.dependencies.authentication import get_authentication_backend, get_user_manager

_fastapi_users_cache = {}


def get_current_user(
    version_api: str, active_user: bool = True, superuser: bool = False
):
    if version_api not in _fastapi_users_cache:
        from core.config import settings, get_token_url

        # Выбираем стратегию для версии и URL
        try:
            strategy = getattr(
                settings.api, version_api
            ).authentication_backend_strategy
            token_url = get_token_url(version_api)
        except AttributeError:
            raise ValueError(f"Invalid version API selected!. Got: {version_api}")

        # Создаем authentication_backend
        authentication_backend = get_authentication_backend(strategy, token_url)

        # Создаем FastAPIUsers
        fastapi_users = FastAPIUsers[User, UserIdType](
            get_user_manager,
            auth_backends=[authentication_backend],
        )

        _fastapi_users_cache[version_api] = fastapi_users

    fastapi_users = _fastapi_users_cache[version_api]

    return Depends(fastapi_users.current_user(active=active_user, superuser=superuser))
