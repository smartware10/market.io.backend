from contextlib import asynccontextmanager
from typing import AsyncGenerator

import uvicorn

from fastapi import FastAPI, Request, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from api import router as api_router
from core.helpers import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # Load App
    yield
    # Exit App
    await db_helper.dispose()


main_app = FastAPI(
    title="Market.io",
    description="Market.io API documentation",
    version="1.0.0",
    lifespan=lifespan,
)
main_app.include_router(router=api_router)

# Добавление CORS middleware
main_app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.middleware.allow_origins,
    allow_credentials=settings.middleware.allow_credentials,
    allow_methods=settings.middleware.allow_methods,
    allow_headers=settings.middleware.allow_headers,
)


@main_app.exception_handler(403)
async def forbidden_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={
            "detail": {
                "code": exc.status_code,
                "reason": {
                    "error": exc.detail,
                    "method": request.method,
                    "url": str(request.url),
                },
            },
        },
    )


@main_app.exception_handler(404)
async def not_found_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "detail": {
                "code": exc.status_code,
                "reason": {
                    "error": exc.detail,
                    "method": request.method,
                    "url": str(request.url),
                },
            },
        },
    )


if __name__ == "__main__":
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
