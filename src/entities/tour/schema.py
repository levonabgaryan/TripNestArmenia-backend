from datetime import date
import enum

from pydantic import BaseModel, EmailStr, Field


class BookTourModel(BaseModel):
    user_email: EmailStr = Field(..., alias="email")
    user_phone_number: str = Field(..., alias="userPhoneNumber")
    need_hotel: bool = Field(default=False, alias="needHotel")
    destination: str
    booking_date: date = Field(..., alias="bookingDate")
    description: str
    number_of_people: int = Field(..., alias="numberOfPeople")

    def to_dict(self):
        data = self.__dict__.copy()
        for key, value in data.items():
            if isinstance(value, date):
                data[key] = value.isoformat()
        return data

class TourStatus(enum.Enum):
    CREATED = "created"
    IN_PROGRESS = "in_progress"
    ACTIVE = "active"
    REJECTED = "rejected"
    ENDED = "ended"
