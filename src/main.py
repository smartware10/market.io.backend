import uvicorn
from fastapi import FastAPI, APIRouter

from src.users.views import router as users_router

app = FastAPI(
    title="Market.io",
)
app.include_router(users_router)


@app.get("/")
async def root():
    return {"message": "Market.io"}


if __name__ == '__main__':
    uvicorn.run('src.main:app', reload=True)
