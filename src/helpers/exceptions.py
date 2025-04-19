from typing import Dict, Any

from fastapi import HTTPException, status

from src.helpers import messages


class TripNestArmeniaException(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    message = messages.INTERNAL_SERVER_ERROR

    def __init__(
            self,
            status_code=status_code,
            message=message,
            content: Dict[str, Any] | None = None
    ):
        content = content or {}
        content['status_code'] = status_code
        content['message'] = message
        super().__init__(status_code=status_code, detail=content)


class ValidationError(TripNestArmeniaException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = "VALIDATION_ERROR"


class NotFound(TripNestArmeniaException):
    status_code = status.HTTP_404_NOT_FOUND
    message = messages.NOT_FOUND


class EmailExists(TripNestArmeniaException):
    status_code = status.HTTP_409_CONFLICT
    message = messages.EMAIL_EXISTS