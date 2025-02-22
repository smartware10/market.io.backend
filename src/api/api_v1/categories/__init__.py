from fastapi import APIRouter

from core.config import settings
from .category import router as categories_router

router = APIRouter(
    prefix=settings.api.v1.categories,
    tags=["Categories"],
)

router.include_router(router=categories_router)
