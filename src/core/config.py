from pathlib import Path
from typing import Literal

from pydantic import BaseModel, PostgresDsn, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent


class RunConfig(BaseModel):
    host: str = "localhost"
    port: int = 8000


class MiddlewareConfig(BaseModel):
    allow_origins: list[str] = [
        "http://localhost",
        "http://localhost:3000",
    ]
    allow_credentials: bool = True
    allow_methods: list[str] = ["*"]
    allow_headers: list[str] = ["*"]


class DatabaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 15

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 3600


class ApiV1Prefix(BaseModel):
    prefix: str = "/v1"
    auth: str = "/auth"
    users: str = "/users"
    products: str = "/products"
    categories: str = "/categories"

    # Choose either 'db' or 'jwt' for API v1
    authentication_backend_strategy: Literal["db", "jwt"] = "jwt"


class ApiV2Prefix(BaseModel):
    prefix: str = "/v2"
    auth: str = "/auth"

    # Choose either 'db' or 'jwt' for API v2
    authentication_backend_strategy: Literal["db", "jwt"] = "db"


class ApiPrefix(BaseModel):
    prefix: str = "/api"
    v1: ApiV1Prefix = ApiV1Prefix()
    v2: ApiV2Prefix = ApiV2Prefix()


class AccessToken(BaseModel):
    lifetime_seconds: int = 3600
    reset_password_token_secret: SecretStr
    verification_token_secret: SecretStr
    reset_password_token_audience: str = "Market.io: ResetPasswordToken"
    verification_token_audience: str = "Market.io: VerificationToken"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(BASE_DIR / ".env.template", BASE_DIR / ".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="MARKET__",
    )

    run: RunConfig = RunConfig()
    middleware: MiddlewareConfig = MiddlewareConfig()
    api: ApiPrefix = ApiPrefix()
    auth_jwt: AuthJWT = AuthJWT()
    db: DatabaseConfig
    access_token: AccessToken


settings = Settings()


def get_token_url(version: str) -> str:
    # /api/{version}/auth/login
    api = settings.api
    version_config = getattr(api, version)

    parts = [api.prefix, version_config.prefix, version_config.auth, "/login"]
    return "".join(parts).removeprefix("/")
