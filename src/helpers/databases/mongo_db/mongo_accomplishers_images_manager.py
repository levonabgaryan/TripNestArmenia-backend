import io
from motor.motor_asyncio import AsyncIOMotorGridFSBucket, AsyncIOMotorGridOut
from fastapi import UploadFile, HTTPException


from src.helpers.databases.mongo_db.mongo_db import mongo_async_client
from src.helpers.exceptions import FileNameAlreadyExists



bucket = AsyncIOMotorGridFSBucket(mongo_async_client, bucket_name="accomplishers")


async def save_accomplisher_image_to_mongo(
    file: UploadFile,
    filename: str,
) -> None:
    existing = bucket.find({"filename": filename})
    async for _ in existing:
        raise FileNameAlreadyExists(filename)

    contents = await file.read()
    stream: io[bytes] = io.BytesIO(contents)

    await bucket.upload_from_stream(
        filename,
        stream,
    )


async def get_accomplisher_image_by_filename(filename: str) -> AsyncIOMotorGridOut:
    try:
        file = await bucket.open_download_stream_by_name(filename)
        return file
    except Exception:
        raise HTTPException(status_code=404, detail=f"File '{filename}' not found")