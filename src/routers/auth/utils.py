import re
from passlib.context import CryptContext

from src.helpers.exceptions import ValidationError
from src.helpers.messages import INVALID_PASSWORD_FORMAT


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def is_valid_password(password: str) -> bool:
    pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=[\]{}]).{8,}$"  # issue with password check
    return re.match(pattern, password) is not None


def validate_password_format(value, handler):
    if not is_valid_password(value):
        raise ValidationError(message=INVALID_PASSWORD_FORMAT)

    return value

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)