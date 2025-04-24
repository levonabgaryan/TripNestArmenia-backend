from typing_extensions import Annotated

from pydantic import EmailStr, WrapValidator, BaseModel, Field
from src.routers.auth.utils import validate_password_format

PasswordString = Annotated[str, WrapValidator(validate_password_format)]


class UserSignUpSchema(BaseModel):
    first_name: str = Field(..., alias="firstName")
    last_name: str = Field(..., alias="lastName")
    email: EmailStr
    password: PasswordString


class UserVerificationSchema(BaseModel):
    email: EmailStr
    verified_code: str = Field(..., alias='verificationCode')


class UserSignInSchema(BaseModel):
    email: EmailStr
    password: PasswordString
