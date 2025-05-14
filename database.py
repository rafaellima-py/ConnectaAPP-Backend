from motor.motor_asyncio import AsyncIOMotorClient
from scheema import *
import datetime
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
            'services': [],
            'status': 'ativo',
            'created_at': datetime.datetime.now(),
        }
        data_copy.update(data_plus)
        await self.user_collection.insert_one(data_copy)

    async def get_info_login(self, user: str):
        user = await self.get_user(user)
        if not user:
            return None 
      
        contrato = user['contracts_info']
        if not contrato:  
            role = user['role']
            nome = user['name']
            sobrenome = user['last_name']
            cpf = user['cpf']
            email = user['email']
            cep = user['cep']
            rg = user['rg']
            rua = user['rua']
            numero = user['numero']
            bairro = user['bairro']
            cidade = user['cidade']
            estado = user['estado']
            telefone = user['phone']
            cargo = user['cargo']
            contratos = user['contracts_info']
            primeiro_login = user['primeiro_login']
            return {
                "contratos": contratos,
                'role': role,
                'nome': nome,
                'lastName': sobrenome,
                'cpf': cpf,
                'phone': telefone,
                'cargo': cargo,
                'email': email,
                'cep': cep,
                'rg': rg,
                'rua': rua,
                'numero': numero,
                'bairro': bairro,
                'cidade': cidade,
                'estado': estado,
                "is_first_login": primeiro_login
            }
        return None


    async def login_user(self, data: UserLogin):
      user = data.email
      password = data.password
      print(user, password)
    
    async def get_user(self, user: str):
        return await self.user_collection.find_one({'email': user})