"""**E-commerce API Extension:** Extend the e-commerce API example with endpoints for 
managing product categories. Include endpoints for creating, retrieving, updating, 
and deleting categories."""

import importlib
from fastapi import FastAPI
from .routers import products, users, categories
from .middlewares.logging import LoggingMiddleware
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Awesome API"
    debug: bool = False
    database_url: str = "sqlite:///./test.db"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore") # Load from .env file and ignore extra variables

def create_app(settings_module="config.development"):
    app = FastAPI()
    
    package = __package__ or __name__.rpartition('.')[0]
    if package and not settings_module.startswith(package) and not settings_module.startswith("."):
        import_name = f"{package}.{settings_module}"
    else:
        import_name = settings_module
    settings = importlib.import_module(import_name)
    app.state.settings = settings

    app.add_middleware(LoggingMiddleware)
    app.include_router(users.router)
    app.include_router(products.router)
    app.include_router(categories.router)

    return app

app = create_app(settings_module="config.production")

# Rodar com: uv run fastapi dev api.py