from sqlalchemy.orm import Mapped, mapped_column

from src.helpers.databases.postgres_db.postgres_db import BaseDBModel


class Accomplisher(BaseDBModel):
    __tablename__ = "accomplishers"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    first_name: Mapped[str] = mapped_column(index=True)
    last_name: Mapped[str] = mapped_column(index=True)
    phone_number: Mapped[str] = mapped_column(nullable=True)
    info: Mapped[str] = mapped_column(nullable=True)