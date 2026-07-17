from pydantic import BaseModel

from src.schemas.hotels import Hotel, HotelAdd


class HotelBulkPatch(BaseModel):
    id: int
    title: str


async def test_add_hotel(db):
    hotel_data = HotelAdd(title="Hotel 5 stars", location="Sochi")
    await db.hotels.add_constructor(hotel_data)
    await db.commit()


async def test_edit_and_patch_hotels_bulk(db):
    original_hotels = (await db.hotels.get_all())[:2]
    edited_hotels = [
        Hotel(id=hotel.id, title=f"Edited {hotel.id}", location=f"Location {hotel.id}")
        for hotel in original_hotels
    ]

    try:
        await db.hotels.edit_bulk(edited_hotels)

        for expected in edited_hotels:
            actual = await db.hotels.get_one_or_none(id=expected.id)
            assert actual == expected

        patched_hotel = HotelBulkPatch(
            id=edited_hotels[0].id,
            title="Patched title",
        )
        await db.hotels.patch_bulk([patched_hotel])

        actual = await db.hotels.get_one_or_none(id=patched_hotel.id)
        assert actual is not None
        assert actual.title == patched_hotel.title
        assert actual.location == edited_hotels[0].location
    finally:
        await db.hotels.edit_bulk(original_hotels)
        await db.commit()
