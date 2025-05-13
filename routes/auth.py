from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from scheema import *
from database import Database
from security import create_hash, verify_hash
db = Database()
auth_router = APIRouter()

@auth_router.post("/login")
async def login(login: UserLogin):
    user = await db.get_user(login.email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario não encontrado")
    
    if str(user) == str(login.email) and verify_hash(login.password, user.password):
        return JSONResponse(content={'user':user.email, 'password':user.password}, status_code=status.HTTP_200_OK)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário ou senha inválidos")
    
@auth_router.post("/register")
async def register(register: UserRegister):
    user = await db.get_user(register.email)
    if not user:
        password = create_hash(register.password)
        register.password = password
        await db.register_user(register)
        return JSONResponse(content={'user':register.email, 'password':register.password}, status_code=status.HTTP_200_OK)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario ja existe!")
