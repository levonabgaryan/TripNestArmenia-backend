from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import EmailStr

from src.entities.admin.db_models import Admin
from src.helpers.databases.postgres_db import insert_data, delete_data



async def create_admin_in_db(db: AsyncSession, **kwargs) -> Admin:
    instance = Admin(**kwargs)
    result = await insert_data(db, instance)
    return result


async def delete_admin(db: AsyncSession, admin: Admin) -> Admin | None:
    result = await delete_data(db, admin)
    return result


async def get_admin_by_email(email: EmailStr, db: AsyncSession) -> Admin | None:
    result = await db.execute(select(Admin).filter_by(email=email))
    return result.scalar()


async def update_admin_active_status(email: EmailStr, db: AsyncSession) -> Admin | None:
    user = await get_admin_by_email(email=email, db=db)
    if user:
        user.active = True
        await db.commit()
    return user
