from fastapi import APIRouter

from core.config import settings
from .product import router as products_router

router = APIRouter(
    prefix=settings.api.v1.products,
    tags=["Products:v1"],
)

router.include_router(router=products_router)
