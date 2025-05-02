from fastapi import APIRouter

from core.config import settings
from .user import router as users_router


router = APIRouter(
    prefix=settings.api.v1.users,
    tags=["Users:v1"],
)

router.include_router(router=users_router)
