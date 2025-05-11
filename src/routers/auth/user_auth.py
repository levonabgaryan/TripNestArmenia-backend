from fastapi import APIRouter, Depends, status, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.entities.user.crud import (
    get_user_by_email,
    create_user,
    create_user_verification_instance_by_email,
    get_user_verification_code_by_email,
    update_user_active_status,
    delete_user_verify_instance_by_verify_code
)
from src.entities.user.schema import (
    UserSignUpSchema,
    UserVerificationSchema,
    UserSignInSchema
)

from src.helpers import messages
from src.routers.auth.utils import create_access_token, decode_access_token
from src.helpers.databases.postgres_db.postgres_db import get_async_session
from src.helpers.exceptions import ValidationError, NotFound, EmailExists
from src.helpers.response import TripNestArmeniaJSONResponse
from src.routers.auth.utils import get_password_hash, verify_password, JWTPayload
from src.helpers.mail import send_mail

router = APIRouter(prefix='/user', tags=['user'])


@router.post('/sign-up')
async def sign_up(user_data: UserSignUpSchema, db: AsyncSession = Depends(get_async_session)):
    user_instance = await get_user_by_email(user_data.email, db)
    if user_instance:
        raise EmailExists(email=user_data.email)
    password_hash = get_password_hash(user_data.password)
    payload: JWTPayload = {
        'email': user_data.email,
        'first_name': user_data.first_name,
        'last_name': user_data.last_name,
        'user_phone_number': user_data.user_phone_number,
    }
    access_token = create_access_token(payload=payload)

    new_user = await create_user(
        db,
        email=user_data.email,
        hashed_password=password_hash,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        user_phone_number=user_data.user_phone_number,
    )
    if new_user:
        new_user_verification_instance = await create_user_verification_instance_by_email(
            new_user.email,  # noqa
            db
        )  # in user_verification table
        await send_mail(
            subject='Welcome to TripNestArmenia',
            email_to=new_user.email,  # noqa
            body={'verification_code': new_user_verification_instance.verification_code},
        )

    response = TripNestArmeniaJSONResponse(
        status_code=status.HTTP_201_CREATED,
        message=messages.USER_CREATED,
        content={
            'verified': True,
            'first_name': new_user.first_name,
            'last_name': new_user.last_name,
            'email': new_user.email,
            'user_phone_number': new_user.user_phone_number,
            'access_token': access_token,
        }
    )

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite="lax",
        secure=False
    )
    return response


@router.post('/verify-user')
async def verify_user(user: UserVerificationSchema, db: AsyncSession = Depends(get_async_session)):
    user_instance = await get_user_by_email(user.email, db)
    if not user_instance:
        raise ValidationError(message=messages.EMAIL_NOT_EXISTS)
    verify_code_in_db = await get_user_verification_code_by_email(user.email, db)
    if verify_code_in_db:
        if user.verified_code == verify_code_in_db:
            await update_user_active_status(email=user.email, db=db)
        else:
            raise ValidationError(message=messages.INVALID_VERIFICATION_CODE)
    else:
        raise NotFound(message=messages.EMAIL_NOT_EXISTS)  # Need to change this logic
    # await delete_user_verify_instance_by_verify_code(verify_code_in_db, db)  # update -> delete

    return TripNestArmeniaJSONResponse(
        message=messages.USER_VERIFIED,
        status_code=status.HTTP_201_CREATED
    )  # user in front end side after success must see success message


@router.post("/sign-in")
async def user_sign_in(user: UserSignInSchema, db: AsyncSession = Depends(get_async_session)):
    user_from_db = await get_user_by_email(email=user.email, db=db)
    if not user_from_db:
        raise NotFound(message=messages.EMAIL_NOT_EXISTS)

    if not verify_password(plain_password=user.password, hashed_password=user_from_db.hashed_password):
        raise ValidationError(message=messages.INVALID_PASSWORD)

    payload: JWTPayload = {
        'first_name': str(user_from_db.first_name),
        'last_name': str(user_from_db.last_name),
        'email': str(user_from_db.email),
        'user_phone_number': str(user_from_db.user_phone_number)
    }
    access_token = create_access_token(payload=payload)

    response = TripNestArmeniaJSONResponse(
        content={
            'verified': True,
            'first_name': user_from_db.first_name,
            'last_name': user_from_db.last_name,
            'email': user_from_db.email,
            'user_phone_number': user_from_db.user_phone_number
        }
    )

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite="lax",  # 👈 работает на localhost
        secure=False
    )

    return response


@router.get("/check")
async def check_auth(request: Request, db: AsyncSession = Depends(get_async_session)):
    token = request.cookies.get("access_token")

    if not token:
        return TripNestArmeniaJSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Authorization token is missing", "authenticated": False},
        )

    payload = decode_access_token(token)
    user = None
    if payload:
        email_ = payload.get('email')
        user = await get_user_by_email(email_, db)
        if user:
            return TripNestArmeniaJSONResponse(
                content={'authenticated': True, 'email': email_}
            )

    return TripNestArmeniaJSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": "Invalid or expired token", "authenticated": False},
    )
