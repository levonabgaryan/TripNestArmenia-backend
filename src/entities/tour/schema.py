from datetime import date
from enum import StrEnum
from decimal import Decimal

from pydantic import BaseModel, EmailStr, Field


class TourStatus(StrEnum):
    CREATED = "CREATED"
    IN_PROGRESS = "IN_PROGRESS"
    ACTIVE = "ACTIVE"
    REJECTED = "REJECTED"
    ENDED = "ENDED"


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


class ChangeTourStatusModel(BaseModel):
    tour_id: int = Field(..., alias="tourId")
    new_status: TourStatus = Field(..., alias="newStatus")


class UpdateAmountTourModel(BaseModel):
    tour_id: int = Field(..., alias="tourId")
    amount: Decimal

class UserCommentModel(BaseModel):
    tour_id: int
    comment: str