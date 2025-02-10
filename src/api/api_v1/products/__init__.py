from fastapi import APIRouter

from core.config import settings
from .views import router as products_router

router = APIRouter(
    prefix=settings.api.v1.products,
    tags=["Products"],
)

router.include_router(router=products_router)
