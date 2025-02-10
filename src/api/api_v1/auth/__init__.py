from fastapi import APIRouter

from core.config import settings

router = APIRouter(
    prefix=settings.api.v1.auth,
    tags=["Auth"],
)

router.include_router(router=router)
