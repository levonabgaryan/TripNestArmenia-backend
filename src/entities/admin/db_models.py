from sqlalchemy.orm import Mapped, mapped_column

from src.helpers.databases.postgres_db import BaseDBModel

class Admin(BaseDBModel):
    __tablename__ = "admins"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str] = mapped_column()
    first_name: Mapped[str] = mapped_column(index=True)
    last_name: Mapped[str] = mapped_column(index=True)
