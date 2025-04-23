from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from src.entities.places.image_crud import get_images_zip_by_location, get_place_images_zip_by_place_name
from src.helpers.exceptions import NotFound

router = APIRouter(prefix='/images', tags=['images'])


@router.get('/get-location-images/{location}')
async def get_images(location: str):
    location_images = await get_images_zip_by_location(location)
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

    return StreamingResponse(
        content=place_images,
        media_type="application/zip",
        headers={
            "Content-Disposition": 'attachment; filename="images.zip"',
        }
    )