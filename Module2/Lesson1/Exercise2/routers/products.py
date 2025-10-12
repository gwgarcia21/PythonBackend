from fastapi import APIRouter, Depends
from typing import Optional

router = APIRouter(
    prefix="/products",
    tags=["products"],
    responses={404: {"description": "Not found"}},
)

# Simulate a simple data store
products = {}

def fake_dependency(q: Optional[str] = None):
    return {"q": q}

@router.get("/")
async def read_products():
    """
    Retrieve all products.
    """
    return products

@router.get("/{product_id}")
async def read_product(product_id: int):
    """
    Retrieve a specific user by its ID.
    """
    if product_id in products:
        return products[product_id]
    return {"error": "Product not found"}

@router.post("/")
async def create_product(product_id: int, name: str):
    """
    Create a new product.
    """
    products[product_id] = {"name": name}
    return {"product_id": product_id, "name": name}