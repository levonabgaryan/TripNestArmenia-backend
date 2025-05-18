from typing import TypedDict, Optional
import json
import asyncio

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import io
import zipfile
from pathlib import Path
from fastapi import UploadFile, HTTPException

from src.entities.accomplisher.db_models import Accomplisher
from src.helpers.databases.postgres_db.postgres_db import insert_data, delete_data


class AccomplisherData(TypedDict, total=False):
    email: str
    first_name: str
    last_name: str
    phone_number: str
    info: str
    image_file_name_in_mongo: Optional[str]


async def create_accomplisher_in_db(
    accomplisher_data: AccomplisherData,
    db: AsyncSession
) -> Accomplisher | None:

    instance = Accomplisher(
        email=accomplisher_data['email'],
        first_name=accomplisher_data['first_name'],
        last_name=accomplisher_data['last_name'],
        phone_number=accomplisher_data['phone_number'],
        info=accomplisher_data['info'],
        image_file_name_in_mongo=None
    )

    result = await insert_data(db, instance)
    return result


async def get_accomplishers_data(
    db: AsyncSession
) -> list:
    stmt = select(
        Accomplisher.email,
        Accomplisher.first_name,
        Accomplisher.last_name,
        Accomplisher.phone_number,
        Accomplisher.info,
    )
    result = await db.execute(stmt)
    rows = result.mappings().all()
    data = [dict(row) for row in rows]

    return data
