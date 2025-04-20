from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.entities.user.crud import (
    get_user_by_email,
    create_user,
    create_user_verification_instance_by_email,
    get_user_verification_code_by_email,
    update_user_active_status,
    delete_user_verify_instance_by_verify_code
)
from src.entities.user.schema import UserSignUpSchema, UserVerificationSchema
from src.helpers.databases.postgres_db import get_async_session
from src.helpers.exceptions import ValidationError, NotFound, EmailExists
from src.helpers import messages
from src.helpers.response import TripNestArmeniaJSONResponse
from src.routers.auth.utils import get_password_hash
from src.helpers.mail import send_mail


router = APIRouter(prefix='/user-auth', tags=['user-auth'])

@router.post('/sign-up')
async def sign_up(user_data: UserSignUpSchema, db: AsyncSession = Depends(get_async_session)):
    user_instance = await get_user_by_email(user_data.email, db)
    if user_instance:
        raise EmailExists()
    password_hash = get_password_hash(user_data.password)
    new_user = await create_user(
        db,
        email=user_data.email,
        hashed_password=password_hash,
        first_name=user_data.first_name,
        last_name=user_data.last_name
    )
    if new_user:
        new_user_verification_instance = await create_user_verification_instance_by_email(
            new_user.email,
            db
        )  # in user_verification table
        await send_mail(
            subject='Welcome to TripNestArmenia',
            email_to=new_user.email,
            body={'verification_code': new_user_verification_instance.verification_code},
        )

    return TripNestArmeniaJSONResponse(status_code=status.HTTP_201_CREATED, message=messages.USER_CREATED)


@router.post('/verify-user')
async def verify_user(user: UserVerificationSchema, db: AsyncSession = Depends(get_async_session)):
    user_instance = await get_user_by_email(user.email, db)
    if not user_instance:
        raise ValidationError(status_code=status.HTTP_404_NOT_FOUND, message=messages.EMAIL_NOT_EXISTS)
    verify_code_in_db = await get_user_verification_code_by_email(user.email, db)
    if verify_code_in_db:
        if user.verified_code == verify_code_in_db:
            active_user = await update_user_active_status(email=user.email, db=db)
        else:
            raise ValidationError(message=messages.INVALID_VERIFICATION_CODE)
    else:
        raise NotFound(message=messages.EMAIL_NOT_EXISTS)  # Need to change this logic
    # await delete_user_verify_instance_by_verify_code(verify_code_in_db, db)  # update -> delete

    return TripNestArmeniaJSONResponse(
        message=messages.USER_VERIFIED,
        status_code=status.HTTP_201_CREATED
    )  # user in front end side after success must see success message
