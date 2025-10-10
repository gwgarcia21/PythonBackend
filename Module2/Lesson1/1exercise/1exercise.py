"""**Router Exercise:** Create a FastAPI application with two routers: one for `users` and one for `products`.
 The `users` router should have endpoints for creating, reading, and updating user profiles. 
 The `products` router should have endpoints for creating, reading, and listing products."""

from fastapi import FastAPI
from routers import products, users

def create_app():
    app = FastAPI()

    app.include_router(users.router)
    app.include_router(products.router)

    return app

app = create_app()