from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.helpers.databases.postgres_db.postgres_db import get_async_session
from src.entities.tour.schema import (
    BookTourModel,
    TourStatus,
    ChangeTourStatusModel,
    UpdateAmountTourModel,
    UserCommentModel,
    UpdateTourAssessment
)
from src.entities.tour.crud import (
    create_tour,
    get_tours_by_status,
    get_current_month_tours_from_db_by_status,
    update_tour_status_in_db,
    update_amount_of_tour_by_id,
    get_tours_by_user_email,
    add_comment_for_tour,
    get_first_15_comments_of_all_tours,
    update_tour_assessment_in_db,
    get_tour_assessment_from_db
)
from src.helpers.exceptions import NotFound, AssessmentError
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
async def get_current_month_tours_by_status(
        tour_status: TourStatus,
        db: AsyncSession = Depends(get_async_session)
):
    tours = await get_current_month_tours_from_db_by_status(
        db=db, need_id=True, tour_status=tour_status
    )
    return TripNestArmeniaJSONResponse(content={"tours_list": tours or []})


@router.patch("/update-tour-status")
async def update_tour_status(tour: ChangeTourStatusModel, db: AsyncSession = Depends(get_async_session)):
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


@router.patch("/update-amount")
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


@router.get("/get-tours-by-user-email{user_email}")
async def get_tours_list_for_user(user_email: str, db: AsyncSession = Depends(get_async_session)):
    list_of_tours = await get_tours_by_user_email(
        db=db,
        user_email=user_email
    )

    return TripNestArmeniaJSONResponse(
        content={'tours_list': list_of_tours}
    )


@router.patch('/leave-comment')
async def leave_a_comment(comment: UserCommentModel, db: AsyncSession = Depends(get_async_session)):
    comment = await add_comment_for_tour(
        tour_id=comment.tour_id,
        comment=comment.comment,
        db=db
    )

    if comment:
        return TripNestArmeniaJSONResponse(
            content={'added_comment': comment}
        )
    else:
        return NotFound()


@router.get('/get-comments')
async def get_tours_comment(db: AsyncSession = Depends(get_async_session)):
    comments = await get_first_15_comments_of_all_tours(db)
    return TripNestArmeniaJSONResponse(content={'comments': comments})


@router.patch('/update-tour-assessment')
async def update_tour_assessment(data: UpdateTourAssessment, db: AsyncSession=Depends(get_async_session)):
    try:
        await update_tour_assessment_in_db(
            db=db,
            tour_id=data.tour_id,
            new_assessment=data.new_assessment
        )
    except AssessmentError as e:
        return TripNestArmeniaJSONResponse(status_code=status.HTTP_400_BAD_REQUEST, message=str(e))
    else:
        return TripNestArmeniaJSONResponse(content={'assessment': data.new_assessment})


@router.get('/get-tour-assessment')
async def get_tour_assessment(tour_id: int, db: AsyncSession = Depends(get_async_session)):
    tour_assessment = await get_tour_assessment_from_db(
        tour_id=tour_id,
        db=db
    )
    if not tour_assessment:
        raise NotFound()
    return TripNestArmeniaJSONResponse(content={'tour_assessment': tour_assessment})
