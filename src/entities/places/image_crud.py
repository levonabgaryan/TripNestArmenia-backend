from io import BytesIO


from src.helpers.databases.mongo_db.mongo_file_manager import (
    create_files_zip_buffer,
    download_file_from_mongo_db,
    find_filenames_by_location
)


async def get_images_zip_by_location(location: str) -> BytesIO | None:
    location = location.lower()
    file_names = await find_filenames_by_location(location_pattern=location)
    if not file_names:
        return None
    return await create_files_zip_buffer(file_names)


async def put_image_from_db_by_file_name(file_name: str) -> None:
    await download_file_from_mongo_db(file_name)
