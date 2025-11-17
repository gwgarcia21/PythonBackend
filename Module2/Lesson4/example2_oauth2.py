from fastapi import FastAPI, Depends
from fastapi_users import FastAPIUsers, models
from fastapi_users.authentication import AuthenticationBackend, BearerTransport
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Optional

# Database setup
DATABASE_URL = "sqlite:///./test.db"  # Use a proper database in production
engine = create_engine(DATABASE_URL)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)

Base.metadata.create_all(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# FastAPI Users setup
bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

class UserDB(SQLAlchemyUserDatabase):
    pass

class User(models.BaseUser):
    pass

class UserCreate(models.BaseUserCreate):
    pass

class UserUpdate(User, models.BaseUserUpdate):
    pass

class UserRead(User, models.BaseUser):
    pass


def get_user_db():
    db = SessionLocal()
    try:
        yield UserDB(db, User)
    finally:
        db.close()

authentication_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=lambda: None,  # Replace with your JWT strategy (fastapi_users.authentication.JWTStrategy)
)

fastapi_users = FastAPIUsers(
    UserRead,
    UserCreate,
    authentication_backend,
    get_user_db,
)

app = FastAPI()

app.include_router(
    fastapi_users.get_auth_router(authentication_backend), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate), prefix="/auth", tags=["auth"]
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate), prefix="/users", tags=["users"]
)

@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(fastapi_users.get_current_active_user)):
    return {"message": f"Hello, {user.email}! You are authenticated."}
