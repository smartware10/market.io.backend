from fastapi import APIRouter

from core.config import settings
from .views import router as users_router

router = APIRouter(
    prefix=settings.api.v1.users,
    tags=["Users"],
)

router.include_router(router=users_router)
