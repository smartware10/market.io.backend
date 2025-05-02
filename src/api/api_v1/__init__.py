from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from core.config import settings
from .auth import router as auth_router
from .users import router as users_router
from .products import router as products_router
from .categories import router as categories_router


http_bearer = HTTPBearer(auto_error=False)
router = APIRouter(
    prefix=settings.api.v1.prefix,
    dependencies=[Depends(http_bearer)],
)

router.include_router(router=auth_router)
router.include_router(router=users_router)
router.include_router(router=categories_router)
router.include_router(router=products_router)
