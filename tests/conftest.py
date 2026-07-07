import asyncio
import sys
import pytest_asyncio
import orjson

from typing import AsyncGenerator
from httpx import ASGITransport, AsyncClient
from pathlib import Path
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from src.core.config import settings
from src.database import Base, engine_null_pool, async_session_maker_null_pool
from src.models import *
from src.schemas.hotels import HotelAdd
from src.schemas.rooms import RoomAdd
from src.utils.db_manager import DBManager
from src.core.dependencies import get_db
from src.connectors.redis_manager import redis_manager

from src.main import app

BASE_DIR = Path(__file__).parent

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

def load_fixture(filename: str) -> list:
    return orjson.loads((BASE_DIR / filename).read_bytes())


@pytest_asyncio.fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.MODE == "TEST"


@pytest_asyncio.fixture(scope="session", loop_scope="session", autouse=True)
async def setup_redis():
    await redis_manager.connect()
    FastAPICache.init(RedisBackend(redis_manager.client), prefix="fastapi-cache-test")
    yield
    await redis_manager.close()


@pytest_asyncio.fixture(scope="session", loop_scope="session")
async def db(setup_database):
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db
        
        
async def get_db_null_pool():
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db
        
app.dependency_overrides[get_db] = get_db_null_pool


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        
        hotels = [HotelAdd.model_validate(h) for h in load_fixture("mock_hotels.json")]
        rooms = [RoomAdd.model_validate(r) for r in load_fixture("mock_rooms.json")]
       
    async with DBManager(session_factory=async_session_maker_null_pool) as db_: 
        await db_.hotels.add_bulk(hotels)
        await db_.rooms.add_bulk(rooms)
        await db_.commit()


@pytest_asyncio.fixture(scope="session", loop_scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest_asyncio.fixture(scope="session", autouse=True)        
async def register_user(ac, setup_database):
    response = await ac.post(
        "/auth/register",
        json={
            "email": "kot@pes.com",
            "password": "1234",
            "username": "testuser" 
        }
    )
    assert response.status_code == 200, response.json()
        
        

