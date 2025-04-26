from fastapi_users.authentication import AuthenticationBackend, BearerTransport

from .strategy_db import get_database_strategy
from .strategy_jwt import get_jwt_strategy

STRATEGIES = {
    "db": {
        "get_strategy": get_database_strategy,
        "name": "access-tokens-db",
    },
    "jwt": {
        "get_strategy": get_jwt_strategy,
        "name": "access-tokens-jwt",
    },
}


def get_authentication_backend(
    strategy_type: str, token_url: str
) -> AuthenticationBackend:
    strategy_config = STRATEGIES.get(strategy_type)

    if strategy_config is None:
        raise ValueError(
            f"Invalid strategy selected! Choose either 'db' or 'jwt'. Got: {strategy_type}"
        )

    # Создаем BearerTransport с нужным URL
    transport = BearerTransport(tokenUrl=token_url)

    return AuthenticationBackend(
        name=strategy_config["name"],
        transport=transport,
        get_strategy=strategy_config["get_strategy"],
    )
