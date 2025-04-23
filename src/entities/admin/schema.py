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
