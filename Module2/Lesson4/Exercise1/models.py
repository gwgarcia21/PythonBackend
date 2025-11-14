from pydantic import BaseModel

# Hash Argon2 da senha "1234" (gerado abaixo)
# Você pode gerar outros hashes no main.py depois.

fake_user = {
    "username": "guilherme",
    "password": "$argon2id$v=19$m=65536,t=3,p=4$qhUixPhfa41xjvHeG0MohQ$FKQ+l7QHNWswCPg0WSihV8x+9OJfwfXD81dUS9lx//I",  # senha: 1234
    "role": "user"
}

class UserLogin(BaseModel):
    username: str
    password: str
