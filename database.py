from motor.motor_asyncio import AsyncIOMotorClient
from scheema import *
import datetime
import asyncio
import random
class DatabaseConfig:
    uri = 'mongodb://18.118.226.162:5003'
    database = 'connecta'
    collection_user = 'users'
    collection_service = 'service'
    collection_ticket = 'ticket'

class Database:
    def __init__(self):
        self.client = AsyncIOMotorClient(DatabaseConfig.uri)
        self.db = self.client[DatabaseConfig.database]
        self.user_collection = self.db[DatabaseConfig.collection_user]
        self.service_collection = self.db[DatabaseConfig.collection_service]
        self.ticket_collection = self.db[DatabaseConfig.collection_ticket]


    async def close(self):
        self.client.close()

    async def register_user(self, data: UserRegister):
        data_copy = data.dict()
        data_plus ={
            'tickets': [],
            'contracts_info': [],
            'projetos': [],
            'servicos': [],
            'status': 'ativo',
            'created_at': datetime.datetime.now(),
            'periodo': None,
        }
        data_copy.update(data_plus)
        await self.user_collection.insert_one(data_copy)


    async def login_user(self, data: UserLogin):
      user = data.username
      password = data.password
      print(user, password)
    
    async def get_user(self, username: str):
        user = await self.user_collection.find_one({'username': username})
        
        if not user:
            return None
        return user
    
    async def add_user_service(self, user: str, service: dict):
        user = await self.get_user(user)
        if not user:
            return None
        await self.user_collection.update_one({'username': user['username']}, {'$push': {'services': service}})
        return True
    
    async def add_user_projeto(self, user: str, projeto: list):
        user = await self.get_user(user)
        if not user:
            return None
        await self.user_collection.update_one({'username': user['username']}, {'$push': {'projetos': projeto}})
        return True
    
    async def desable_first_login(self, user: str):
        user = await self.get_user(user)
        if not user:
            return None
        await self.user_collection.update_one({'username': user['username']}, {'$set': {'primeiro_login': False}})
        return True
    async def add_contract_user(self, user: str, contract: dict):
        user = await self.get_user(user)
        if not user:
            return None
        await self.user_collection.update_one({'username': user['username']}, {'$push': {'contracts_info': contract}})
        return True

    async def get_all_tickets(self):
        tickets = await self.ticket_collection.find().to_list(length=None)
        return tickets
    
    async def get_all_services(self):
        services = await self.service_collection.find().to_list(length=None)
        return services

    async def get_all_users(self, type: str):
        users = await self.user_collection.find({'role': type}).to_list(length=None)
        return users

    async def create_ticket(
        self,
        username: str,
        nome: str,
        email: str,
        titulo: str,
        mensagem: str,
        status: str = "pendente",  # valor padrão
        data_criacao: datetime = None  # se não passar, usa agora
):
        idtic = 'tk'+str(random.randint(1000, 89999))
        ticket_data = {
            "user_info": {
                "id": idtic,
                "username": username,
                'nome': nome,
                "email": email
            },
            "ticket": {
                "titulo": titulo,
                "mensagem": mensagem,
                "status": status,
                "data_criacao":  datetime.datetime.utcnow()
            }
        }

        result = await self.ticket_collection.insert_one(ticket_data)
        # update em user tickets
        #await self.user_collection.update_one

        return True if result.acknowledged else False
    
    async def delete_ticket(self, id: str):
        result = await self.ticket_collection.delete_one({"user_info.id": id})
        return True if result.deleted_count > 0 else False
    
    async def create_service(self, nome: str, descricao: str, valor: float, periodo: str):
        service_data = {
            'id': 'sv' + str(random.randint(1000, 89999)),
            "nome": nome,
            "descricao": descricao,
            "valor": valor,
            "periodo": periodo,
            "status": 'pendente'
        }
        result = await self.service_collection.insert_one(service_data)
        return True if result.acknowledged else False
    
    
    async def delete_service(self, service_id: str):
        result = await self.service_collection.delete_one({"id": service_id})
        return result.deleted_count > 0

    async def add_service_in_user(self, user: str, service_id: str):
        result = await self.user_collection.update_one({'username': user}, {'$push': {'servicos': service_id}})
        return result.modified_count > 0
    async def remove_service_in_user(self, user: str, service_id: str):
        result = await self.user_collection.update_one({'username': user}, {'$pull': {'servicos': service_id}})
        return result.modified_count > 0