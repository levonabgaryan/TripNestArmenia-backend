from datetime import datetime
from copy import deepcopy

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.helpers.databases.postgres_db import get_async_session
from src.entities.tour.schema import (
    BookTourModel,
    TourStatus,
    ChangeTourStatusModel,
    UpdateAmountTourModel
)
from src.entities.tour.crud import (
    create_tour,
    get_tours_by_status,
    get_current_month_tours_from_db_by_status,
    update_tour_status_in_db,
    update_amount_of_tour_by_id
)
from src.helpers.exceptions import NotFound
from src.helpers.response import TripNestArmeniaJSONResponse
from src.helpers import messages

router = APIRouter(prefix="/tours", tags=["tours"])


@router.post("/book-tour")
async def book_tour(tour: BookTourModel, db: AsyncSession = Depends(get_async_session)):
    data = tour.model_dump()

    created_tour = await create_tour(db=db, **data)

    if created_tour:
        return TripNestArmeniaJSONResponse(
            status_code=status.HTTP_201_CREATED,
            message=messages.TOUR_CREATED,
            content=tour.to_dict()
        )
    return None


@router.get("/get-tours/{status}")
async def get_tours_list_by_status(status_: TourStatus, db: AsyncSession = Depends(get_async_session)):
    tours_list = await get_tours_by_status(status_=status_, db=db)
    if not tours_list:
        raise NotFound(message='There are no tours by this status')
    return TripNestArmeniaJSONResponse(
        content={'tours_list': tours_list}
    )


@router.get("/get-current-month-tours/{tour_status}")
async def get_current_month_tours_by_status(tour_status: TourStatus, db: AsyncSession = Depends(get_async_session)):
    tours = await get_current_month_tours_from_db_by_status(db=db, need_id=True, tour_status=tour_status)
    if not tours:
        return NotFound(message='No tours in this month')
    return TripNestArmeniaJSONResponse(content={'tours_list': tours})


@router.patch("/update-tour-status")
async def update_tour_status(tour: ChangeTourStatusModel, db : AsyncSession = Depends(get_async_session)):
    new_status = tour.new_status
    result = await update_tour_status_in_db(
        db=db,
        tour_id=tour.tour_id,
        new_status=new_status
    )
    if result:
        return TripNestArmeniaJSONResponse(
            message=f"Status changed on {new_status} for tour with id {tour.tour_id}"
        )
    else:
        return None


@router.patch("/update-amount/")
async def update_amount(tour: UpdateAmountTourModel, db: AsyncSession = Depends(get_async_session)):
    result = await update_amount_of_tour_by_id(
        db=db,
        tour_id=tour.tour_id,
        amount=tour.amount
    )
    if result:
        return TripNestArmeniaJSONResponse(
            message=f"Amount changed to {tour.amount} DRAM for tour which have id {tour.tour_id}"
        )
    else:
        return None