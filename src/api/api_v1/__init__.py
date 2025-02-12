from fastapi import APIRouter

from core.config import settings
from .auth import router as auth_router
from .users import router as users_router

# from .products import router as products_router
#
router = APIRouter(
    prefix=settings.api.v1.prefix,
)

router.include_router(router=auth_router)
router.include_router(router=users_router)
# router.include_router(router=products_router)
