from passlib.context import CryptContext
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
import datetime
from fastapi import Depends, HTTPException, status, FastAPI
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer

# Contexto com Argon2
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

class AuthConfig:
    SECRET_KEY = "48IKPH25.P$@#dwqX"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 60*24*360
    REFRESH_TOKEN_EXPIRE_MINUTES = 30

def create_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_hash(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)

def create_token(data: dict, expires_delta = AuthConfig.ACCESS_TOKEN_EXPIRE_MINUTES) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=expires_delta)
        to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, AuthConfig.SECRET_KEY, algorithm=AuthConfig.ALGORITHM)
    return encoded_jwt


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido ou expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, AuthConfig.SECRET_KEY, algorithms=[AuthConfig.ALGORITHM])
        user_email: str = payload.get("sub")
        if user_email is None:
            raise credentials_exception
        return user_email
    except JWTError:
        raise credentials_exception
    
async def token_is_admin(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido ou expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, AuthConfig.SECRET_KEY, algorithms=[AuthConfig.ALGORITHM])
        user_role: str = payload.get("role")
        if user_role == 'admin':
            return True
        else:
            return False
    except JWTError:
        raise credentials_exception
    