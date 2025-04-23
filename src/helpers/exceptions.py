from typing import Dict, Any
from fastapi import HTTPException, status
from pydantic import EmailStr

from src.helpers import messages


class TripNestArmeniaException(HTTPException):
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_message: str = messages.INTERNAL_SERVER_ERROR

    def __init__(self, message: str | None = None, content: Dict[str, Any] | None = None):
        msg = message or self.default_message
        content = content or {}
        content.update({
            'status_code': self.status_code,
            'message': msg
        })
        super().__init__(status_code=self.status_code, detail=content)


class ValidationError(TripNestArmeniaException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_message = "VALIDATION_ERROR"


class NotFound(TripNestArmeniaException):
    status_code = status.HTTP_404_NOT_FOUND
    default_message = messages.NOT_FOUND


class EmailExists(TripNestArmeniaException):
    status_code = status.HTTP_409_CONFLICT
    default_message = messages.EMAIL_EXISTS

    def __init__(self, email: EmailStr):
        full_message = f"{email} {self.default_message}"
        super().__init__(message=full_message)
