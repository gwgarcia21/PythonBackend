import os
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

ENV = os.getenv("APP_ENV", "dev")

CSP_PROD = (
    "default-src 'none'; "
    "script-src 'self'; "
    "style-src 'self'; "
    "img-src 'self'; "
    "font-src 'self'; "
    "connect-src 'self'; "
    "frame-ancestors 'none'; "
    "base-uri 'none'; "
    "object-src 'none';"
)

class SecurityMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request : Request, call_next):
        print(ENV)
        response = await call_next(request)
        if ENV == "prod":
            response.headers["Content-Security-Policy"] = CSP_PROD
        return response
