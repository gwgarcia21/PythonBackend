from passlib.context import CryptContext

pwd = CryptContext(schemes=["argon2"], deprecated="auto")
print(pwd.hash("1234"))