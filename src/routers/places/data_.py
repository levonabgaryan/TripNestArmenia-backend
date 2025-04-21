from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from src.entities.places.image_crud import get_images_zip_by_location
from src.helpers.exceptions import NotFound

router = APIRouter(prefix='/place-data', tags=['place-data'])


@router.get('/get-place-images/{place_name}')
async def get_images(place_name: str):
    place_images = await get_images_zip_by_location(place_name)

    if place_images is None:
        raise NotFound(message=f"Missing data for '{place_name}' place")

    return StreamingResponse(
        content=place_images,
        media_type="application/zip",
        headers={
            "Content-Disposition": 'attachment; filename="images.zip"',
        }
    )
