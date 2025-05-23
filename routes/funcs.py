from fastapi import APIRouter, HTTPException, status, Header, UploadFile, File
from fastapi.responses import JSONResponse
from scheema import *
from database import Database
from fastapi.security import OAuth2PasswordBearer
from security import *
import base64

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


@functions_router.post('/get_all_tickets')
async def get_all_tickets(token: str = Depends(token_is_admin)):
    tickets = await db.get_all_tickets()
    for item in tickets:
        item['_id'] = str(item['_id'])
    return tickets

@functions_router.post('/get_all_services')
async def get_all_services(token: str = Depends(token_is_admin)):
    services = await db.get_all_services()
    for item in services:
        item['_id'] = str(item['_id'])
    return services

@functions_router.post('/get_all_users')
async def get_all_users(type: UserRole, token: str =  Depends(token_is_admin)):
    users = await db.get_all_users(type)

    for user in users:
        user['_id'] = str(user['_id'])
        
        for contract in user.get("contracts_info", []):
            if "contrato" in contract and isinstance(contract["contrato"], bytes):
                contract["contrato"] = base64.b64encode(contract["contrato"]).decode('utf-8')
            if "assinatura" in contract and isinstance(contract["assinatura"], bytes):
                contract["assinatura"] = base64.b64encode(contract["assinatura"]).decode('utf-8')

    return users

    return users
@functions_router.post('/create_ticket')
async def create_ticket(ticket: Ticket, token: str = Depends(get_current_user)):
    username = ticket.username
    nome = ticket.nome
    email = ticket.email
    titulo = ticket.titulo
    mensagem = ticket.mensagem
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
    elif await db.create_ticket(username=username, nome=nome,
                                email=email, titulo=titulo, mensagem=mensagem):
        return JSONResponse(content={'sucess':True,'detail':'Ticket criado com sucesso'},
                         status_code=status.HTTP_200_OK)
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Usuário não encontrado')

@functions_router.delete('/delete_ticket')
async def delete_ticket(id: str, token: str = Depends(get_current_user)):
    deleted = await db.delete_ticket(id)
    if deleted:
        return JSONResponse(content={
            'success': True,
            'detail': 'Ticket excluído com sucesso'
        }, status_code=status.HTTP_200_OK)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Ticket não encontrado')



@functions_router.post('/create_service')
async def create_service(service: Service, token: str = Depends(get_current_user)):
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
    elif await db.create_service(nome=service.nome, descricao=service.descricao, valor=service.valor, periodo=service.periodo):
        return JSONResponse(content={'sucess':True,'detail':'Serviço criado com sucesso'},
                         status_code=status.HTTP_200_OK)
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Usuário não encontrado')

@functions_router.delete('/delete_service')
async def delete_service(service_id: str, token: str = Depends(get_current_user)):
    deleted = await db.delete_service(service_id)
    
    if deleted:
        return JSONResponse(content={
            'success': True,
            'detail': 'Serviço excluído com sucesso'
        }, status_code=status.HTTP_200_OK)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Serviço não encontrado')

@functions_router.post('/add_service_in_user')
async def add_service_in_user(username: str, service_id: str):
    if await db.add_service_in_user(username, service_id):
        return JSONResponse(content={'sucess':True,'detail':'Serviço adicionado com sucesso'},
                         status_code=status.HTTP_200_OK)
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Falha ao atribuir serviço ao usuario')

@functions_router.post('/remove_service_in_user')
async def remove_service_in_user(username: str, service_id: str):
    if await db.remove_service_in_user(username, service_id):
        return JSONResponse(content={'sucess':True,'detail':'Serviço removido com sucesso'},
                         status_code=status.HTTP_200_OK)
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Falha ao remover serviço do usuario')
