import re
from typing import TypedDict, NotRequired
from copy import deepcopy
from datetime import datetime, timedelta, timezone

from passlib.context import CryptContext
from pydantic import EmailStr
import jwt
from jwt.exceptions import InvalidTokenError


from src.helpers.exceptions import ValidationError
from src.helpers.messages import INCORRECT_PASSWORD_FORMAT

# must be taken from env
SECRET_KEY = 'MY_SECRET_KEY'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_DAYS = 30

PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")

class JWTPayload(TypedDict):
    email: EmailStr
    first_name: str
    last_name: str
    user_phone_number: str
    exp: NotRequired[datetime]


def is_valid_password(password: str) -> bool:
    pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=[\]{}]).{8,}$"  # issue with password check
    return re.match(pattern, password) is not None


def validate_password_format(value: str, handler) -> str:
    if not is_valid_password(value):
        raise ValidationError(message=INCORRECT_PASSWORD_FORMAT)

    return value


def get_password_hash(password: str) -> str:
    return PWD_CONTEXT.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return PWD_CONTEXT.verify(plain_password, hashed_password)


def create_access_token(payload: JWTPayload, expires_time: int = ACCESS_TOKEN_EXPIRE_DAYS) -> str:
    to_encode = deepcopy(payload)
    expire_time = datetime.now(timezone.utc) + timedelta(minutes=expires_time)
    to_encode.update({'exp': expire_time})
    return jwt.encode(payload=to_encode, key=SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> JWTPayload | None:
    try:
        payload = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except InvalidTokenError:
        return None
