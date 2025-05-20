from database import Database
import asyncio

print(__path__)
class TicketDatabase(Database):
    def __init__(self):
        super().__init__()


    async def show_all_tickets(self):
        tickets = await self.ticket_collection.find()
        return tickets


print(asyncio.run(TicketDatabase().show_all_tickets()))