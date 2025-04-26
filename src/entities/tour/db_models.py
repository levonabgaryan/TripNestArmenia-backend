from typing import Optional
from datetime import date
from decimal import Decimal

from sqlalchemy import Numeric
from sqlalchemy import CheckConstraint, Enum
from sqlalchemy.orm import Mapped, mapped_column

from src.helpers.databases.postgres_db import BaseDBModel
from src.entities.tour.schema import TourStatus


class Tour(BaseDBModel):
    __tablename__ = "tours"
    __table_args__ = (
        CheckConstraint('number_of_people > 0', name='count_positive'),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_email: Mapped[str] = mapped_column()
    user_phone_number: Mapped[str] = mapped_column()
    destination: Mapped[Optional[str]] = mapped_column(default='')
    need_hotel: Mapped[bool] = mapped_column(default=False)
    number_of_people: Mapped[int] = mapped_column()
    booking_date: Mapped[date] = mapped_column()
    description: Mapped[str] = mapped_column()
    status: Mapped[TourStatus] = mapped_column(Enum(TourStatus), default=TourStatus.CREATED)

    amount_by_dram: Mapped[Decimal] = mapped_column(
        Numeric(precision=12, scale=2),  # 12 цифр максимум, из них 2 после запятой
        nullable=False,
        default=0
    )

    def to_dict(self) -> dict:
        d = {}
        for column in self.__table__.columns:
            d[column.name] = str(getattr(self, column.name))

        return d