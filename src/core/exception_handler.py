from fastapi import Request, status, HTTPException
from fastapi.responses import JSONResponse

from main import main_app


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
