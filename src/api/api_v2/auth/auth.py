from fastapi import APIRouter
from api.common.auth_router_factory import get_auth_router

router = APIRouter()

router.include_router(get_auth_router("v2"))
