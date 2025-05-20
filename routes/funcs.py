from fastapi import APIRouter, HTTPException, status, Header, UploadFile, File
from fastapi.responses import JSONResponse
from scheema import *
from database import Database
from fastapi.security import OAuth2PasswordBearer
from security import *

db = Database()
functions_router = APIRouter()

@functions_router.post('/desable_first_login', responses={'200': {'success':True,
                                                              'description': 'Usuário  aceitou o contrato'},
                                                              '404': {'success':False, 'description': 'Usuário não encontrado'},
                                                                      }
                                                 
                                                              )
async def desable_first_login(token: str = Depends(get_current_user)):
    print(token)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
    elif await db.desable_first_login(token):
        return JSONResponse(content={'sucess':True,'detail':'Usuário assinou o contrato'},
                         status_code=status.HTTP_200_OK)
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Usuário não encontrado')
@functions_router.post('/send_contract')
async def accept_contract(
    token: str = Depends(get_current_user),
    files: list[UploadFile] = File(...)
):
    contrato = None
    assinatura = None

    for file in files:
        content = await file.read()
        
        if file.filename.endswith('.pdf'):
            contrato = content
        elif file.filename.endswith('.png'):
            assinatura = content

    if not contrato or not assinatura:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Envie um contrato (.pdf) e uma assinatura (.png)")

    # Supondo que db.add_contract_user seja async:
    await db.add_contract_user(token, contract={
        'contrato': contrato,
        'assinatura': assinatura
    })

    return {"success": True, "detail": "Contrato enviado com sucesso"}
@functions_router('/get_all_tickets')
async def get_all_tickets(token: str = Depends(token_is_admin)):
    tickets = await db.get_all_tickets()
    return tickets
