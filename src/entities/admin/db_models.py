from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.helpers.databases.postgres_db.postgres_db import BaseDBModel


class Admin(BaseDBModel):
    __tablename__ = "admins"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str] = mapped_column()
    first_name: Mapped[str] = mapped_column(index=True)
    last_name: Mapped[str] = mapped_column(index=True)


class AdminChatMessage(BaseDBModel):
    __tablename__ = "admin_chat_messages"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    admin_id: Mapped[int] = mapped_column(ForeignKey("admins.id"), nullable=False)
    message: Mapped[str] = mapped_column(nullable=False)

    sender: Mapped["Admin"] = relationship("Admin", backref="chat_messages")
