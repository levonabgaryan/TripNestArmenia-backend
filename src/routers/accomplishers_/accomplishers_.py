from fastapi import APIRouter, Depends, UploadFile, File, status, Form
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.entities.accomplisher.crud import get_accomplishers_data_with_images_and_metadata, create_accomplisher_in_db, \
    AccomplisherData
from src.helpers.databases.postgres_db.postgres_db import get_async_session
from src.helpers.response import TripNestArmeniaJSONResponse

router = APIRouter(prefix='/accomplishers', tags=['accomplishers'])


@router.get("/get-all-data")
async def download_accomplishers_bundle(db: AsyncSession = Depends(get_async_session)):
    bundle = await get_accomplishers_data_with_images_and_metadata(db)
    return StreamingResponse(
        bundle,
        media_type="application/zip",
        headers={
            "Content-Disposition": 'attachment; filename="accomplishers_bundle.zip"'
        }
    )


@router.post('/create')
async def create_accomplisher(
        email: str = Form(...),
        first_name: str = Form(...),
        last_name: str = Form(...),
        phone_number: str = Form(...),
        info: str = Form(...),
        image: UploadFile = File(...),
        db: AsyncSession = Depends(get_async_session)
):
    accomplisher_data: AccomplisherData = {
        'email': email,
        'first_name': first_name,
        'last_name': last_name,
        'phone_number': phone_number,
        'info': info
    }
    data = await create_accomplisher_in_db(
        image=image,
        accomplisher_data=accomplisher_data,
        db=db
    )

    return TripNestArmeniaJSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={'created_accomplisher_email': data.email}
    )
