from typing import Any, Dict, List

from fastapi.responses import JSONResponse
from fastapi import status
import inflection

from src.helpers import messages


class TripNestArmeniaJSONResponse(JSONResponse):
    status_code = status.HTTP_200_OK
    message = messages.SUCCESS

    def __init__(
            self,
            status_code=status_code,
            message: str = messages,
            content: Dict[str, Any] | None = None
    ):
        content = content or {}

        content['status_code'] = status_code
        content['message'] = message

        content = convert_keys_to_camel_case(content)

        super().__init__(status_code=status_code, content=content)


def to_camel_case(string: str) -> str:
    return inflection.camelize(string, uppercase_first_letter=False)


def convert_keys_to_camel_case(data: Dict[str, Any] | List[Any]) -> Dict[str, Any] | List[Any]:
    if isinstance(data, dict):
        return {to_camel_case(key): convert_keys_to_camel_case(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [convert_keys_to_camel_case(item) for item in data]
    else:
        return data
