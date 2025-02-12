from fastapi_users.authentication import JWTStrategy

from core.config import settings


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=settings.auth_jwt.private_key_path.read_text(),
        lifetime_seconds=settings.auth_jwt.access_token_expire_minutes,
        algorithm=settings.auth_jwt.algorithm,
        public_key=settings.auth_jwt.public_key_path.read_text(),
    )
