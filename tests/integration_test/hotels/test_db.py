from src.schemas.hotels import HotelAdd
from tests.conftest import db


async def test_add_hotel(db):
    hotel_data = HotelAdd(title="Hotel 5 stars", location="Sochi")
    new_hotel_data = await db.hotels.add_constructor(hotel_data)
    await db.commit()
