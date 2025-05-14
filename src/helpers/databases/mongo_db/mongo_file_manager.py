import os
from io import BytesIO
from typing import IO, List, Tuple, Optional, TypedDict
import zipfile
import asyncio

import aiofiles
from fastapi import UploadFile
from motor.motor_asyncio import AsyncIOMotorGridFSBucket, AsyncIOMotorGridOut

from src.helpers.databases.mongo_db.mongo_db import mongo_async_client


class PlaceMetadata(TypedDict):
    place_name: str
    location: str
    region: str
    local_image_path: Optional[str]
    description: Optional[str]
    visited_tours_count_by_location: Optional[int]


# filename is a correct name of place e.g. Յոթ_վերք_եկեղեցի_1, location=Գյումրի, region=Շիրակ, place_name=Յոթ_վերք

async def is_file_exists_by_file_name(file_name: str) -> bool:
    query = {"filename": file_name}
    file_manager = AsyncIOMotorGridFSBucket(mongo_async_client)
    cursor = file_manager.find(query)

    async for _ in cursor:
        return True

    return False


async def download_file_from_mongo_db(file_name: str) -> AsyncIOMotorGridOut:
    file_manager = AsyncIOMotorGridFSBucket(mongo_async_client)
    stream = await file_manager.open_download_stream_by_name(filename=file_name)
    return stream


async def upload_file_in_db(file: UploadFile, file_name: str, metadata: PlaceMetadata) -> None:
    file_manager = AsyncIOMotorGridFSBucket(mongo_async_client)
    if not await is_file_exists_by_file_name(file_name):
        contents = await file.read()
        stream: IO[bytes] = BytesIO(contents)
        await file_manager.upload_from_stream(file_name, stream, metadata=metadata)


async def upload_local_file_in_db(local_file_path: str, metadata: PlaceMetadata) -> None:
    file_name = os.path.basename(local_file_path)
    idx = file_name.find('.')
    file_name = file_name[:idx]
    if not await is_file_exists_by_file_name(file_name):
        file_manager = AsyncIOMotorGridFSBucket(mongo_async_client)

        async with aiofiles.open(local_file_path, 'rb') as file:
            data = await file.read()

        stream: IO[bytes] = BytesIO(data)
        await file_manager.upload_from_stream(file_name, stream, metadata=metadata)


async def _fetch_file_data(
        file_name: str,
        only_description_from_metadata: bool = False
) -> Tuple[PlaceMetadata, str, bytes] | str | None:
    metadata = await find_file_metadata_by_file_name(file_name)
    try:
        stream = await download_file_from_mongo_db(file_name)
    except Exception:
        raise

    try:
        data = await stream.read()
    except Exception:
        raise

    if only_description_from_metadata:
        return metadata.get('description')

    return metadata, file_name, data


async def create_files_zip_buffer(file_names: List[str], need_only_one_image: bool) -> BytesIO:
    tasks = [_fetch_file_data(name) for name in file_names]
    results = await asyncio.gather(*tasks)

    buf = BytesIO()

    with zipfile.ZipFile(buf, mode="w") as zf:
        if need_only_one_image:
            for metadata, _, image in results:
                image_name = metadata.get('place_name') or "unknown"
                zf.writestr(image_name, image)
        else:
            for _, file_name, image in results:
                zf.writestr(file_name, image)

    buf.seek(0)
    return buf


async def find_filenames_by_location(location_pattern: str) -> List[str]:
    files_collection = mongo_async_client["fs"]["files"]
    query = {
        "metadata.location": {
            "$regex": f"^{location_pattern}",
            "$options": "i"  # регистронезависимый поиск
        }
    }

    cursor = files_collection.find(query)

    filenames = []
    async for file in cursor:
        filenames.append(file["filename"])

    return filenames


async def find_filenames_by_place_name(place_name_pattern: str) -> List[str]:
    files_collection = mongo_async_client["fs"]["files"]
    query = {
        "metadata.place_name": {
            "$regex": f"^{place_name_pattern}",
            "$options": "i"  # регистронезависимый поиск
        }
    }

    cursor = files_collection.find(query)

    filenames = []
    async for file in cursor:
        filenames.append(file["filename"])

    return filenames


async def find_filenames_by_region_name(region_name_pattern: str) -> List[str]:
    files_collection = mongo_async_client["fs"]["files"]
    query = {
        "metadata.region": {
            "$regex": f"{region_name_pattern}",
            "$options": "i"
        }
    }

    cursor = files_collection.find(query)

    filenames = []
    async for file in cursor:
        filenames.append(file["filename"])
    return filenames


async def find_file_metadata_by_file_name(file_name: str) -> PlaceMetadata | None:
    files_collection = mongo_async_client["fs"]["files"]
    file_metadata = await files_collection.find_one({"filename": file_name})
    if file_metadata and "metadata" in file_metadata:
        metadata = file_metadata["metadata"]
        return metadata
    return None
