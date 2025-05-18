from io import BytesIO

from fastapi import UploadFile

from src.helpers.databases.mongo_db.mongo_fs_file_manager import (
    create_files_zip_buffer,
    download_file_from_mongo_db,
    find_filenames_by_location,
    find_filenames_by_place_name,
    find_file_metadata_by_file_name,
    find_filenames_by_region_name,
    upload_file_in_db, PlaceMetadata,
    find_filenames_by_location_or_place_name
)


async def get_location_images_zip_by_location(location: str) -> BytesIO | None:
    location = location.lower()
    file_names = await find_filenames_by_location(location_pattern=location)
    if not file_names:
        return None
    return await create_files_zip_buffer(file_names, need_only_one_image=False)


async def get_location_image_zip_by_location(location: str) -> BytesIO | None:
    location = location.lower()
    file_names = await find_filenames_by_location(location_pattern=location)
    if not file_names:
        return None
    return await create_files_zip_buffer(file_names, need_only_one_image=True)


async def put_image_from_db_by_file_name(file_name: str) -> None:
    await download_file_from_mongo_db(file_name)


async def get_place_images_zip_by_place_name(place_name: str) -> BytesIO | None:
    place_name = place_name.lower()
    file_names = await find_filenames_by_place_name(place_name_pattern=place_name)
    if not file_names:
        return None
    return await create_files_zip_buffer(file_names, need_only_one_image=False)


async def get_image_description_by_place_name(place_name: str) -> str | None:
    place_name = place_name.lower()
    file_names = await find_filenames_by_place_name(place_name_pattern=place_name)
    if not file_names:
        return None

    for file_name in file_names:
        metadata = await find_file_metadata_by_file_name(file_name)
        if description := metadata.get('description'):
            return description
    return None


async def get_image_description_by_location(location: str) -> str | None:
    location = location.lower()
    file_names = await find_filenames_by_location(location_pattern=location)
    if not file_names:
        return None

    for file_name in file_names:
        metadata = await find_file_metadata_by_file_name(file_name)
        if description := metadata.get('description'):
            return description
    return None


async def get_region_images_zip_by_region_name(region_name: str) -> BytesIO | None:
    region_name = region_name.lower()
    file_names = await find_filenames_by_region_name(region_name)
    if not file_names:
        return None
    return await create_files_zip_buffer(file_names, need_only_one_image=False)


async def upload_image_with_metadata_in_db(file: UploadFile, file_name: str, metadata: PlaceMetadata) -> None:
    await upload_file_in_db(file=file, file_name=file_name, metadata=metadata)


async def get_location_in_map(location: str) -> tuple[float, float] | None:
    location = location.lower()
    file_names = await find_filenames_by_location(location_pattern=location)

    for file_name in file_names:
        metadata = await find_file_metadata_by_file_name(file_name)
        if metadata:
            if coordinates := metadata.get('location_in_map'):
                return coordinates

    return None


async def get_images_by_location_or_place_name(pattern_: str) -> BytesIO | None:
    pattern_ = pattern_.lower()
    file_names = await find_filenames_by_location_or_place_name(pattern_)
    if not file_names:
        return None
    return await create_files_zip_buffer(file_names, need_only_one_image=False)