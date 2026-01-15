from fastapi import FastAPI
from src.api.hotels import router as hotel_router

app = FastAPI(title="Мобильное приложение API", version="0.1.0")

app.include_router(hotel_router)
