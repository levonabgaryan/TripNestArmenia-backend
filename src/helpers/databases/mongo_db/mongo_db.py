import os
import asyncio

from dotenv import find_dotenv, load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv(find_dotenv())

MONGO_USERNAME = os.getenv("MONGO_INITDB_ROOT_USERNAME")
MONGO_PASSWORD = os.getenv("MONGO_INITDB_ROOT_PASSWORD")
MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_PORT = os.getenv("MONGO_PORT")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

MONGO_URI = f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}"

client = AsyncIOMotorClient(MONGO_URI)
mongo_async_client = client[MONGO_DB_NAME]


async def set_log_level():
    await mongo_async_client.admin.command({"setParameter": 1, "logLevel": 1})
    result = await mongo_async_client.admin.command("getParameter", "logLevel")
    print("Current log level:", result.get("logLevel"))


if __name__ == "__main__":
    asyncio.run(set_log_level())
