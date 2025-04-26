from typing import Optional

from sqlalchemy import CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column
from src.helpers.databases.postgres_db import BaseDBModel

class Tour(BaseDBModel):
    __tablename__ = "tours"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_email: Mapped[str] = mapped_column(unique=True)
    user_phone_number: Mapped[str] = mapped_column()
    destination: Mapped[Optional[str]] = mapped_column(default='')
    need_hotel: Mapped[bool] = mapped_column(default=False)
    number_of_people: Mapped[int] = mapped_column(CheckConstraint('count > 0', name='count_positive'))
    description: Mapped[int] = mapped_column()
