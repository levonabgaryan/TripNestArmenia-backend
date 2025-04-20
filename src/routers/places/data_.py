from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from src.entities.places.place_document_crud import get_document_about_place_by_name
from src.entities.places.image_crud import get_images_by_prefix
from src.helpers.exceptions import NotFound

router = APIRouter(prefix='/place-data', tags=['place-data'])


@router.get('/get-place-description-with-images/{place}')
async def get_description_data(place_name: str):
    place_data = await get_document_about_place_by_name(place_name)
    place_images = await get_images_by_prefix(place_name)
    if not place_data:
        raise NotFound(message=f"Missing data for '{place_name}' place")

    return StreamingResponse(
        place_images,
        media_type="application/zip",
        headers={"Content-Disposition": 'attachment; filename="images.zip"',
                 "description": place_data.get('description')}
    )
