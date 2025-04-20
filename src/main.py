from fastapi import FastAPI, UploadFile, Body
from fastapi.middleware.cors import CORSMiddleware

from src.routers.auth import user_auth
from src.routers.places import data_

app = FastAPI()

app.include_router(user_auth.router)
app.include_router(data_.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    return 'ssss'
