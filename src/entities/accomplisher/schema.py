from typing import Optional
from pydantic import BaseModel, EmailStr


class AccomplisherModel(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    phone_number: Optional[str]
    info: Optional[str]
