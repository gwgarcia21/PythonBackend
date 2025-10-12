from fastapi import APIRouter, Depends
from typing import Optional
from ..utils.validation import verify_token

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

# Simulate a simple data store
users = {}

def fake_dependency(q: Optional[str] = None):
    return {"q": q}

@router.get("/", dependencies=[Depends(verify_token)])
async def read_users():
    """
    Retrieve all users.
    """
    return users

@router.get("/{user_id}")
async def read_user(user_id: int):
    """
    Retrieve a specific user by its ID.
    """
    if user_id in users:
        return users[user_id]
    return {"error": "User not found"}

@router.post("/")
async def create_user(user_id: int, name: str):
    """
    Create a new user.
    """
    users[user_id] = {"name": name}
    return {"user_id": user_id, "name": name}

@router.put("/{user_id}")
async def update_user(user_id: int, name: str):
    """
    Update a specific user by its ID.
    """
    if user_id in users:
        user = users[user_id]
        user["name"] = name
        return user
    return {"error": "User not found"}