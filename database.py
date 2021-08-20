from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine

from setting import setting


client = AsyncIOMotorClient(
    setting.DATABASE_URL,
    uuidRepresentation="standard"
)

db = client[setting.DATABASE_DB]
engine = AIOEngine(motor_client=client, database=setting.DATABASE_DB)
