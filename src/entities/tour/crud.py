from datetime import datetime
from decimal import Decimal

from sqlalchemy import select, and_, extract, RowMapping
from sqlalchemy.ext.asyncio import AsyncSession

from src.entities.tour.db_models import Tour
from src.helpers.databases.postgres_db import insert_data, delete_data, update_data
from src.entities.tour.schema import TourStatus


async def create_tour(db: AsyncSession, **kwargs) -> Tour | None:
    instance = Tour(**kwargs)
    result = await insert_data(db, instance)
    return result


async def get_tours_by_status(db: AsyncSession, status_: TourStatus, need_id: bool = False) -> list[dict[
    str, str]] | None:
    if need_id:
        not_need_fields = {"createdAt", "updatedAt"}
    else:
        not_need_fields = {"id", "createdAt", "updatedAt"}

    tours = await (
        db.execute(
            select(Tour).filter(Tour.status == status_)
        )
    )
    tours = tours.scalars().all()
    tours = [tour.to_dict() for tour in tours]
    return [
        {k: v for k, v in tour.items() if k not in not_need_fields}
        for tour in tours
    ]


async def get_current_month_tours_from_db_by_status(
        db: AsyncSession,
        tour_status: TourStatus,
        need_id: bool = False
) -> list[dict[str, str]] | None:
    if need_id:
        not_need_fields = {"created_at", "updated_at"}
    else:
        not_need_fields = {"id", "created_at", "updated_at"}

    now = datetime.now()
    tours = await db.execute(
        select(Tour).filter(
            and_(
                Tour.status == tour_status,
                extract("year", Tour.created_at) == now.year,
                extract("month", Tour.created_at) == now.month
            )
        )
    )
    tours = tours.scalars().all()
    tours = [tour.to_dict() for tour in tours]
    return [
        {k: v for k, v in tour.items() if k not in not_need_fields}
        for tour in tours
    ]


async def update_tour_status_in_db(db: AsyncSession, tour_id: int, new_status: TourStatus) -> None | RowMapping:
    result = await update_data(
        db=db,
        table_=Tour,
        instance_id=tour_id,
        field_name='status',
        new_value=new_status
    )
    return result


async def update_amount_of_tour_by_id(db: AsyncSession, tour_id: int, amount: Decimal) -> RowMapping | None:
    result = await update_data(
        db=db,
        table_=Tour,
        instance_id=tour_id,
        field_name='amount_by_dram',
        new_value=amount
    )
    return result


async def get_tours_by_user_email(user_email: str, db: AsyncSession) -> list[dict[str, str]] | None:
    not_need_fields = {"created_at", "updated_at"}

    tours = await db.execute(
        select(Tour)
        .filter(Tour.user_email == user_email)
    )
    tours = tours.scalars().all()
    tours = [tour.to_dict() for tour in tours]
    return [
        {k: v for k, v in tour.items() if k not in not_need_fields}
        for tour in tours
    ]


async def add_comment_for_tour(tour_id: int, comment: str, db: AsyncSession) -> None | str:
    tour = await db.execute(
        select(Tour)
        .filter(Tour.id == tour_id)
    )

    tour = tour.scalar_one_or_none()
    if tour:
        tour.comment = comment
        db.add(tour)
        await db.commit()
        return str(tour.comment)

    return None


async def get_first_15_comments_of_all_tours(db: AsyncSession) -> list[dict[str, str]]:
    result = await db.execute(
        select(Tour.comment, Tour.destination, Tour.user_email)
        .where(Tour.comment.isnot(None))
        .order_by(Tour.id)
        .limit(15)
    )
    rows = result.mappings().all()
    return [
        {
            "comment": row["comment"],
            "destination": row["destination"],
            "user_email": row["user_email"]
        }
        for row in rows
    ]
