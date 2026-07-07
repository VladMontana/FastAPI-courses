from typing import Any

import redis.asyncio as redis
from redis.asyncio import Redis

from src.core.config import settings


class RedisManager:
    """
    Менеджер для ручной работы с Redis.

    Используется для прямых операций с Redis:
    set, get, delete.

    Подходит для хранения временных данных, токенов, кодов подтверждения,
    ручного кэша и других данных, где ты сам управляешь ключами.
    """

    def __init__(
        self,
        redis_url: str,
        prefix: str = "app",
    ) -> None:
        """
        Создает экземпляр RedisManager.

        :param redis_url: строка подключения к Redis.
            Например: redis://localhost:6379
        :param prefix: префикс для ключей, чтобы отделить ручные ключи
            приложения от ключей fastapi-cache.
        """
        self.redis_url = redis_url
        self.prefix = prefix
        self.client: Redis | None = None

    async def connect(self) -> None:
        """
        Подключается к Redis и проверяет соединение через ping.

        decode_responses=True означает, что Redis будет возвращать строки,
        а не bytes. Это удобно для ручной работы с данными.
        """
        self.client = redis.from_url(
            self.redis_url,
            decode_responses=True,
        )

        await self.client.ping()

    def _get_client(self) -> Redis:
        """
        Возвращает активный Redis-клиент.

        :raises RuntimeError: если connect() еще не был вызван.
        :return: Redis-клиент.
        """
        if self.client is None:
            raise RuntimeError("Redis is not connected. Call connect() first.")

        return self.client

    def _build_key(self, key: str) -> str:
        """
        Добавляет префикс к ключу Redis.

        Например:
        key='facilities'
        prefix='app'

        Итоговый ключ:
        app:facilities

        :param key: исходный ключ.
        :return: ключ с префиксом.
        """
        return f"{self.prefix}:{key}"

    async def set(
        self,
        key: str,
        value: Any,
        expire: int | None = None,
    ) -> bool:
        """
        Сохраняет значение в Redis.

        :param key: ключ без префикса.
        :param value: значение, которое нужно сохранить.
        :param expire: время жизни ключа в секундах.
            Если None, ключ будет храниться без ограничения по времени.
        :return: True, если значение успешно сохранено.
        """
        client = self._get_client()

        return await client.set(
            name=self._build_key(key),
            value=value,
            ex=expire,
        )

    async def get(self, key: str) -> str | None:
        """
        Получает значение из Redis по ключу.

        :param key: ключ без префикса.
        :return: строка из Redis или None, если ключ не найден.
        """
        client = self._get_client()

        return await client.get(name=self._build_key(key))

    async def delete(self, key: str) -> int:
        """
        Удаляет ключ из Redis.

        :param key: ключ без префикса.
        :return: количество удаленных ключей.
        """
        client = self._get_client()

        return await client.delete(self._build_key(key))

    async def close(self) -> None:
        """
        Закрывает соединение с Redis.
        """
        if self.client is not None:
            await self.client.close()
            self.client = None


redis_manager: RedisManager = RedisManager(
    redis_url=settings.REDIS_URL,
    prefix="app",
)