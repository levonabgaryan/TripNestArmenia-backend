from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import EmailStr

from src.entities.admin.db_models import Admin, AdminChatMessage
from src.helpers.databases.postgres_db.postgres_db import insert_data, delete_data


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
    admin = await get_admin_by_email(email=email, db=db)
    if admin:
        admin.active = True
        await db.commit()
    return admin


async def save_message_in_admins_chat(
    db: AsyncSession,
    admin_id: int,
    message: str,
) -> None | AdminChatMessage:
    message_instance = AdminChatMessage(
        admin_id=admin_id,
        message=message,
    )
    result = await insert_data(db=db, instance=message_instance)

    if result:
        print(f"Message saved: {message_instance}")
    else:
        print("Failed to save message")

    return result


async def get_first_50_messages_of_chat(db: AsyncSession) -> list[dict[str, str]]:
    result = await db.execute(
        select(
            Admin.first_name.label("first_name"),
            Admin.last_name.label("last_name"),
            AdminChatMessage.message,
        )
        .join(Admin, Admin.id == AdminChatMessage.admin_id)
        .order_by(AdminChatMessage.created_at)
        .limit(50)
    )
    rows = result.all()  # список кортежей (first_name, last_name, message)
    return [
        {"first_name": fn, "last_name": ln, "message": msg}
        for fn, ln, msg in rows
    ]


async def find_admin_first_name_last_name_by_id(db: AsyncSession, admin_id: int) -> tuple[str, str] | None:
    result = await db.execute(
        select(Admin.first_name, Admin.last_name)
        .filter(Admin.id == admin_id)
    )
    row = result.first()
    if row is None:
        return None
    return row[0], row[1]

