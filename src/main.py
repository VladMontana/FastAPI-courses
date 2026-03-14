from fastapi import FastAPI
from src.api.hotels import router as hotel_router
from src.api.auth import router as auth_router

app = FastAPI(version="0.1.0")

app.include_router(auth_router)
app.include_router(hotel_router)
