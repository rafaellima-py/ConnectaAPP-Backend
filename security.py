from passlib.context import CryptContext

# Contexto com Argon2
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def create_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_hash(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)
