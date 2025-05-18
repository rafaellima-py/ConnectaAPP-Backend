from fastapi import APIRouter, Depends, HTTPException, status, Header
from fastapi.responses import JSONResponse
from scheema import *
from database import Database
from fastapi.security import OAuth2PasswordBearer
from security import *
from docs.info_docs import *
db = Database()
info_router = APIRouter()

@info_router.get("/get_user_info", responses=info_user_basic_response)
async def get_user_info(authorization: str = Header(..., description='Envie um Authorization: Bearer token') ,token: str = Depends(get_current_user)):
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
    
    user_info = await db.get_info_login(token)
    if not user_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    
    return JSONResponse(content={'sucess':True,'detail':'Usuario encontrado com sucesso', 'user_info': user_info},
                         status_code=status.HTTP_200_OK)