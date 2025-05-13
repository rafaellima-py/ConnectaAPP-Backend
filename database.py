from motor.motor_asyncio import AsyncIOMotorClient
from scheema import *
import datetime
class DatabaseConfig:
    uri = 'mongodb://18.118.226.162:5003'
    database = 'connecta'
    collection_user = 'user'
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

    async def login_user(self, data: UserLogin):
      user = data.email
      password = data.password
      print(user, password)