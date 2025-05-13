from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from scheema import *
from database import Database
from security import create_hash, verify_hash
db = Database()
auth_router = APIRouter()

@auth_router.post("/login")
async def login(login: UserLogin):
    await db.login_user(login)
    return JSONResponse(content={'user':login.email, 'password':login.password}, status_code=status.HTTP_200_OK)

@auth_router.post("/register")
async def register(register: UserRegister):
    password = create_hash(register.password)
    register.password = password
    await db.register_user(register)
    return JSONResponse(content={'user':register.email, 'password':register.password}, status_code=status.HTTP_200_OK)
@auth_router.post("/logout")
async def logout():
    return {"message": "Logout successfull"}
