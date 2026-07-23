from fastapi import APIRouter, UploadFile
from src.services.images import ImagesService

router = APIRouter(prefix="/images", tags=["Изображение отелей"])


@router.post("")
async def upload_images(file: UploadFile):
    await ImagesService().upload_images(file)

    return None
