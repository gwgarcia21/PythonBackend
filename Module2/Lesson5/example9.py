from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

app = FastAPI()

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        # HSTS is typically set by the web server (Nginx, Caddy)
        # but can be added here. Max-age should be long (e.g., 2 years)
        # response.headers["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains; preload"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        # CSP is complex and often needs to be endpoint-specific or configured with a specialized library
        # See XSS mitigation for an example.
        return response

app.add_middleware(SecurityHeadersMiddleware)

@app.get("/config_check")
async def config_check():
    return {"message": "Check your response headers!"}