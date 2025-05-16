from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped
from pydantic import EmailStr

from src.entities.user.db_models import User, UserVerificationCode
from src.entities.user.utils import generate_verification_code
from src.helpers.databases.postgres_db.postgres_db import insert_data, delete_data, update_data


async def get_user_by_email(email: EmailStr, db: AsyncSession) -> User | None:
    result = await db.execute(select(User).filter_by(email=email))
    return result.scalar()


async def create_user(db: AsyncSession, **kwargs) -> User:
    instance = User(**kwargs)
    result = await insert_data(db, instance)
    return result


async def create_user_verification_instance_by_email(email: EmailStr, db: AsyncSession) -> UserVerificationCode:
    user_instance = await db.execute(select(User).filter(User.email == email))
    user_instance = user_instance.scalar()
    user_id = user_instance.id
    verification_code = generate_verification_code()
    instance = UserVerificationCode(user_id=user_id, verification_code=verification_code)
    return await insert_data(db, instance)


async def update_verification_code_for_user(email: EmailStr, db: AsyncSession) -> None | str:

    verify_instance = await get_user_verification_instance_by_email(email=email, db=db)

    if not verify_instance:
        return

    new_verification_code = generate_verification_code()
    await update_data(
        db=db,
        table_=UserVerificationCode,
        instance_id=verify_instance.id,
        field_name="verification_code",
        new_value=new_verification_code
    )
    return new_verification_code

async def get_user_verification_instance_by_email(email: EmailStr, db: AsyncSession) -> UserVerificationCode | None:
    result = await db.execute(
        select(UserVerificationCode) \
            .join(User, User.id == UserVerificationCode.user_id) \
            .filter(User.email == email)
    )
    return result.scalar()


async def get_user_verification_code_by_email(email: EmailStr, db: AsyncSession) -> Mapped[str] | None:
    result = await get_user_verification_instance_by_email(email, db)
    return result.verification_code


async def update_user_active_status(email: EmailStr, db: AsyncSession) -> User | None:
    user = await get_user_by_email(email=email, db=db)
    if user:
        user.active = True
        await db.commit()
    return user


async def delete_user_verify_instance_by_verify_code(verify_code: str, db: AsyncSession) -> UserVerificationCode | None:
    instance_to_delete = await db.execute(select(UserVerificationCode).filter(
        UserVerificationCode.verification_code == verify_code))
    instance_to_delete = instance_to_delete.scalar()
    if instance_to_delete:
        result = await delete_data(db, instance_to_delete)
        return result
    else:
        return None
