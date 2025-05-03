from fastapi import Request
from src.helpers.response import TripNestArmeniaJSONResponse
from src.routers.auth.utils import decode_access_token
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import status

PROTECTED_PATHS = {"/tours/book-tour"}

class CheckAccessTokenMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        if path in PROTECTED_PATHS:
            # Извлекаем токен из cookies
            token = request.cookies.get("access_token")
            if not token:
                return TripNestArmeniaJSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"detail": "Authorization token is missing"},
                )

            payload = decode_access_token(token=token)
            if payload:
                # Дополняем запрос информацией о пользователе
                request.state.user = payload
                return await call_next(request)
            else:
                return TripNestArmeniaJSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"detail": "Invalid or expired token", "authenticated": False},
                )

        response = await call_next(request)
        return response
