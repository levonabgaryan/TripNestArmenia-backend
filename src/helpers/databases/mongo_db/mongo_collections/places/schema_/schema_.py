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
    name: str  # must be unique for init data
    description: str
    location: LocationModel
    image_uri: Optional[str]

    @property
    def to_dict_with_correct_image_id(self) -> Dict[str, str | Dict[str, str]]:
        data = self.model_dump()
        data['image_uri'] = os.path.basename(self.image_uri)
        return data


async def handle_place_insert(data: dict, collection):
    place = PlaceModel(**data)
    image_name = os.path.basename(place.image_uri)

    # Проверка наличия по уникальному name
    existing = await collection.find_one({"name": place.name})
    if existing:
        return  # Пропускаем, если уже есть

    # Загружаем изображение (если его ещё нет)
    await upload_local_image_in_db(place.image_uri)

    # Подготавливаем документ и вставляем
    document = place.model_dump()
    document['image_uri'] = image_name
    await collection.insert_one(document)


async def create_collection_if_not_exists() -> None:
    collection = mongo_async_client["places"]

    existing_collections = await mongo_async_client.list_collection_names()
    if "places" not in existing_collections:
        await collection.insert_one({
            "name": "Test Place",
            "description": "This is a test place.",
            "location": {
                "city": "Yerevan",
                "region": "Ararat"
            }
        })

    # 3) Подготавливаем корутины для загрузки картинок и вставки документов
    async def handle_place(data: dict):
        place = PlaceModel(**data)
        image_name = os.path.basename(place.image_uri)

        if await collection.find_one({"name": place.name}):
            return

        await upload_local_image_in_db(place.image_uri)

        doc = place.model_dump()
        doc["image_uri"] = image_name
        await collection.insert_one(doc)

    tasks = [handle_place(data) for data in DATA]
    await asyncio.gather(*tasks)
