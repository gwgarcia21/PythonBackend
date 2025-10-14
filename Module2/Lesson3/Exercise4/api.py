"""Error Handling: Add more robust error handling to the user management API. 
Return specific error messages for different scenarios, such as invalid email 
format or duplicate user names."""

import importlib
from fastapi import APIRouter, FastAPI
from .routers.v1 import products as v1_products, users as v1_users, categories as v1_categories
from .routers.v2 import products as v2_products, users as v2_users, categories as v2_categories
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

    version_router_v1 = APIRouter(prefix=f"/v1")
    version_router_v1.include_router(v1_users.router)
    version_router_v1.include_router(v1_products.router)
    version_router_v1.include_router(v1_categories.router)

    app.include_router(version_router_v1)

    version_router_v2 = APIRouter(prefix=f"/v2")
    version_router_v2.include_router(v2_users.router)
    version_router_v2.include_router(v2_products.router)
    version_router_v2.include_router(v2_categories.router)

    app.include_router(version_router_v2)

    return app

app = create_app(settings_module="config.production")

# Rodar com: uv run fastapi dev api.py