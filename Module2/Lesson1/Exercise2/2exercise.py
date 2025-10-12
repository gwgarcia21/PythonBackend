"""Dependency Injection Exercise: Implement a dependency function that retrieves the current user 
from the database based on a JWT token passed in the request headers. Use this dependency in 
several route handlers to protect access to sensitive data."""

from fastapi import FastAPI
from .routers import products, users

def create_app():
    app = FastAPI()

    app.include_router(users.router)
    app.include_router(products.router)

    return app

app = create_app()

# Rodar com: uv run fastapi dev 2exercise.py