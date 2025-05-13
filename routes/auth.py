from fastapi import APIRouter, Depends, HTTPException, status
from scheema import *
auth_router = APIRouter()

@auth_router.post("/login")
async def login(login: UserLogin):
    return {"message": "Login successful", "email": login.email, 'password': login.password}

@auth_router.post("/register")
async def register(register: UserRegister):
    return {"message": "Register successful", "email": register.email, 'password': register.password}

@auth_router.post("/logout")
async def logout():
    return {"message": "Logout successfull"}
