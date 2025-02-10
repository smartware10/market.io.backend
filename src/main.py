from contextlib import asynccontextmanager
from fastapi import FastAPI

import uvicorn


from core.config import settings
from api import router as api_router
from core.models import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load App

    yield
    # Exit App
    await db_helper.dispose()


main_app = FastAPI(title="Market.io", lifespan=lifespan)
main_app.include_router(router=api_router)


@main_app.get("/")
async def root():
    return {"message": "Market.io"}


if __name__ == "__main__":
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
