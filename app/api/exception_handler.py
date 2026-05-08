from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

async def custom_http_exception_handler(_request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "HttpException",
            "status_code": exc.status_code,
            "message": exc.detail,
            "details": []
        }
    )

def register_exception_handlers(api: FastAPI):
    api.add_exception_handler(StarletteHTTPException, custom_http_exception_handler)