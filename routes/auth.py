from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from scheema import *
from database import Database
from fastapi.security import OAuth2PasswordBearer
from security import *

db = Database()
auth_router = APIRouter()


@auth_router.post("/login")
async def login(login: UserLogin):
    user = await db.get_user(login.username)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    
    if user["username"] == login.username and verify_hash(login.password, user["password"]):
        user_info = await db.get_info_login(user["username"])

        if not user_info:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Falha ao obter informações do usuário")
        
        token = create_token(data={"sub": user["email"], 'role': user["role"]})
        
        return JSONResponse(content={'sucess':True,'detail':'Login realizado',
                                     'token': token, 'token_type': 'Bearer'},
        status_code=status.HTTP_200_OK)
        
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário ou senha inválidos")

@auth_router.post("/register")
async def register(register: UserRegister, token: str = Depends(token_is_admin)):
    user = await db.get_user(register.email)
    if not user:
        
        password = create_hash(register.password)
        register.password = password
        await db.register_user(register)

        return JSONResponse(content={'sucess':True,'detail':'Usuario cadastrado com sucesso'},	
        status_code=status.HTTP_200_OK)
    
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario ja existe!")
'''
@auth_router.post("/user")
async def get_user(token: str = Depends(get_current_user)):
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
    return JSONResponse(content={'message':'ok'}, status_code=status.HTTP_200_OK)

@auth_router.post("/admin")
async def get_admin(token: str = Depends(token_is_admin)):
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
    return JSONResponse(content={'message':'ok'}, status_code=status.HTTP_200_OK)
'''