from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from scheema import *
auth_router = APIRouter()

@auth_router.post("/login")
async def login(login: UserLogin):
    return JSONResponse(content={'message':'Ok'}, status_code=status.HTTP_200_OK)
@auth_router.post("/register")
async def register(register: UserRegister):
    return {"message": "Register successful", "email": register.email, 'password': register.password}

@auth_router.post("/logout")
async def logout():
    return {"message": "Logout successfull"}
