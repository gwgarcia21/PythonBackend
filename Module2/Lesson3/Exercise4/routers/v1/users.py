from fastapi import APIRouter, Depends, Query, HTTPException, status
from typing import Optional
from ...dependencies.auth import verify_token

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

# Simulate a simple data store
users = [
    {"id": 1, "name": "Alice Johnson", "email": "alice.johnson@example.com"},
    {"id": 2, "name": "Bob Smith", "email": "bob.smith@example.com"},
    {"id": 3, "name": "Charlie Brown", "email": "charlie.brown@example.com"},
    {"id": 4, "name": "Diana Miller", "email": "diana.miller@example.com"},
    {"id": 5, "name": "Ethan Williams", "email": "ethan.williams@example.com"},
    {"id": 6, "name": "Fiona Davis", "email": "fiona.davis@example.com"},
    {"id": 7, "name": "George Wilson", "email": "george.wilson@example.com"},
    {"id": 8, "name": "Hannah Thompson", "email": "hannah.thompson@example.com"},
    {"id": 9, "name": "Ian Clark", "email": "ian.clark@example.com"},
    {"id": 10, "name": "Julia Roberts", "email": "julia.roberts@example.com"},
]

def fake_dependency(q: Optional[str] = None):
    return {"q": q}

@router.get("/")
async def read_users(
            name: Optional[str] = Query(None, description="Filter by name"),
            sort: Optional[str] = Query(None, description="Sort by field"),
            order: Optional[str] = Query("asc", description="Sort order (asc or desc)"),
        ):
    """
    Retrieve all users.
    """
    filtered_users = users
    if name:
        filtered_users = [p for p in users if p["name"] == name]

    if sort:
        reverse = order == "desc"
        filtered_users = sorted(filtered_users, key=lambda x: x[sort], reverse=reverse)
    return filtered_users

@router.get("/{user_id}")
async def read_user(user_id: int):
    """
    Retrieve a specific user by its ID.
    """
    if user_id in users:
        return users[user_id]
    return {"error": "User not found"}

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(name: str, email: str):
    """
    Create a new user.
    """
    if any(user["name"] == name for user in users) or any(user["email"] == email for user in users):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User already exists")
    # Logic to create a new user in the database
    new_id = max(user["id"] for user in users) + 1 if users else 1
    users.append({"id": new_id, "name": name, "email": email})
    return {"message": f"User {name} created successfully"}

@router.put("/{user_id}", dependencies=[Depends(verify_token)])
async def update_user(user_id: int, name: str):
    """
    Update a specific user by its ID.
    """
    if user_id in users:
        user = users[user_id]
        user["name"] = name
        return user
    return {"error": "User not found"}