from pathlib import Path
from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent.parent


class DatabaseConfig(BaseModel):
    # DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 15


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15


class ApiPrefix(BaseModel):
    prefix: str = "/api"


class Settings(BaseSettings):
    db: DatabaseConfig
    api: ApiPrefix = ApiPrefix()
    auth_jwt: AuthJWT = AuthJWT()


settings = Settings()
