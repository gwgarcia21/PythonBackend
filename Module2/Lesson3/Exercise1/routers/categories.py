from fastapi import APIRouter, Depends
from typing import Optional

router = APIRouter(
    prefix="/categories",
    tags=["categories"],
    responses={404: {"description": "Not found"}},
)

# Simulate a simple data store
categories = {}

def fake_dependency(q: Optional[str] = None):
    return {"q": q}

@router.get("/")
async def read_categories():
    """
    Retrieve all categories.
    """
    return categories

@router.get("/{category_id}")
async def read_category(category_id: int):
    """
    Retrieve a specific category by its ID.
    """
    if category_id in categories:
        return categories[category_id]
    return {"error": "category not found"}

@router.post("/")
async def create_category(category_id: int, name: str):
    """
    Create a new category.
    """
    categories[category_id] = {"name": name}
    return {"category_id": category_id, "name": name}

@router.put("/{category_id}")
async def update_category(category_id: int, name: str):
    categories[category_id] = {"name": name}
    return {"message": f"Category {category_id} updated successfully"}

@router.delete("/{category_id}")
async def delete_category(category_id: int):
    try:
        categories.pop(category_id)
    except KeyError:
        return {"error": "Category not found"}
    return {"message": f"Category {category_id} deleted successfully"}
