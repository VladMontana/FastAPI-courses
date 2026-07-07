from typing import AsyncIterator
from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.api.hotels import router as hotel_router
from src.api.auth import router as auth_router
from src.api.rooms import router as room_router
from src.api.bookings import router as booking_router
from src.api.facilities import router as facility_router
from src.api.images import router as images_router

from src.connectors.redis_manager import redis_manager
from src.connectors.fastapi_cache_manager import fastapi_cache_manager

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    await redis_manager.connect()
    await fastapi_cache_manager.connect()
    yield
    await redis_manager.close()
    await fastapi_cache_manager.close()

app = FastAPI(version="0.1.0", lifespan=lifespan)

app.include_router(auth_router)
app.include_router(hotel_router)
app.include_router(room_router)
app.include_router(booking_router)
app.include_router(facility_router)
app.include_router(images_router)