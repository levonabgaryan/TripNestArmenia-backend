import re
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.helpers.databases.postgres_db import BaseDBModel


class User(BaseDBModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str] = mapped_column(default='')
    first_name: Mapped[str] = mapped_column(index=True)
    last_name: Mapped[str] = mapped_column(index=True)
    user_phone_number: Mapped[str] = mapped_column(default='')
    active: Mapped[bool] = mapped_column(default=False)
    user_verification_code: Mapped["UserVerificationCode"] = \
        relationship(
            back_populates="user",
            uselist=False,
            cascade="all, delete"
        )

class UserVerificationCode(BaseDBModel):
    __tablename__ = "users_verification_codes"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
    verification_code: Mapped[str] = mapped_column(default='')

    user: Mapped["User"] = relationship(back_populates="user_verification_code", uselist=False)
