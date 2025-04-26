from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from core.config import settings
from .auth import router as auth_router

http_bearer = HTTPBearer(auto_error=False)

router = APIRouter(
    prefix=settings.api.v2.auth,
    tags=["Auth:v2"],
    dependencies=[Depends(http_bearer)],
)

router.include_router(router=auth_router)
