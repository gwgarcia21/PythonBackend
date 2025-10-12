"""Middleware Exercise: Create a middleware that logs the IP address 
of each incoming request. Configure the middleware to exclude logging 
for requests to /healthcheck endpoint."""

from fastapi import FastAPI
from .routers import products, users
from .middlewares.logging import LoggingMiddleware

def create_app():
    app = FastAPI()

    app.add_middleware(LoggingMiddleware)
    app.include_router(users.router)
    app.include_router(products.router)

    return app

app = create_app()

# Rodar com: uv run fastapi dev 2exercise.py