from typing import Annotated

from pydantic import BaseModel, EmailStr, WrapValidator

from src.routers.auth.utils import validate_password_format

PasswordString = Annotated[str, WrapValidator(validate_password_format)]


class AdminCreateSchema(BaseModel):
    email: EmailStr
    password: PasswordString
    first_name: str
    last_name: str


class AdminSignInSchema(BaseModel):
    email: EmailStr
    password: PasswordString


class ChatMessageResponseSchema(BaseModel):
    id: int
    admin_id: int
    sender_first_name: str
    sender_last_name: str
    message: str
    timestamp: str
