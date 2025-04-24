from base64 import b64encode

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from src.entities.places.image_crud import (
    get_location_images_zip_by_location,
    get_place_images_zip_by_place_name,
    get_image_description_by_place_name,
    get_region_images_zip_by_region_name
)
from src.helpers.exceptions import NotFound
from src.helpers.response import convert_keys_to_camel_case

router = APIRouter(prefix='/images', tags=['images'])


@router.get('/get-location-images/{location}')
async def get_images(location: str):
    location_images = await get_location_images_zip_by_location(location)
    if location_images is None:
        raise NotFound(message=f"Missing data for '{location}' location")

    return StreamingResponse(
        content=location_images,
        media_type="application/zip",
        headers={
            "Content-Disposition": 'attachment; filename="images.zip"',
        }
    )


@router.get("/get-place-images/{place_name}")
async def get_place_images_by_place_name(place_name: str):
    place_images = await get_place_images_zip_by_place_name(place_name)
    if place_images is None:
        raise NotFound(message=f"Missing data for '{place_name}' place")
    image_description = await get_image_description_by_place_name(place_name)

    encoded_description = b64encode(image_description.encode('utf-8')).decode('ascii')
    encoded_place_name = b64encode(place_name.encode('utf-8')).decode('ascii')

    headers = {
        "Content-Disposition": 'attachment; filename="images.zip"',
        "description": encoded_description,
        "place_name": encoded_place_name
    }
    headers = convert_keys_to_camel_case(headers)

    return StreamingResponse(
        content=place_images,
        media_type="application/zip",
        headers=headers
    )


@router.get("/get-region-images/{region-name}")
async def get_region_images_by_region_name(region_name: str):
    region_images = await get_region_images_zip_by_region_name(region_name)
    if region_images is None:
        raise NotFound(message=f"Missing data for '{region_images}' region")
    return StreamingResponse(
        content=region_images,
        media_type="application/zip",
        headers={
            "Content-Disposition": 'attachment; filename="images.zip"',
        }
    )
