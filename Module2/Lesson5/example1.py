from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, EmailStr
from typing import Optional

app = FastAPI()

# Define a Pydantic model for user creation
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=20, regex="^[a-zA-Z0-9_]+$")
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: Optional[str] = Field(None, max_length=50)

# Define a Pydantic model for an item
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float = Field(..., gt=0) # Price must be greater than 0
    tax: Optional[float] = None

@app.post("/users/")
async def create_user(user: UserCreate):
    # Pydantic has already validated username, email, password length, and regex
    # If validation fails, FastAPI automatically returns a 422 Unprocessable Entity error
    print(f"User received: {user.username}, {user.email}")
    # In a real app, you would hash the password before storing it
    return {"message": "User created successfully", "username": user.username}

@app.post("/items/")
async def create_item(item: Item):
    # Pydantic validates item attributes, like price > 0
    if item.tax:
        price_with_tax = item.price + item.tax
    else:
        price_with_tax = item.price
    return {"item_name": item.name, "price_with_tax": price_with_tax}

# Example of query parameter validation
@app.get("/search/")
async def search_items(q: str = Field(..., min_length=2, max_length=50)):
    # FastAPI and Pydantic ensure 'q' is a string between 2 and 50 characters
    return {"query": q, "results": [f"Item for {q}"]}