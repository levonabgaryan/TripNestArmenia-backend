from typing_extensions import Annotated

from pydantic import EmailStr, WrapValidator, BaseModel
from src.routers.auth.utils import validate_password_format

PasswordString = Annotated[str, WrapValidator(validate_password_format)]


class UserSignUpSchema(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: PasswordString


class UserVerificationSchema(BaseModel):
    email: EmailStr
    verified_code: str
