import asyncio
from pathlib import Path
from PIL import Image # type: ignore

from src.tasks.celery_app import celery_instance
from src.utils.db_manager import DBManager
from src.database import async_session_maker_null_pool

@celery_instance.task
def compress_image_to_sizes(
    image_path: str,
    output_dir: str = "src/static/images",
    widths: tuple[int, ...] = (1000, 500, 200),
    quality: int = 85,
) -> list[Path]:
    """
    Сжимает изображение до указанных ширин и сохраняет получившиеся файлы
    в заданную локальную директорию.

    Высота каждого изображения рассчитывается автоматически, чтобы сохранить
    исходные пропорции. Файлы сохраняются в формате JPEG с именами вида:
    `<имя_файла>_1000px.jpg`, `<имя_файла>_500px.jpg`, `<имя_файла>_200px.jpg`.

    Args:
        image_path: Путь к исходному изображению.
        output_dir: Путь к директории, куда будут сохранены изображения.
        widths: Набор ширин, до которых нужно уменьшить изображение.
        quality: Качество JPEG-файла от 1 до 100.

    Returns:
        Список путей к сохранённым изображениям.
    """
    image_path = Path(image_path)
    output_dir = Path(output_dir)

    saved_files = []
    
    with Image.open(image_path) as img:
        img = img.convert("RGB")

        original_width, original_height = img.size

        for width in widths:
            height = int(original_height * width / original_width)

            resized_img = img.resize(
                (width, height),
                Image.Resampling.LANCZOS
            )

            output_path = output_dir / f"{image_path.stem}_{width}px.jpg"

            resized_img.save(
                output_path,
                format="JPEG",
                quality=quality,
                optimize=True
            )

            saved_files.append(output_path)

    return saved_files


async def get_bookings_with_today_checkin_helper():
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        await db.bookings.get_bookings_with_today_checkin()
    

@celery_instance.task(name="booking_today_checkin")
def send_email_to_users_with_today_checkin():
    asyncio.run(get_bookings_with_today_checkin_helper())

