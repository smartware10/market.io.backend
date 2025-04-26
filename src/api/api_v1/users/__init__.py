from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from core.config import settings
from .user import router as users_router

http_bearer = HTTPBearer(auto_error=False)

router = APIRouter(
    prefix=settings.api.v1.users,
    tags=["Users:v1"],
    dependencies=[Depends(http_bearer)],
)

router.include_router(router=users_router)
