from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routers.auth import user_auth
from src.routers.places import images_
from src.routers.auth import admin_auth
from src.routers.tours import tours_

app = FastAPI()

app.include_router(user_auth.router)
app.include_router(images_.router)
app.include_router(admin_auth.router)
app.include_router(tours_.router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешить запросы от всех источников (можно заменить на свой домен)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]  # <-- Вот здесь ты разрешаешь читать все заголовки
)


@app.get("/health")
async def health():
    return 'ssss'
