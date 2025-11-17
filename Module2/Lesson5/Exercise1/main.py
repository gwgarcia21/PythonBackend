from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, EmailStr
from typing import Optional

app = FastAPI()

class Product(BaseModel):
    name: str = Field(..., min_length=3, max_length=20)
    description: Optional[str] = Field(..., max_length=200)
    price: float = Field(..., gt=0)
    stock_quantity: int = Field(None, ge=0)

@app.post("/products")
def create_product(product : Product):
    print(f"Created product {product.name}")
