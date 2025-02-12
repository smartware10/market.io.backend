from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from core.config import settings
from .auth import router as auth_router

http_bearer = HTTPBearer(auto_error=False)

router = APIRouter(
    prefix=settings.api.v1.auth,
    tags=["Auth"],
    dependencies=[Depends(http_bearer)],
)

router.include_router(router=auth_router)
