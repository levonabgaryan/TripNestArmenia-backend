from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routers.auth import user_auth

app = FastAPI()

app.include_router(user_auth.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return 'ssss'


