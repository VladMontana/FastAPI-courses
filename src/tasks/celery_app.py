from celery import Celery
from celery.schedules import crontab

from src.core.config import settings

celery_instance = Celery(
    main="tasks", broker=settings.REDIS_URL, include=["src.tasks.tasks"]
)

celery_instance.conf.update(
    # Формат сообщений
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    # Временная зона
    timezone="Europe/Moscow",
    enable_utc=True,
    # Повторные попытки при сбое брокера
    broker_connection_retry_on_startup=True,
    # Время жизни результата задачи (в секундах)
    result_expires=3600,
)

celery_instance.conf.beat_schedule = {
    "send": {
        "task": "booking_today_checkin",
        "schedule": crontab(minute=5),
    }
}
