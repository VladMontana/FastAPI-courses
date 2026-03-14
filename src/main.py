from fastapi import FastAPI

from src.api.hotels import router as hotel_router
from src.api.auth import router as auth_router
from src.api.rooms import router as room_router

app = FastAPI(version="0.1.0")

app.include_router(auth_router)
app.include_router(hotel_router)
app.include_router(room_router)
