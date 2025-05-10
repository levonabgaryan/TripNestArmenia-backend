from typing import TypedDict
import json

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import io
import zipfile
from pathlib import Path
from fastapi import UploadFile, HTTPException

from src.entities.accomplisher.db_models import Accomplisher
from src.helpers.databases.postgres_db import insert_data, delete_data


class AccomplisherData(TypedDict):
    email: str
    first_name: str
    last_name: str
    phone_number: str
    info: str


async def create_accomplisher_in_db(image: UploadFile, accomplisher_data: AccomplisherData, db: AsyncSession) -> Accomplisher | None:
    images_dir = Path(__file__).parent / "images"
    images_dir.mkdir(exist_ok=True, parents=True)
    file_path = images_dir / image.filename
    try:
        contents = await image.read()
        file_path.write_bytes(contents)
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to save image")

    instance = Accomplisher(
        email=accomplisher_data['email'],
        first_name=accomplisher_data['first_name'],
        last_name=accomplisher_data['last_name'],
        phone_number=accomplisher_data['phone_number'],
        info=accomplisher_data['info']
    )

    result = await insert_data(db, instance)
    return result


async def get_accomplishers_data_with_images(db: AsyncSession) -> io.BytesIO:
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

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, mode="w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr(
            "metadata.json",
            json.dumps(data, ensure_ascii=False, indent=2)
        )

        images_dir = Path(__file__).parent / "images"
        for img_path in images_dir.iterdir():
            if img_path.is_file():
                archive.write(img_path, arcname=f"images/{img_path.name}")

    buf.seek(0)
    return buf
