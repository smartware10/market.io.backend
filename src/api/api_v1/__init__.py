from fastapi import APIRouter

from core.config import settings
from .products.views import router as products_router
from .users.views import router as users_router

router = APIRouter(prefix=settings.api.v1.prefix)

router.include_router(router=products_router)
router.include_router(router=users_router)
