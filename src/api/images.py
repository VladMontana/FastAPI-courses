import aiofiles

from fastapi import APIRouter, UploadFile

from src.tasks.tasks import compress_image_to_sizes

router = APIRouter(prefix="/images", tags=["Изображение отелей"])


@router.post("")
async def upload_images(file: UploadFile):
    image_path = f"src/static/images/{file.filename}"
    
    async with aiofiles.open(image_path, "wb+") as new_file:
        while chunk := await file.read(1024 * 1024):
            await new_file.write(chunk)
    
    await compress_image_to_sizes(image_path)
    
    return None

