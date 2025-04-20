from io import BytesIO

from src.helpers.databases.mongo_db.mongo_file_manager import (
    find_filenames_by_prefix,
    create_files_zip_buffer,
    download_file_from_mongo_db
)


async def get_images_by_prefix(prefix: str) -> BytesIO:
    prefix = prefix.lower()
    file_names = await find_filenames_by_prefix(prefix)
    return await create_files_zip_buffer(file_names)


async def put_image_from_db_by_file_name(file_name: str) -> None:
    await download_file_from_mongo_db(file_name)
