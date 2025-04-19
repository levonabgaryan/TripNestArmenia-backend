import os
from io import BytesIO
from typing import IO

import aiofiles
from fastapi import UploadFile
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorGridFSBucket, AsyncIOMotorGridOut
from src.helpers.databases.mongo_db.mongo_db import mongo_async_client


async def is_image_exists(image_id):
    collection = mongo_async_client["your_database"]["your_collection"]
    result = await collection.find_one({"image_id": image_id})
    return result is not None


async def download_image_of_db(image_id: str) -> AsyncIOMotorGridOut:
    file_manager = AsyncIOMotorGridFSBucket(mongo_async_client)
    # Не используем ObjectId, просто ищем по имени файла
    stream = await file_manager.open_download_stream_by_name(image_id)
    return stream


async def upload_image_in_db(image: UploadFile, image_name: str) -> str:
    file_manager = AsyncIOMotorGridFSBucket(mongo_async_client)
    contents = await image.read()
    stream: IO[bytes] = BytesIO(contents)
    file_id = await file_manager.upload_from_stream(image_name, stream)
    return str(file_id)


async def upload_local_image_in_db(local_image_path: str) -> str | None:
    image_id = os.path.basename(local_image_path)
    if not await is_image_exists(image_id):
        file_manager = AsyncIOMotorGridFSBucket(mongo_async_client)

        # Использование aiofiles для асинхронного открытия файла
        async with aiofiles.open(local_image_path, 'rb') as file:
            data = await file.read()

        stream: IO[bytes] = BytesIO(data)
        file_id = await file_manager.upload_from_stream(image_id, stream)
        return str(file_id)
