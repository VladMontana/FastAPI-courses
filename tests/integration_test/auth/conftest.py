import pytest_asyncio
from httpx import AsyncClient
from collections.abc import AsyncGenerator


@pytest_asyncio.fixture(scope="function")
async def clear_cookies(ac: AsyncClient) -> AsyncGenerator[None, None]:
    ac.cookies.clear()
    yield
    ac.cookies.clear()
