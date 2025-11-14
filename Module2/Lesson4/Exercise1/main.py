""" Modify the code to include roles (e.g., "admin", "user") in the JWT payload.
Create a new endpoint that only administrators can access, using the role information in the JWT.
Implement refresh tokens. Create a /refresh_token endpoint that exchanges a valid refresh token for a new access token and refresh token """

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

    token = create_access_token({"sub": data.username, "role": fake_user["role"]})
    return {"access_token": token, "token_type": "bearer"}


@app.get("/me")
def protected_route(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)

    if payload is None:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")

    return {"message": "Acesso permitido!", "user": payload["sub"], "role": payload["role"]}

@app.get("/me")
def protected_route(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)

    if payload is None:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")

    return {"message": "Acesso permitido!", "user": payload["sub"], "role": payload["role"]}

@app.get("/admin")
def admin_route(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)

    if payload is None:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")

    if payload["role"] != "admin":
        raise HTTPException(status_code=403, detail="Acesso negado!")

    return {"message": "Acesso permitido!", "user": payload["sub"], "role": payload["role"]}

@app.get("/refresh_token")
def refresh_token(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)

    if payload is None:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")

    token = create_access_token({"sub": payload["sub"], "role": payload["role"]})
    return {"access_token": token, "token_type": "bearer"}