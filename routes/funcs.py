from fastapi import APIRouter, HTTPException, status, Header
from fastapi.responses import JSONResponse
from scheema import *
from database import Database
from fastapi.security import OAuth2PasswordBearer
from security import *

db = Database()
functions_router = APIRouter()

@functions_router.post('/desable_first_login', responses={'200': {'success':True,
                                                              'description': 'Usuário  aceitou o contrato'}})
async def desable_first_login(token: str = Depends(get_current_user)):
    print(token)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
    elif await db.desable_first_login(token):
        return JSONResponse(content={'sucess':True,'detail':'Usuário assinou o contrato'},
                         status_code=status.HTTP_200_OK)
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Usuário não encontrado')
    