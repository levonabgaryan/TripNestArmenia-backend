from fastapi import APIRouter
from src.entities.places.schema import PlaceDataModel


router = APIRouter(prefix='/place-data', tags=['place-data'])

@router.get('/get-plac-data')
async def get_place_data(data: PlaceDataModel):
    ...