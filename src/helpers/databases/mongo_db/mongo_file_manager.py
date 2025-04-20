import os
from io import BytesIO
from typing import IO, List, Tuple
import zipfile
import asyncio

import aiofiles
from fastapi import UploadFile, HTTPException
from motor.motor_asyncio import AsyncIOMotorGridFSBucket, AsyncIOMotorGridOut

from src.helpers.databases.mongo_db.mongo_db import mongo_async_client


async def is_file_exists(file_name: str) -> bool:
    file_manager = AsyncIOMotorGridFSBucket(mongo_async_client)
    cursor = file_manager.find({"filename": file_name})

    async for _ in cursor:
        return True

    return False


async def download_file_from_mongo_db(file_name: str) -> AsyncIOMotorGridOut:
    file_manager = AsyncIOMotorGridFSBucket(mongo_async_client)
    stream = await file_manager.open_download_stream_by_name(filename=file_name)
    return stream


async def upload_image_in_db(file: UploadFile, file_name: str) -> None:
    file_manager = AsyncIOMotorGridFSBucket(mongo_async_client)
    contents = await file.read()
    stream: IO[bytes] = BytesIO(contents)
    await file_manager.upload_from_stream(file_name, stream)


async def upload_local_image_in_db(local_file_path: str) -> None:
    file_name = os.path.basename(local_file_path)
    if not await is_file_exists(file_name):
        file_manager = AsyncIOMotorGridFSBucket(mongo_async_client)

        async with aiofiles.open(local_file_path, 'rb') as file:
            data = await file.read()

        stream: IO[bytes] = BytesIO(data)
        await file_manager.upload_from_stream(file_name, stream)


async def _fetch_file_data(name: str) -> Tuple[str, bytes]:
    try:
        stream = await download_file_from_mongo_db(name)
    except Exception:
        raise HTTPException(status_code=404, detail=f"File {name} not found in database")

    try:
        data = await stream.read()
    except Exception:
        raise HTTPException(status_code=500, detail=f"Error reading file {name}")

    return name, data



async def create_images_zip_buffer(file_names: List[str]) -> BytesIO:
    """
    Собирает переданные file_names из GridFS в один ZIP-архив
    и возвращает BytesIO с этим архивом.
    """
    # 1) Запускаем загрузку всех файлов параллельно
    tasks = [_fetch_file_data(name) for name in file_names]
    results = await asyncio.gather(*tasks)

    # 2) Собираем ZIP
    buf = BytesIO()
    with zipfile.ZipFile(buf, mode="w") as zf:
        for name, data in results:
            zf.writestr(name, data)

    buf.seek(0)
    return buf
