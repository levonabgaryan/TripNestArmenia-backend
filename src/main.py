from typing import List

from fastapi import FastAPI, UploadFile, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from src.routers.auth import user_auth
from src.helpers.databases.mongo_db.mongo_file_manager import download_file_from_mongo_db, upload_image_in_db, create_images_zip_buffer

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
async def health():
    return 'ssss'


@app.get("/image/{image_id}")
async def get_image_from_mongo(image_id: str):
    # Получаем поток из MongoDB
    stream = await download_file_from_mongo_db(image_id)

    # Определяем заголовок Content-Type. Вам нужно будет добавить логику для определения типа изображения
    # Например, если это JPEG, используйте 'image/jpeg', если PNG - 'image/png' и так далее.
    # Для простоты здесь будет указан `application/octet-stream`.
    return StreamingResponse(stream, media_type="application/octet-stream")


@app.post("/upload-image")
async def upload_image_in_mongo_db(file_name: str, image: UploadFile):
    await upload_image_in_db(file=image, file_name=file_name)


@app.post("/images/download")
async def download_images(file_names: List[str] = Body(...)):
    zip_buf = await create_images_zip_buffer(file_names)
    return StreamingResponse(
        zip_buf,
        media_type="application/zip",
        headers={"Content-Disposition": 'attachment; filename="images.zip"'}
    )