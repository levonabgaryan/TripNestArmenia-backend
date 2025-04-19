from fastapi import UploadFile
from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, Union

from src.helpers.databases.mongo_db.mongo_db import mongo_async_client
from src.helpers.databases.mongo_db.mongo_collections.places import PLACES


class LocationModel(BaseModel):
    city: Optional[str] = Field(default=None)
    region: str


class PlaceModel(BaseModel):
    description: str
    location: LocationModel
    image_or_url: Union[str, HttpUrl, UploadFile]


async def create_collection_if_not_exists() -> None:
    collection_names = await mongo_async_client.list_collection_names()
    if "places" not in collection_names:
        collection = mongo_async_client["places"]
        await collection.insert_one({
            "name": "Test Place",
            "description": "This is a test place.",
            "location": {
                "city": "Yerevan",
                "region": "Ararat"
            }
        })
        validated_data = [PlaceModel(**place).model_dump() for place in PLACES]
        print('++++++++++++')
        print(validated_data)
        print('++++++++++++')
        if validated_data:
            await collection.insert_many(documents=validated_data)