from motor.motor_asyncio import AsyncIOMotorClient
from scheema import *

class DatabaseConfig:
    uri = 'mongodb://18.118.226.162:5003/'
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

    async def register_user(self):
        pass

    async def login_user(self, data: UserLogin):
        user = await self.user_collection.find_one({"email": data.email, "password": data.password})
        if user:
            pass