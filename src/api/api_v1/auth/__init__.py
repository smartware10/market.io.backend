from fastapi import APIRouter

from core.config import settings
from .auth import router as auth_router

router = APIRouter(
    prefix=settings.api.v1.auth,
    tags=["Auth:v1"],
)

router.include_router(router=auth_router)
