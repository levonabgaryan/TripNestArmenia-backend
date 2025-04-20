from typing import Optional

from pydantic import BaseModel, Field


class LocationModel(BaseModel):
    city: Optional[str] = Field(default=None)
    region: str


class PlaceDataModel(BaseModel):
    description: str
    location: LocationModel
    prefix: Optional[str]
