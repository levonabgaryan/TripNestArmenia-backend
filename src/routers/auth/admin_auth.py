from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.entities.admin.schema import AdminSignInSchema, AdminCreateSchema
from src.helpers.databases.postgres_db import get_async_session
from src.entities.admin.crud import get_admin_by_email, create_admin_in_db
from src.helpers.exceptions import ValidationError, TripNestArmeniaException
from src.helpers.response import TripNestArmeniaJSONResponse
from src.routers.auth.utils import verify_password, get_password_hash

router = APIRouter(prefix='/admin', tags=['admin'])


@router.post("/create-admin")
async def create_admin(admin: AdminCreateSchema, db: AsyncSession = Depends(get_async_session)):
    password_hash = get_password_hash(admin.password)

    admin_instance = await create_admin_in_db(
        db=db,
        email=admin.email,
        hashed_password=password_hash,
        first_name=admin.first_name,
        last_name=admin.last_name
    )

    if admin_instance is not None:
        return TripNestArmeniaJSONResponse(
            message='Admin creates successfully'
        )
    else:
        return None


@router.post("/sign-in")
async def sign_in_admin(admin: AdminSignInSchema, db: AsyncSession = Depends(get_async_session)):
    admin_instance = await get_admin_by_email(email=admin.email, db=db)
    if admin_instance is None:
        raise ValidationError(message='Incorrect email')

    password_hash = get_password_hash(admin.password)
    if verify_password(admin_instance, password_hash):
        return TripNestArmeniaJSONResponse(
            message='Admin logins successfully'
        )
    else:
        raise ValidationError(message='Incorrect password')
