import aiofiles

from fastapi import UploadFile
from src.tasks.tasks import compress_image_to_sizes


class ImagesService:
    async def upload_images(self, file: UploadFile):
        image_path = f"src/static/images/{file.filename}"

        async with aiofiles.open(image_path, "wb+") as new_file:
            while chunk := await file.read(1024 * 1024):
                await new_file.write(chunk)

        await compress_image_to_sizes(image_path)
