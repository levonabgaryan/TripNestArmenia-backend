from typing_extensions import Annotated

from pydantic import EmailStr, WrapValidator, Field
from src.helpers.camel_case_base_schema import CamelCaseBaseModel
from src.routers.auth.utils import validate_password_format

PasswordString = Annotated[str, WrapValidator(validate_password_format)]


class UserSignUpSchema(CamelCaseBaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: PasswordString


class UserVerificationSchema(CamelCaseBaseModel):
    email: EmailStr
    verified_code: str
