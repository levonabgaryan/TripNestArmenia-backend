from __future__ import annotations
import os
import asyncio

from pydantic import BaseModel, Field
from typing import Optional, Iterable, Dict

from src.helpers.databases.mongo_db.mongo_db import mongo_async_client
from src.helpers.databases.mongo_db.mongo_collections.places.places_data import DATA
from src.helpers.databases.mongo_db.mongo_file_manager import upload_local_image_in_db


class LocationModel(BaseModel):
    city: Optional[str] = Field(default=None)
    region: str


class PlaceModel(BaseModel):
    description: str
    location: LocationModel
    image_uri: Optional[str]

    @property
    def to_dict_with_correct_image_id(self) -> Dict[str, str | Dict[str, str]]:
        data = self.model_dump()
        data['image_uri'] = os.path.basename(self.image_uri)
        return data


async def create_collection_if_not_exists() -> None:
    collection = mongo_async_client["places"]
    collection_names = await mongo_async_client.list_collection_names()
    if "places" not in collection_names:
        await collection.insert_one({
            "name": "Test Place",
            "description": "This is a test place.",
            "location": {
                "city": "Yerevan",
                "region": "Ararat"
            }
        })


    validate_data: Iterable[Dict] = (PlaceModel(**data).model_dump() for data in DATA)

    if validate_data:
        tasks = []  # Список задач для асинхронной обработки
        for data in validate_data:
            tasks.append(upload_local_image_in_db(data['image_uri']))  # Добавляем задачу в список
            tasks.append(collection.insert_one(data))  # Добавляем задачу вставки данных

        await asyncio.gather(*tasks)
