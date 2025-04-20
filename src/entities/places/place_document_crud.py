from typing import Mapping, Any

from src.helpers.databases.mongo_db.mongo_db import mongo_async_client


async def get_document_about_place_by_name(name: str) -> Mapping[str, Any] | None:
    name = name.lower()
    collection = mongo_async_client["places"]
    document = await collection.find_one({"name": name})
    return document
