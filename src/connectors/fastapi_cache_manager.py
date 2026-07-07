import redis.asyncio as redis
from redis.asyncio import Redis

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from src.core.config import settings


class FastAPICacheManager:
    """
    Менеджер для подключения fastapi-cache2 к Redis.

    Используется не для ручных get/set/delete, а для работы декоратора:

        @cache(expire=60)

    Этот менеджер инициализирует FastAPICache через RedisBackend.
    """

    def __init__(
        self,
        redis_url: str,
        prefix: str = "fastapi-cache",
    ) -> None:
        """
        Создает экземпляр FastAPICacheManager.

        :param redis_url: строка подключения к Redis.
            Например: redis://localhost:6379
        :param prefix: общий префикс для ключей fastapi-cache2.
            Благодаря этому ключи кэша не будут смешиваться с ручными
            ключами RedisManager.
        """
        self.redis_url = redis_url
        self.prefix = prefix
        self.client: Redis | None = None

    async def connect(self) -> None:
        """
        Подключается к Redis и инициализирует FastAPICache.

        Для fastapi-cache2 используется decode_responses=False,
        потому что библиотека хранит кэшированные данные как bytes.
        """
        self.client = redis.from_url(
            self.redis_url,
            decode_responses=False,
        )

        await self.client.ping()

        FastAPICache.init(
            RedisBackend(self.client),
            prefix=self.prefix,
        )

    async def close(self) -> None:
        """
        Закрывает Redis-соединение, которое используется fastapi-cache2.
        """
        if self.client is not None:
            await self.client.aclose()
            self.client = None


fastapi_cache_manager: FastAPICacheManager = FastAPICacheManager(
    redis_url=settings.REDIS_URL,
    prefix="fastapi-cache",
)