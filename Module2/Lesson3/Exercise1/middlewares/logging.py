from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware to log the IP address of each incoming request.
    """
    async def dispatch(self, request: Request, call_next):
        if request.url.path == "/healthcheck":
            return await call_next(request)
        
        ip_address = request.headers.get("X-Forwarded-For", request.client.host)
        print(f"Request from IP address: {ip_address}")

        response = await call_next(request)
        return response