from fastapi_users.authentication import AuthenticationBackend
from core.authentication.transport import bearer_transport
from core.config import settings

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

strategy_config = STRATEGIES.get(settings.api.v1.authentication_backend_strategy)

if strategy_config is None:
    raise ValueError(
        "Invalid strategy selected! Choose either 'db' or 'jwt' from configuration."
    )

authentication_backend = AuthenticationBackend(
    name=strategy_config["name"],
    transport=bearer_transport,
    get_strategy=strategy_config["get_strategy"],
)
