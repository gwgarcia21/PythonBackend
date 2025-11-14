from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from auth import create_access_token, verify_token
from models import UserLogin, fake_user

app = FastAPI()

# 🔥 AGORA USANDO ARGON2
pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def authenticate_user(username: str, password: str):
    if username != fake_user["username"]:
        return False

    if not pwd_context.verify(password, fake_user["password"]):
        return False

    return True


@app.post("/login")
def login(data: UserLogin):
    if not authenticate_user(data.username, data.password):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    token = create_access_token({"sub": data.username})
    return {"access_token": token, "token_type": "bearer"}


@app.get("/me")
def protected_route(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)

    if payload is None:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")

    return {"message": "Acesso permitido!", "user": payload["sub"]}
