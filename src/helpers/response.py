from typing import Any

from fastapi.responses import JSONResponse
from fastapi import status
from src.helpers import messages


class TripNestArmeniaJSONResponse(JSONResponse):
    status_code = status.HTTP_200_OK
    # message = messages.SUCCESS

    def __init__(
            self,
            status_code=status_code,
            message: str | None = None,
            content: dict[str, Any] | None = None
    ):
        content = content or {}

        content['status_code'] = status_code
        content['message'] = message

        super().__init__(status_code=status_code, content=content)
