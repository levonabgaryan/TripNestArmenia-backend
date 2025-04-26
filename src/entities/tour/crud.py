from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.entities.tour.db_models import Tour
from src.helpers.databases.postgres_db import insert_data, delete_data


async def create_tour(db: AsyncSession, **kwargs) -> Tour | None:
    instance = Tour(**kwargs)
    result = await insert_data(db, instance)
    return result
