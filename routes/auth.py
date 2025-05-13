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
    else:
       username_db = user['username']
       password_db = user['password']
       password_is_valid = verify_hash(login.password, password_db)
       if username_db == login.email and password_is_valid:
           return JSONResponse(content={'user':login.email, 'password':login.password}, status_code=status.HTTP_200_OK)
    
@auth_router.post("/register")
async def register(register: UserRegister):
    user = await db.get_user(register.email)
    if not user:
        password = create_hash(register.password)
        register.password = password
        await db.register_user(register)
        return JSONResponse(content={'user':register.email, 'password':register.password}, status_code=status.HTTP_200_OK)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario ja existe")

@auth_router.post("/logout")
async def logout():
    return {"message": "Logout successfull"}
