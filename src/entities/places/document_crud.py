import asyncio
from typing import List

from motor.motor_asyncio import AsyncIOMotorGridOut, AsyncIOMotorGridFSBucket

from src.helpers.databases.mongo_db.mongo_db import mongo_async_client
from src.helpers.databases.mongo_db.mongo_file_manager import download_file_from_mongo_db


async def get_list_of_files_from_db_by_prefix(prefix: str) -> List[AsyncIOMotorGridOut]:
    file_manager = AsyncIOMotorGridFSBucket(mongo_async_client)
    cursor = file_manager.find({'filename': {'$regex': f'^{prefix}'}})
    files = [file async for file in cursor]

    tasks = [download_file_from_mongo_db(file) for file in files]
    results = await asyncio.gather(*tasks)

    return results
