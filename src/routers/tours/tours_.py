from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.helpers.databases.postgres_db import get_async_session
from src.entities.tour.schema import BookTourModel
from src.entities.tour.crud import create_tour
from src.helpers.response import TripNestArmeniaJSONResponse
from src.helpers import messages

router = APIRouter(prefix="/tours", tags=["tours"])


@router.post("/book-tour")
async def book_tour(tour: BookTourModel, db: AsyncSession = Depends(get_async_session)):
    data = {
        'user_email': tour.user_email,
        'user_phone_number': tour.user_phone_number,
        'need_hotel': tour.need_hotel,
        'destination': tour.destination,
        'booking_date': tour.booking_date,
        'description': tour.description,
        'number_of_people': tour.number_of_people
    }

    created_tour = await create_tour(db=db,**data)
    if created_tour:
        return TripNestArmeniaJSONResponse(
            status_code=status.HTTP_201_CREATED,
            message=messages.TOUR_CREATED,
            content=data
        )
    return None
