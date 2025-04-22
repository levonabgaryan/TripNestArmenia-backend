import datetime as dt
from typing import AsyncGenerator, Any

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from src.settings import DBConfiguration as Db

DATABASE_URL = f"postgresql+asyncpg://{Db.USER}:{Db.PASSWORD}@{Db.HOST}:{Db.PORT}/{Db.NAME}"
# for alembic.ini postgresql+psycopg2://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}

async_engine = create_async_engine(DATABASE_URL, echo=True)
Base = declarative_base()


async_session = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_async_session() -> AsyncGenerator[AsyncSession | Any, Any]:
    async with async_session() as async_session_client:
        yield async_session_client


class BaseDBModel(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )

    updated_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )


# docker stop $(docker ps -aq) && docker rm $(docker ps -aq) && docker rmi $(docker images -q) && docker volume prune -f && docker volume rm $(docker volume ls -q) && docker network prune -f && docker system prune -a --volumes -f

async def insert_data[T: BaseDBModel](db: AsyncSession, instance: T) -> T | None:
    db.add(instance)
    await db.commit()
    await db.refresh(instance)
    return instance


async def delete_data[T: BaseDBModel](db: AsyncSession, instance: T) -> T | None:
    await db.delete(instance)
    await db.commit()
    return instance
