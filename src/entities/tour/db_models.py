from typing import Optional
import re

from sqlalchemy import CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column
from pydantic import EmailStr

from src.helpers.databases.postgres_db import BaseDBModel

class Tour(BaseDBModel):
    __tablename__ = "tours"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_email: Mapped[EmailStr] = mapped_column(unique=True)
    user_phone_number: Mapped[str] = mapped_column()
    destination: Mapped[Optional[str]] = mapped_column()
    need_hotel: Mapped[bool] = mapped_column()
    count: Mapped[int] = mapped_column(CheckConstraint('count > 0', name='count_positive'))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.user_phone_number or not re.match(r'^\+?[1-9]\d{1,14}$', self.user_phone_number):
            raise ValueError(f"Invalid phone number format: {self.user_phone_number}")