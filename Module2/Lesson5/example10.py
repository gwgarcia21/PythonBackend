from passlib.context import CryptContext # pip install passlib[bcrypt]

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Conceptual usage in a user creation and login flow
class UserLogin(BaseModel):
    username: str
    password: str

@app.post("/register")
async def register_user(user: UserCreate): # Use UserCreate from previous example
    hashed_pwd = hash_password(user.password)
    # Store user.username, user.email, hashed_pwd in database
    print(f"User {user.username} registered with hashed password.")
    return {"message": "User registered successfully"}

@app.post("/login")
async def login_user(user: UserLogin):
    # In a real app, retrieve stored_hashed_password for the user.username from DB
    stored_hashed_password = "$2b$12$Ejh9CjS0sY/eL.7HqB8.L.O.D.A.N.G.E.R.O.U.S.H.A.S.H" # Placeholder
    if verify_password(user.password, stored_hashed_password):
        return {"message": "Login successful"}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")