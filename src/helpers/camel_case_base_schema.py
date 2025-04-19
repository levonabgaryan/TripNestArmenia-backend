from pydantic import BaseModel
from pydantic.alias_generators import to_camel


class CamelCaseBaseModel(BaseModel):
    class Config:
        alias_generator = to_camel
        populate_by_name = True
        from_attributes = True
