import zipfile
import io
import json

from fastapi import APIRouter, Depends, UploadFile, File, status, Form
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.entities.accomplisher.crud import (
    get_accomplishers_data,
    create_accomplisher_in_db,
    AccomplisherData
)
from src.helpers.databases.mongo_db.mongo_accomplishers_images_manager import bucket
from src.helpers.databases.mongo_db.mongo_accomplishers_images_manager import save_accomplisher_image_to_mongo
from src.helpers.databases.postgres_db.postgres_db import get_async_session
from src.helpers.response import TripNestArmeniaJSONResponse, convert_keys_to_camel_case

router = APIRouter(prefix='/accomplishers', tags=['accomplishers'])


@router.get("/get-all-data")
async def download_accomplishers_bundle(db: AsyncSession = Depends(get_async_session)):
    accomplishers = await get_accomplishers_data(db)
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.writestr("data.json", json.dumps(accomplishers, indent=2))

        for person in accomplishers:
            email = person["email"]
            try:
                grid_out = await bucket.open_download_stream_by_name(email)
                image_bytes = await grid_out.read()
                ext = grid_out.filename.split('.')[-1] if '.' in grid_out.filename else "jpg"
                zip_file.writestr(f"{email}.{ext}", image_bytes)
            except Exception:
                continue

    zip_buffer.seek(0)

    zip_buffer.seek(0)

    headers = convert_keys_to_camel_case(
        {"Content-Disposition": "attachment; filename=accomplishers_bundle.zip"}
    )
    return StreamingResponse(
        zip_buffer,
        media_type="application/zip",
        headers=headers
    )


@router.post("/create")
async def create_accomplisher(
    email: str = Form(...),
    first_name: str = Form(...),
    last_name: str = Form(...),
    phone_number: str = Form(...),
    info: str = Form(...),
    image: UploadFile = File(...),
    db: AsyncSession = Depends(get_async_session),
):
    image_file_name = email  # simple and unique

    await save_accomplisher_image_to_mongo(
        file=image,
        filename=image_file_name,
    )

    accomplisher_data: AccomplisherData = {
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "phone_number": phone_number,
        "info": info,
    }

    result = await create_accomplisher_in_db(accomplisher_data, db)

    return TripNestArmeniaJSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"created_accomplisher_email": result.email},
    )
