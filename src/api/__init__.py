from fastapi import APIRouter

from core.config import settings
from .api_v1 import router as router_api_v1
from .api_v2 import router as router_api_v2

router = APIRouter(
    prefix=settings.api.prefix,
)

router.include_router(
    router=router_api_v1,
)

router.include_router(
    router=router_api_v2,
)
